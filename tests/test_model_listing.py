"""Model listing module tests (no network — exercises helpers + offline fallback)."""

from __future__ import annotations

from providers import Provider, Tier
from model_listing import _models_endpoint, _auth_headers


def test_models_endpoint_for_openai_compatible():
    p = Provider(
        name="Together",
        tier=Tier.free,
        endpoint="https://api.together.xyz/v1/images/generations",
        openai_compatible=True,
    )
    assert _models_endpoint(p) == "https://api.together.xyz/v1/models"


def test_models_endpoint_returns_none_for_non_openai_compatible():
    p = Provider(
        name="Discord",
        tier=Tier.freemium,
        endpoint="(Discord-based)",
        openai_compatible=False,
    )
    assert _models_endpoint(p) is None


def test_models_endpoint_handles_paths_without_v1():
    p = Provider(
        name="Custom",
        tier=Tier.free,
        endpoint="https://example.com/openai/images/generations",
        openai_compatible=True,
    )
    result = _models_endpoint(p)
    assert result is not None
    assert "/v1/models" in result


def test_auth_headers_empty_when_key_not_set(monkeypatch):
    monkeypatch.delenv("MISSING_KEY", raising=False)
    p = Provider(
        name="X", tier=Tier.free, endpoint="https://x/y",
        env_key="MISSING_KEY", auth_style="bearer",
    )
    assert _auth_headers(p) == {}


def test_auth_headers_bearer_when_key_set(monkeypatch):
    monkeypatch.setenv("PRESENT_KEY", "abc")
    p = Provider(
        name="X", tier=Tier.free, endpoint="https://x/y",
        env_key="PRESENT_KEY", auth_style="bearer",
    )
    assert _auth_headers(p)["Authorization"] == "Bearer abc"
