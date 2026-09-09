"""Fixtures for quality-infrastructure tests. Not a trading or strategy suite."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = REPO_ROOT / "scripts" / "security" / "check_secrets.py"


def _load_scanner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_secrets", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCANNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def check_secrets() -> ModuleType:
    return _load_scanner()
