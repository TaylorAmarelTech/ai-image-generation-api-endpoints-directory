"""Minimal OpenAI-compatible image-generation proxy with fallback.

POST /v1/images/generations  -> fans the request out to the configured
provider cascade. If the primary provider fails, the proxy tries the next
provider in the cascade until one succeeds or the list is exhausted.

The server uses Python's stdlib http.server so it stays dependency-free.
For production use, swap in a real ASGI server.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterable
from urllib.parse import urlparse

import httpx

from providers import Provider, PROVIDERS, Tier


def _cascade(providers: Iterable[Provider]) -> list[Provider]:
    """Filter to providers that can be used without manual config."""
    usable: list[Provider] = []
    for p in providers:
        if not p.openai_compatible:
            continue
        if p.auth_style in ("none", "url"):
            usable.append(p)
            continue
        if p.env_key and os.environ.get(p.env_key):
            usable.append(p)
    return usable


def _auth_headers(provider: Provider) -> dict[str, str]:
    headers: dict[str, str] = {"Content-Type": "application/json"}
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


def build_handler(
    cascade: list[Provider],
    request_timeout: float = 120.0,
):
    """Return a request handler class bound to the given cascade."""

    class ProxyHandler(BaseHTTPRequestHandler):
        server_version = "ai-image-proxy/0.1"

        def log_message(self, fmt: str, *args) -> None:  # noqa: ANN001
            print(f"[proxy] {self.address_string()} - {fmt % args}")

        def _send_json(self, status: int, body: dict) -> None:
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path in ("/health", "/healthz"):
                self._send_json(200, {
                    "status": "ok",
                    "cascade": [p.name for p in cascade],
                })
                return
            if parsed.path == "/v1/models":
                models_out: list[dict] = []
                for p in cascade:
                    model_ids = p.models or ([p.test_model] if p.test_model else ["default"])
                    for model in model_ids:
                        models_out.append({
                            "id": model,
                            "owned_by": p.name,
                            "object": "model",
                        })
                self._send_json(200, {"object": "list", "data": models_out})
                return
            self._send_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path != "/v1/images/generations":
                self._send_json(404, {"error": {"message": "Not found"}})
                return

            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                payload = json.loads(raw or b"{}")
            except json.JSONDecodeError:
                self._send_json(400, {"error": {"message": "Invalid JSON"}})
                return

            if not isinstance(payload, dict) or "prompt" not in payload:
                self._send_json(400, {"error": {"message": "Missing 'prompt'"}})
                return

            requested_model = payload.get("model")
            errors: list[dict] = []

            for provider in cascade:
                if requested_model and provider.models and requested_model not in provider.models:
                    continue

                outbound = dict(payload)
                if provider.test_model and "model" not in outbound:
                    outbound["model"] = provider.test_model

                try:
                    with httpx.Client(timeout=request_timeout, follow_redirects=True) as client:
                        resp = client.post(
                            provider.endpoint,
                            json=outbound,
                            headers=_auth_headers(provider),
                        )
                except (httpx.TimeoutException, httpx.ConnectError) as exc:
                    errors.append({"provider": provider.name, "error": str(exc)[:200]})
                    continue
                except httpx.HTTPError as exc:
                    errors.append({"provider": provider.name, "error": str(exc)[:200]})
                    continue

                if resp.status_code == 200:
                    try:
                        body = resp.json()
                    except ValueError:
                        body = {"raw": resp.text[:500]}
                    if isinstance(body, dict):
                        body.setdefault("_proxy", {})["provider"] = provider.name
                    self._send_json(200, body)
                    return

                errors.append({
                    "provider": provider.name,
                    "status": resp.status_code,
                    "error": resp.text[:300],
                })

            self._send_json(502, {
                "error": {"message": "All providers in cascade failed"},
                "attempts": errors,
            })

    return ProxyHandler


def serve(
    port: int = 8000,
    cascade: list[Provider] | None = None,
    host: str = "127.0.0.1",
) -> None:
    """Run the proxy until interrupted."""
    if cascade is None:
        ordered = (
            [p for p in PROVIDERS if p.tier == Tier.free]
            + [p for p in PROVIDERS if p.tier == Tier.generous_free]
            + [p for p in PROVIDERS if p.tier == Tier.free_credits]
            + [p for p in PROVIDERS if p.tier == Tier.router]
        )
        cascade = _cascade(ordered)

    if not cascade:
        raise SystemExit(
            "No usable providers found. Set at least one API key or include "
            "an auth-free provider in the cascade."
        )

    handler_cls = build_handler(cascade)
    server = ThreadingHTTPServer((host, port), handler_cls)
    print(f"[proxy] Serving OpenAI-compatible image proxy at http://{host}:{port}")
    print(f"[proxy] Cascade order: {', '.join(p.name for p in cascade)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[proxy] Shutting down")
    finally:
        server.server_close()
