"""Scanner unit tests — classification logic and auth header building."""

from __future__ import annotations

import pytest

from providers import Provider, Tier
from scanner import ImageScanner


@pytest.fixture
def scanner():
    return ImageScanner({"scan": {"concurrency": 1, "test_prompt": "a cat"}})


def test_classify_401_is_auth_failed(scanner):
    assert scanner._classify_error(401, "unauthorized") == "auth_failed"


def test_classify_402_is_needs_credits(scanner):
    assert scanner._classify_error(402, "payment required") == "needs_credits"


def test_classify_403_with_credit_keyword_is_needs_credits(scanner):
    assert scanner._classify_error(403, "out of credit") == "needs_credits"


def test_classify_403_without_credit_keyword_is_auth_failed(scanner):
    assert scanner._classify_error(403, "forbidden") == "auth_failed"


def test_classify_429_is_rate_limited(scanner):
    assert scanner._classify_error(429, "too many requests") == "rate_limited"


def test_classify_500_is_error(scanner):
    assert scanner._classify_error(500, "internal error") == "error"


def test_auth_headers_bearer_includes_token(scanner, monkeypatch):
    monkeypatch.setenv("FAKE_KEY", "test-token-123")
    provider = Provider(
        name="Fake", tier=Tier.free, endpoint="https://x/y",
        env_key="FAKE_KEY", auth_style="bearer",
    )
    headers = scanner._get_auth_headers(provider)
    assert headers["Authorization"] == "Bearer test-token-123"


def test_auth_headers_x_api_key(scanner, monkeypatch):
    monkeypatch.setenv("FAKE_KEY", "abc")
    provider = Provider(
        name="Fake", tier=Tier.free, endpoint="https://x/y",
        env_key="FAKE_KEY", auth_style="x-api-key",
    )
    headers = scanner._get_auth_headers(provider)
    assert headers["x-api-key"] == "abc"


def test_auth_headers_none_returns_empty(scanner):
    provider = Provider(
        name="Fake", tier=Tier.free, endpoint="https://x/y",
        env_key=None, auth_style="none",
    )
    assert scanner._get_auth_headers(provider) == {}
