"""Repository quality-gate contracts. Does not exercise historical bot behavior."""

from __future__ import annotations

import compileall
import re
import subprocess
import sys
from pathlib import Path

COMPILEALL_SKIP = re.compile(r"(.venv|venv|__pycache__|\.git)")


def test_python_sources_compile(repo_root: Path) -> None:
    ok = compileall.compile_dir(str(repo_root), quiet=1, rx=COMPILEALL_SKIP)
    assert ok is True


def test_pytest_ini_limits_collection_to_tests(repo_root: Path) -> None:
    text = (repo_root / "pytest.ini").read_text(encoding="utf-8")
    assert "testpaths = tests" in text
    assert re.search(r"(?m)^\s*bots\s*$", text)


def test_bots_tree_has_no_pytest_modules(repo_root: Path) -> None:
    named = [
        path
        for path in (repo_root / "bots").rglob("*.py")
        if path.name.startswith("test_") or path.name.endswith("_test.py")
    ]
    assert named == []


def test_pytest_collects_only_tests_directory(repo_root: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-p",
            "no:cacheprovider",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    assert completed.returncode == 0, output
    assert "bots/" not in completed.stdout
    assert "watchdog.py" not in completed.stdout
    assert "scripts/security/check_secrets.py" not in completed.stdout
