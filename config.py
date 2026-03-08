"""Configuration loader for the AI Image Generation API Directory."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


# Project root directory
ROOT_DIR = Path(__file__).parent

# Default configuration
DEFAULTS = {
    "scan": {
        "concurrency": 5,
        "timeout_seconds": 60,
        "test_prompt": "A red circle on a white background",
        "test_resolution": "256x256",
        "retry_count": 1,
        "skip_local": False,
    },
    "search": {
        "max_results_per_query": 10,
        "search_queries": [
            "free AI image generation API 2026",
            "free text to image API no credit card",
        ],
    },
    "discovery": {
        "enabled": True,
        "strategies": ["web_search", "github_search", "llm_search"],
        "llm_provider": "groq",
        "llm_model": "llama-3.3-70b-versatile",
    },
    "plugins": {
        "enabled_plugins": ["benchmark", "model_list", "export"],
    },
    "report": {
        "output_file": "README.md",
    },
    "proxy": {
        "port": 8000,
        "default_provider": "huggingface",
    },
}


def load_config(config_path: str | None = None) -> dict:
    """Load configuration from YAML file with env overrides."""
    # Load .env file
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # Start with defaults
    config = _deep_copy(DEFAULTS)

    # Load YAML config
    yaml_path = Path(config_path) if config_path else ROOT_DIR / "config.yaml"
    if yaml_path.exists():
        with open(yaml_path) as f:
            yaml_config = yaml.safe_load(f) or {}
        config = _deep_merge(config, yaml_config)

    # Apply environment variable overrides
    _apply_env_overrides(config)

    return config


def _deep_copy(d: dict) -> dict:
    """Deep copy a nested dict."""
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = _deep_copy(v)
        elif isinstance(v, list):
            result[k] = v[:]
        else:
            result[k] = v
    return result


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base."""
    result = _deep_copy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _apply_env_overrides(config: dict) -> None:
    """Apply environment variable overrides to config."""
    env_map = {
        "SCAN_CONCURRENCY": ("scan", "concurrency", int),
        "SCAN_TIMEOUT": ("scan", "timeout_seconds", int),
        "SCAN_TEST_PROMPT": ("scan", "test_prompt", str),
        "SCAN_SKIP_LOCAL": ("scan", "skip_local", lambda x: x.lower() in ("true", "1", "yes")),
        "REPORT_OUTPUT": ("report", "output_file", str),
        "PROXY_PORT": ("proxy", "port", int),
    }
    for env_var, (section, key, converter) in env_map.items():
        value = os.environ.get(env_var)
        if value is not None:
            config[section][key] = converter(value)
