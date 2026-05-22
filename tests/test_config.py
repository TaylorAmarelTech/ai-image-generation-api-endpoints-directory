"""Config loader tests."""

from __future__ import annotations

from config import load_config, _deep_merge, _deep_copy


def test_defaults_loaded_when_no_yaml(tmp_path):
    config = load_config(config_path=str(tmp_path / "missing.yaml"))
    assert "scan" in config
    assert config["scan"]["concurrency"] >= 1
    assert config["report"]["output_file"] == "README.md"


def test_deep_merge_overrides_leaf_values():
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    override = {"b": {"c": 99}}
    result = _deep_merge(base, override)
    assert result == {"a": 1, "b": {"c": 99, "d": 3}}
    assert base == {"a": 1, "b": {"c": 2, "d": 3}}


def test_deep_copy_does_not_alias_nested_lists():
    src = {"q": [1, 2, 3]}
    dup = _deep_copy(src)
    dup["q"].append(4)
    assert src["q"] == [1, 2, 3]


def test_env_var_override(monkeypatch):
    monkeypatch.setenv("SCAN_CONCURRENCY", "42")
    config = load_config()
    assert config["scan"]["concurrency"] == 42


def test_skip_local_env_override(monkeypatch):
    monkeypatch.setenv("SCAN_SKIP_LOCAL", "true")
    config = load_config()
    assert config["scan"]["skip_local"] is True
