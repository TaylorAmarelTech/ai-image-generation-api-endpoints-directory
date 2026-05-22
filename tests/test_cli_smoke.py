"""CLI smoke tests — invoke the entry point and assert it succeeds offline."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "main.py"), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
    )


def test_version_command():
    result = _run("version")
    assert result.returncode == 0
    assert "0." in result.stdout


def test_help_command():
    result = _run("--help")
    assert result.returncode == 0
    assert "discover" in result.stdout
    assert "benchmark" in result.stdout
    assert "costs" in result.stdout


def test_list_json_output_is_valid():
    result = _run("list", "--tier", "free", "--format", "json")
    assert result.returncode == 0
    assert "HuggingFace" in result.stdout


def test_costs_command_runs():
    result = _run("costs", "--sort", "price")
    assert result.returncode == 0
    assert "Per-Image Pricing" in result.stdout or "$" in result.stdout


def test_export_json_output(tmp_path):
    out = tmp_path / "out.json"
    result = _run("export", "--format", "json", "--output", str(out))
    assert result.returncode == 0
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) >= 40
    assert all("name" in p for p in data)
