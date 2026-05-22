"""Discovery module unit tests (no network)."""

from __future__ import annotations

from discovery import CANDIDATES, _registered_hosts, unregistered_candidates


def test_candidates_have_required_fields():
    assert CANDIDATES
    for c in CANDIDATES:
        assert c.host
        assert c.url.startswith("https://")


def test_registered_hosts_returns_non_empty_set():
    hosts = _registered_hosts()
    assert isinstance(hosts, set)
    assert len(hosts) >= 30


def test_unregistered_candidates_excludes_known_hosts():
    known = _registered_hosts()
    candidate_hosts = {c.url.split("/")[2] for c in unregistered_candidates()}
    overlap = candidate_hosts & known
    assert not overlap, f"Candidates should not duplicate registered hosts: {overlap}"
