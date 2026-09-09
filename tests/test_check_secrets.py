"""Tests for the educational secret scanner. Never asserts or prints secret values."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType

import pytest

# Shapes that match CONTENT_PATTERNS. Used only in temp fixtures — never committed.
_PLANTED_ANTHROPIC = "sk-ant-" + ("A" * 24)
_PLANTED_OPENAI = "sk-proj-" + ("B" * 24)


def test_repository_scan_is_clean(
    check_secrets: ModuleType,
    repo_root: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = check_secrets.main([str(repo_root)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "no findings" in captured.out
    assert _PLANTED_ANTHROPIC not in captured.out
    assert _PLANTED_OPENAI not in captured.out


def test_env_example_filename_is_allowed(
    check_secrets: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / ".env.example").write_text("ALERT_PHONE=\n", encoding="utf-8")
    rc = check_secrets.main([str(tmp_path)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "no findings" in captured.out


def test_sensitive_filename_reported_without_file_contents(
    check_secrets: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    planted = _PLANTED_ANTHROPIC
    (tmp_path / ".env").write_text(f"KEY={planted}\n", encoding="utf-8")
    rc = check_secrets.main([str(tmp_path)])
    captured = capsys.readouterr()
    assert rc == 1
    assert planted not in captured.out
    assert planted not in captured.err
    assert "sensitive_filename" in captured.out


def test_content_pattern_reported_without_echoing_value(
    check_secrets: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    planted = _PLANTED_OPENAI
    (tmp_path / "leak.py").write_text(f"token = '{planted}'\n", encoding="utf-8")
    rc = check_secrets.main([str(tmp_path)])
    captured = capsys.readouterr()
    assert rc == 1
    assert planted not in captured.out
    assert planted not in captured.err
    assert "openai_secret_key" in captured.out


def test_markdown_skips_documented_key_shapes(
    check_secrets: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    planted = _PLANTED_ANTHROPIC
    (tmp_path / "note.md").write_text(f"Example shape only: {planted}\n", encoding="utf-8")
    rc = check_secrets.main([str(tmp_path)])
    captured = capsys.readouterr()
    assert rc == 0
    assert planted not in captured.out
    assert "no findings" in captured.out
