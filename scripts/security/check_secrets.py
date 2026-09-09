#!/usr/bin/env python3
"""Scan the working tree for likely committed secrets.

Prints path, line number, and pattern name only. Never prints matched values.
Exit 0 if clean, 1 if a finding is reported, 2 on usage/IO errors.

This is a conservative educational-repo scanner, not a production secret-detection
platform. Re-run after any addition of env files, dumps, or wallet material.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".zip",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".pyc",
    ".pyo",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
}

# Filenames that must never be committed (except the allowlisted example).
SENSITIVE_FILENAMES = {
    ".env",
    "wallets.json",
    "wallet.json",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
    "id_dsa",
    "id_ecdsa",
}

SENSITIVE_SUFFIXES = {
    ".pem",
    ".p12",
    ".pfx",
    ".keystore",
    ".wallet",
    ".dump",
}

# Pattern name → compiled regex. Values are never echoed.
CONTENT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("aws_access_key_id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("github_fine_grained_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("openai_secret_key", re.compile(r"sk-(?:proj-)?[A-Za-z0-9]{20,}")),
    ("anthropic_secret_key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("google_api_key", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("slack_webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/_-]{20,}")),
    (
        "password_bearing_db_url",
        re.compile(
            r"(?i)(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^/\s:]+:[^/\s@]+@"
        ),
    ),
    (
        "quoted_hex_private_key",
        re.compile(
            r"""(?i)(?:priv(?:ate)?[_-]?key|secret[_-]?key|wallet[_-]?key)\s*[:=]\s*['\"][0-9a-f]{64}['\"]"""
        ),
    ),
    (
        "literal_credential_assignment",
        re.compile(
            r"""(?i)(?:api[_-]?key|apikey|secret[_-]?key|private[_-]?key|access[_-]?token|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-/+=]{16,}['\"]"""
        ),
    ),
)

# Documentation and this scanner discuss secret *shapes*; do not treat those as leaks.
DOC_SKIP_PATTERNS = {
    "openai_secret_key",
    "anthropic_secret_key",
    "github_pat",
    "github_fine_grained_pat",
    "aws_access_key_id",
    "google_api_key",
    "slack_token",
    "slack_webhook",
    "literal_credential_assignment",
}

DOC_SUFFIXES = {".md", ".rst", ".txt"}


def repo_root_from(start: Path) -> Path:
    here = start.resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / ".git").exists():
            return candidate
    return here


def is_skipped_dir(path: Path) -> bool:
    return path.name in SKIP_DIR_NAMES


def relpath(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace(os.sep, "/")
    except ValueError:
        return str(path)


def is_sensitive_filename(path: Path) -> bool:
    name = path.name
    if name == ".env.example":
        return False
    if name in SENSITIVE_FILENAMES:
        return True
    if name.startswith(".env."):
        return True
    suffix = path.suffix.lower()
    if suffix == ".key" and name not in {".markdownlint.json"}:
        return True
    return suffix in SENSITIVE_SUFFIXES


def is_doc_path(path: Path) -> bool:
    return path.suffix.lower() in DOC_SUFFIXES


def should_scan_file(path: Path) -> bool:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    if path.name.startswith("."):
        # Hidden files can still hold secrets (.env is handled by filename rules).
        return True
    return True


def lookslike_text(data: bytes) -> bool:
    if b"\x00" in data[:8192]:
        return False
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def scan_file(root: Path, path: Path) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    display = relpath(root, path)
    if is_sensitive_filename(path):
        findings.append((display, 0, "sensitive_filename"))
        return findings
    if not should_scan_file(path):
        return findings
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {display}: {exc}", file=sys.stderr)
        return findings
    if not lookslike_text(raw):
        return findings
    text = raw.decode("utf-8")
    skip_named = is_doc_path(path) or path.name == "check_secrets.py"
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in CONTENT_PATTERNS:
            if skip_named and name in DOC_SKIP_PATTERNS:
                continue
            if pattern.search(line):
                findings.append((display, lineno, name))
    return findings


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            name for name in dirnames if not is_skipped_dir(Path(dirpath) / name)
        )
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            out.append(path)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Repository root to scan (default: detect from this file)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else repo_root_from(Path(__file__))
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    findings: list[tuple[str, int, str]] = []
    for path in iter_files(root):
        findings.extend(scan_file(root, path))

    if not findings:
        print("secret scan: no findings")
        return 0

    print("secret scan: findings (path / line / pattern — values omitted)")
    for path, line, name in findings:
        loc = f"{path}:{line}" if line else path
        print(f"  {loc}  [{name}]")
    print(f"secret scan: {len(findings)} finding(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
