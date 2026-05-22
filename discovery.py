"""Provider discovery — probe candidate endpoints for unregistered providers.

Discovery is intentionally heuristic. It probes a curated list of well-known
URL shapes (``api.{host}/v1/images/generations``, etc.) that aren't yet in the
PROVIDERS registry and reports which ones look reachable. The goal is to give
maintainers a short candidate list to investigate manually.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from providers import PROVIDERS


@dataclass(frozen=True)
class Candidate:
    """A potential new image-generation provider."""

    host: str
    url: str
    notes: str = ""


@dataclass
class DiscoveryResult:
    """Outcome of probing a single candidate."""

    candidate: Candidate
    reachable: bool
    status_code: int | None
    auth_required: bool
    looks_like_images_api: bool
    detail: str = ""


CANDIDATES: list[Candidate] = [
    Candidate("recraft.ai", "https://external.api.recraft.ai/v1/images/generations", "Vector + raster"),
    Candidate("xai-grok", "https://api.x.ai/v1/images/generations", "Grok image generation"),
    Candidate("vivago", "https://api.vivago.ai/v1/images/generations", "Vivago AI"),
    Candidate("blockadelabs", "https://backend.blockadelabs.com/api/v1/skybox", "360 deg skyboxes"),
    Candidate("luma", "https://api.lumalabs.ai/dream-machine/v1/generations/image", "Photon image API"),
    Candidate("freepik", "https://api.freepik.com/v1/ai/text-to-image", "Freepik AI"),
    Candidate("scenario", "https://api.cloud.scenario.com/v1/generate/txt2img", "Game-asset focused"),
    Candidate("openart", "https://openart.ai/api/v1/generate", "OpenArt API"),
    Candidate("magai", "https://api.magai.co/v1/images/generations", "Magai"),
    Candidate("kling", "https://api.klingai.com/v1/images/generations", "Kling image+video"),
    Candidate("aliyun-wanx", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis", "Wanx / Tongyi"),
    Candidate("baidu-ernie", "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image", "ERNIE-ViLG"),
    Candidate("yandex", "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync", "Yandex YandexART"),
    Candidate("decohere", "https://api.decohere.ai/v1/images/generations", "Decohere"),
    Candidate("getexpression", "https://api.getexpression.ai/v1/images", "Expression AI"),
]


def _registered_hosts() -> set[str]:
    """Return the set of hostnames already present in PROVIDERS."""
    hosts: set[str] = set()
    for p in PROVIDERS:
        if not p.endpoint or "localhost" in p.endpoint:
            continue
        host = urlparse(p.endpoint).netloc
        if host:
            hosts.add(host)
    return hosts


def unregistered_candidates() -> list[Candidate]:
    """Candidates whose host is not yet present in PROVIDERS."""
    known = _registered_hosts()
    return [c for c in CANDIDATES if urlparse(c.url).netloc not in known]


async def probe(
    candidate: Candidate,
    client: httpx.AsyncClient,
    timeout: float = 8.0,
) -> DiscoveryResult:
    """Send a lightweight probe to *candidate* and classify the response."""
    try:
        resp = await client.head(
            candidate.url, follow_redirects=True, timeout=timeout,
        )
    except httpx.TimeoutException:
        return DiscoveryResult(candidate, False, None, False, False, "timeout")
    except httpx.ConnectError as exc:
        return DiscoveryResult(candidate, False, None, False, False, f"connect: {exc}")
    except httpx.HTTPError as exc:
        return DiscoveryResult(candidate, False, None, False, False, str(exc)[:120])

    code = resp.status_code
    reachable = code < 500
    auth_required = code in (401, 403)
    looks_like_images_api = code in (401, 403, 405, 200, 204)

    detail = ""
    headers_lower = {k.lower() for k in resp.headers}
    if "www-authenticate" in headers_lower:
        detail = "auth challenge present"

    return DiscoveryResult(
        candidate, reachable, code, auth_required, looks_like_images_api, detail,
    )


async def run_discovery(
    candidates: list[Candidate] | None = None,
    concurrency: int = 8,
    timeout: float = 8.0,
) -> list[DiscoveryResult]:
    """Probe every candidate concurrently."""
    targets = candidates if candidates is not None else unregistered_candidates()
    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient() as client:

        async def _guarded(c: Candidate) -> DiscoveryResult:
            async with sem:
                return await probe(c, client, timeout=timeout)

        tasks = [asyncio.create_task(_guarded(c)) for c in targets]
        return list(await asyncio.gather(*tasks))
