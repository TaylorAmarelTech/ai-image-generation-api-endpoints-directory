"""Fetch model lists from image-generation providers.

OpenAI-compatible providers expose ``/v1/models``. For everything else we fall
back to the static list declared in ``providers.py``.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from providers import Provider, PROVIDERS


@dataclass(frozen=True)
class ModelListing:
    """Resolved model list for a single provider."""

    provider_name: str
    models: list[str]
    source: str          # "live", "static", "auth_missing", "error"
    error_detail: str = ""


def _models_endpoint(provider: Provider) -> str | None:
    """Derive the ``/v1/models`` URL for an OpenAI-compatible provider."""
    if not provider.openai_compatible or not provider.endpoint:
        return None
    parsed = urlparse(provider.endpoint)
    if not parsed.scheme or not parsed.netloc:
        return None
    path = parsed.path
    if "/v1/" in path:
        v1_base = path[: path.index("/v1/") + len("/v1")]
    elif path.endswith("/v1"):
        v1_base = path
    else:
        v1_base = "/v1"
    return f"{parsed.scheme}://{parsed.netloc}{v1_base}/models"


def _auth_headers(provider: Provider) -> dict[str, str]:
    headers: dict[str, str] = {}
    if provider.auth_style in ("none", "url") or not provider.env_key:
        return headers
    api_key = os.environ.get(provider.env_key, "")
    if not api_key:
        return headers
    if provider.auth_style == "bearer":
        headers["Authorization"] = f"Bearer {api_key}"
    elif provider.auth_style == "x-api-key":
        headers["x-api-key"] = api_key
    elif provider.auth_style == "api-key":
        headers["api-key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


async def fetch_models(
    provider: Provider,
    client: httpx.AsyncClient,
    timeout: float = 15.0,
) -> ModelListing:
    """Fetch live model list for one provider, with graceful fallback."""
    endpoint = _models_endpoint(provider)
    if endpoint is None:
        return ModelListing(provider.name, list(provider.models), "static")

    if provider.auth_style not in ("none", "url") and provider.env_key:
        if not os.environ.get(provider.env_key):
            return ModelListing(
                provider.name,
                list(provider.models),
                "auth_missing",
            )

    headers = _auth_headers(provider)
    try:
        resp = await client.get(endpoint, headers=headers, timeout=timeout)
    except (httpx.TimeoutException, httpx.ConnectError) as exc:
        return ModelListing(
            provider.name,
            list(provider.models),
            "error",
            error_detail=str(exc)[:200],
        )

    if resp.status_code != 200:
        return ModelListing(
            provider.name,
            list(provider.models),
            "error",
            error_detail=f"HTTP {resp.status_code}",
        )

    try:
        body = resp.json()
    except ValueError:
        return ModelListing(
            provider.name,
            list(provider.models),
            "error",
            error_detail="Non-JSON response",
        )

    models: list[str] = []
    data = body.get("data") if isinstance(body, dict) else None
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                model_id = entry.get("id") or entry.get("name")
                if isinstance(model_id, str):
                    models.append(model_id)
            elif isinstance(entry, str):
                models.append(entry)

    if not models:
        return ModelListing(
            provider.name,
            list(provider.models),
            "static",
            error_detail="No models in response",
        )

    image_models = [
        m for m in models
        if any(token in m.lower() for token in (
            "flux", "sdxl", "stable-diffusion", "image",
            "dall-e", "dalle", "imagen", "kolors", "midjourney",
            "playground", "ideogram",
        ))
    ]
    return ModelListing(
        provider.name,
        image_models or models[:20],
        "live",
    )


async def fetch_all_models(
    providers: list[Provider] | None = None,
    concurrency: int = 8,
    timeout: float = 15.0,
) -> list[ModelListing]:
    """Fetch model listings for every provider in parallel."""
    targets = providers if providers is not None else list(PROVIDERS)
    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(follow_redirects=True) as client:

        async def _guarded(p: Provider) -> ModelListing:
            async with sem:
                return await fetch_models(p, client, timeout=timeout)

        tasks = [asyncio.create_task(_guarded(p)) for p in targets]
        return list(await asyncio.gather(*tasks))
