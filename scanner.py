"""Async image endpoint scanner.

Probes image-generation providers concurrently and reports their status,
latency, and capabilities.
"""

from __future__ import annotations

import asyncio
import os
import time
import urllib.parse
from dataclasses import dataclass, field

import httpx

from providers import Provider, Tier, PROVIDERS, get_providers, get_provider
from config import load_config


# ---------------------------------------------------------------------------
# Scan result
# ---------------------------------------------------------------------------

@dataclass
class ScanResult:
    provider_name: str
    status: str  # working, reachable, auth_missing, auth_failed, needs_credits,
                 # rate_limited, timeout, error, offline, skipped
    latency_ms: float | None = None
    error_detail: str = ""
    model_used: str = ""
    image_url: str = ""
    generation_time_ms: float | None = None
    resolution: str = ""


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

class ImageScanner:
    """Scan image-generation providers for availability and performance."""

    def __init__(self, config: dict) -> None:
        self.config = config
        scan_cfg = config.get("scan", {})
        self._timeout = httpx.Timeout(
            connect=scan_cfg.get("connect_timeout", 10.0),
            read=scan_cfg.get("read_timeout", 60.0),
            write=scan_cfg.get("write_timeout", 10.0),
            pool=scan_cfg.get("pool_timeout", 10.0),
        )
        self._client = httpx.AsyncClient(
            timeout=self._timeout,
            follow_redirects=True,
        )
        self._semaphore = asyncio.Semaphore(
            scan_cfg.get("concurrency", 8)
        )

    # -- async context manager ----------------------------------------------

    async def __aenter__(self) -> "ImageScanner":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        await self._client.aclose()

    # -- public API ---------------------------------------------------------

    async def scan_all(
        self,
        tier: Tier | None = None,
        provider_name: str | None = None,
    ) -> list[ScanResult]:
        """Scan providers concurrently and return a list of results.

        Parameters
        ----------
        tier:
            If given, only scan providers belonging to this tier.
        provider_name:
            If given, only scan the single provider with this name.
        """
        if provider_name is not None:
            provider = get_provider(provider_name)
            if provider is None:
                return [
                    ScanResult(
                        provider_name=provider_name,
                        status="error",
                        error_detail=f"Unknown provider: {provider_name}",
                    )
                ]
            providers = [provider]
        else:
            providers = get_providers(tier=tier)

        async def _guarded(p: Provider) -> ScanResult:
            async with self._semaphore:
                return await self.scan_provider(p)

        tasks = [asyncio.create_task(_guarded(p)) for p in providers]
        return list(await asyncio.gather(*tasks))

    async def scan_provider(self, provider: Provider) -> ScanResult:
        """Dispatch to the correct test method for *provider*."""
        # --- auth gate -----------------------------------------------------
        if provider.auth_style not in ("none", "url"):
            env_key = getattr(provider, "env_key", None)
            if env_key and not os.environ.get(env_key):
                return ScanResult(
                    provider_name=provider.name,
                    status="auth_missing",
                    error_detail=f"Environment variable {env_key} is not set",
                )

        # --- local reachability check --------------------------------------
        if provider.tier == Tier.local:
            try:
                t0 = time.monotonic()
                resp = await self._client.head(provider.endpoint)
                latency = (time.monotonic() - t0) * 1000
            except (httpx.ConnectError, httpx.TimeoutException):
                return ScanResult(
                    provider_name=provider.name,
                    status="offline",
                    error_detail="Local provider is not reachable",
                )

        # --- dispatch based on provider traits -----------------------------
        try:
            if getattr(provider, "openai_compatible", False):
                return await self._test_openai_compatible(provider)
            if getattr(provider, "a1111_compatible", False):
                return await self._test_a1111_compatible(provider)
            if provider.auth_style in ("none", "url"):
                return await self._test_url_based(provider)
            return await self._test_rest_api(provider)

        except httpx.TimeoutException:
            return ScanResult(
                provider_name=provider.name,
                status="timeout",
                error_detail="Request timed out",
            )
        except httpx.ConnectError:
            status = "offline" if provider.tier == Tier.local else "error"
            return ScanResult(
                provider_name=provider.name,
                status=status,
                error_detail="Connection refused or unreachable",
            )
        except Exception as exc:  # noqa: BLE001
            return ScanResult(
                provider_name=provider.name,
                status="error",
                error_detail=str(exc),
            )

    # -- provider-specific test methods -------------------------------------

    async def _test_openai_compatible(self, provider: Provider) -> ScanResult:
        """Test an OpenAI-style ``/v1/images/generations`` endpoint."""
        scan_cfg = self.config.get("scan", {})
        payload = {
            "model": provider.test_model,
            "prompt": scan_cfg.get("test_prompt", "a white cat"),
            "n": 1,
            "size": scan_cfg.get("test_resolution", "256x256"),
            "response_format": "url",
        }
        headers = self._get_auth_headers(provider)

        t0 = time.monotonic()
        resp = await self._client.post(
            provider.endpoint, json=payload, headers=headers,
        )
        latency = (time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            return ScanResult(
                provider_name=provider.name,
                status=self._classify_error(resp.status_code, resp.text),
                latency_ms=latency,
                error_detail=resp.text[:500],
                model_used=provider.test_model,
            )

        body = resp.json()
        image_url = ""
        if "data" in body and body["data"]:
            image_url = body["data"][0].get("url", "")

        return ScanResult(
            provider_name=provider.name,
            status="working",
            latency_ms=latency,
            model_used=provider.test_model,
            image_url=image_url,
            generation_time_ms=latency,
            resolution=scan_cfg.get("test_resolution", "256x256"),
        )

    async def _test_a1111_compatible(self, provider: Provider) -> ScanResult:
        """Test an Automatic1111 ``/sdapi/v1/txt2img`` endpoint."""
        scan_cfg = self.config.get("scan", {})
        endpoint = provider.endpoint.rstrip("/")
        if not endpoint.endswith("/sdapi/v1/txt2img"):
            endpoint = f"{endpoint}/sdapi/v1/txt2img"

        payload = {
            "prompt": scan_cfg.get("test_prompt", "a white cat"),
            "steps": 5,
            "width": 256,
            "height": 256,
            "batch_size": 1,
        }
        headers = self._get_auth_headers(provider)

        t0 = time.monotonic()
        resp = await self._client.post(
            endpoint, json=payload, headers=headers,
        )
        latency = (time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            return ScanResult(
                provider_name=provider.name,
                status=self._classify_error(resp.status_code, resp.text),
                latency_ms=latency,
                error_detail=resp.text[:500],
                model_used=getattr(provider, "test_model", ""),
            )

        body = resp.json()
        return ScanResult(
            provider_name=provider.name,
            status="working",
            latency_ms=latency,
            model_used=getattr(provider, "test_model", ""),
            generation_time_ms=latency,
            resolution="256x256",
        )

    async def _test_url_based(self, provider: Provider) -> ScanResult:
        """Test a URL-based API like Pollinations (GET, check Content-Type)."""
        scan_cfg = self.config.get("scan", {})
        prompt = scan_cfg.get("test_prompt", "a white cat")
        encoded_prompt = urllib.parse.quote(prompt, safe="")

        # Build the URL — replace a {prompt} placeholder if present, otherwise
        # append the prompt to the endpoint path.
        endpoint = provider.endpoint.rstrip("/")
        if "{prompt}" in endpoint:
            url = endpoint.replace("{prompt}", encoded_prompt)
        else:
            url = f"{endpoint}/{encoded_prompt}"

        t0 = time.monotonic()
        resp = await self._client.get(url)
        latency = (time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            return ScanResult(
                provider_name=provider.name,
                status=self._classify_error(resp.status_code, resp.text),
                latency_ms=latency,
                error_detail=resp.text[:500],
            )

        content_type = resp.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return ScanResult(
                provider_name=provider.name,
                status="error",
                latency_ms=latency,
                error_detail=f"Unexpected Content-Type: {content_type}",
            )

        return ScanResult(
            provider_name=provider.name,
            status="working",
            latency_ms=latency,
            image_url=str(resp.url),
            generation_time_ms=latency,
        )

    async def _test_rest_api(self, provider: Provider) -> ScanResult:
        """Test a generic REST API via POST with the prompt in the body."""
        scan_cfg = self.config.get("scan", {})
        payload = {
            "prompt": scan_cfg.get("test_prompt", "a white cat"),
        }
        # Include the model if the provider specifies one.
        test_model = getattr(provider, "test_model", None)
        if test_model:
            payload["model"] = test_model

        headers = self._get_auth_headers(provider)

        t0 = time.monotonic()
        resp = await self._client.post(
            provider.endpoint, json=payload, headers=headers,
        )
        latency = (time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            return ScanResult(
                provider_name=provider.name,
                status=self._classify_error(resp.status_code, resp.text),
                latency_ms=latency,
                error_detail=resp.text[:500],
                model_used=test_model or "",
            )

        return ScanResult(
            provider_name=provider.name,
            status="working",
            latency_ms=latency,
            model_used=test_model or "",
            generation_time_ms=latency,
        )

    # -- helpers ------------------------------------------------------------

    def _get_auth_headers(self, provider: Provider) -> dict:
        """Build authentication headers for *provider*."""
        headers: dict[str, str] = {}
        auth_style = getattr(provider, "auth_style", "none")
        env_key = getattr(provider, "env_key", None)

        if auth_style == "none" or auth_style == "url" or not env_key:
            return headers

        api_key = os.environ.get(env_key, "")

        if auth_style == "bearer":
            headers["Authorization"] = f"Bearer {api_key}"
        elif auth_style == "x-api-key":
            headers["x-api-key"] = api_key
        elif auth_style == "api-key":
            headers["api-key"] = api_key
        elif auth_style == "basic":
            import base64
            encoded = base64.b64encode(f":{api_key}".encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        else:
            # Fall back to Bearer for unknown styles.
            headers["Authorization"] = f"Bearer {api_key}"

        return headers

    def _classify_error(self, status_code: int, response_text: str) -> str:
        """Map an HTTP status code (and optional body) to a scan status."""
        if status_code == 401:
            return "auth_failed"
        if status_code == 403:
            # Could be auth or payment-related.
            lower = response_text.lower()
            if "credit" in lower or "balance" in lower or "quota" in lower:
                return "needs_credits"
            return "auth_failed"
        if status_code == 402:
            return "needs_credits"
        if status_code == 429:
            return "rate_limited"
        if status_code == 408:
            return "timeout"
        if status_code >= 500:
            return "error"
        return "error"


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

async def run_scan(
    config: dict,
    tier: Tier | None = None,
    provider_name: str | None = None,
) -> list[ScanResult]:
    """Convenience function to run a scan."""
    async with ImageScanner(config) as scanner:
        return await scanner.scan_all(tier=tier, provider_name=provider_name)
