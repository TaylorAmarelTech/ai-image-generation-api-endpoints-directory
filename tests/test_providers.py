"""Provider registry integrity tests."""

from __future__ import annotations

import pytest

from providers import PROVIDERS, Tier, get_providers, get_provider


def test_provider_registry_not_empty():
    assert len(PROVIDERS) >= 40


def test_every_provider_has_name_and_endpoint():
    for p in PROVIDERS:
        assert p.name, "Provider name is empty"
        assert p.endpoint, f"{p.name} has no endpoint"


def test_provider_names_are_unique():
    names = [p.name for p in PROVIDERS]
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"Duplicate provider names: {duplicates}"


@pytest.mark.parametrize("tier", list(Tier))
def test_tier_filter_returns_only_matching_tier(tier):
    matches = get_providers(tier=tier)
    for p in matches:
        assert p.tier == tier


def test_get_provider_case_insensitive():
    expected = PROVIDERS[0]
    found = get_provider(expected.name.lower())
    assert found is not None
    assert found.name == expected.name


def test_get_provider_returns_none_for_unknown():
    assert get_provider("nonexistent-provider-xyz") is None


def test_local_providers_use_localhost():
    locals_ = [p for p in PROVIDERS if p.tier == Tier.local]
    assert locals_, "Expected at least one local provider"
    for p in locals_:
        assert "localhost" in p.endpoint or p.endpoint.startswith("http://127.")


def test_openai_compatible_providers_have_models_or_test_model():
    for p in PROVIDERS:
        if p.openai_compatible and p.tier != Tier.router:
            assert p.test_model or p.models, (
                f"{p.name} is openai_compatible but has no models or test_model"
            )
