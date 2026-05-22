"""Pricing module tests."""

from __future__ import annotations

import pytest

from providers import PROVIDERS
from pricing import (
    PRICING,
    all_pricing_sorted,
    coverage_check,
    estimate_monthly_cost,
    get_pricing,
)


def test_pricing_covers_every_provider():
    missing = coverage_check()
    assert not missing, f"Providers missing from PRICING: {missing}"


def test_get_pricing_by_name():
    p = get_pricing("OpenAI (DALL-E)")
    assert p is not None
    assert p.provider_name == "OpenAI (DALL-E)"
    assert p.usd_per_image > 0


def test_get_pricing_by_provider_instance():
    sample = PROVIDERS[0]
    result = get_pricing(sample)
    assert result is not None
    assert result.provider_name == sample.name


def test_estimate_monthly_cost_subtracts_free_allotment():
    cost = estimate_monthly_cost("OpenAI (DALL-E)", 1000)
    assert cost == pytest.approx(875 * 0.04, abs=0.01)


def test_estimate_monthly_cost_zero_when_below_free_tier():
    cost = estimate_monthly_cost("Cloudflare Workers AI", 5000)
    assert cost == 0


def test_estimate_monthly_cost_none_for_non_comparable():
    assert estimate_monthly_cost("Midjourney", 1000) is None


def test_all_pricing_sorted_ascending_by_default():
    items = all_pricing_sorted()
    for i in range(1, len(items)):
        assert items[i].usd_per_image >= items[i - 1].usd_per_image


def test_all_pricing_excludes_unknown_by_default():
    items = all_pricing_sorted()
    for p in items:
        assert p.usd_per_image >= 0


def test_all_pricing_includes_unknown_when_requested():
    items = all_pricing_sorted(include_unknown=True)
    assert any(p.usd_per_image < 0 for p in items)


def test_cost_per_1000_property():
    p = PRICING["OpenAI (DALL-E)"]
    assert p.cost_per_1000 == pytest.approx(p.usd_per_image * 1000)
