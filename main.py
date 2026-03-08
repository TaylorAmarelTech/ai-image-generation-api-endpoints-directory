"""CLI entry point for the AI Image Generation API Directory.

Provides 13 subcommands for scanning, listing, exporting, generating
images, and more.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import dataclasses
import json
import os
import sys
from pathlib import Path

import httpx
from rich.console import Console
from rich.table import Table

from providers import Tier, PROVIDERS, get_providers, get_provider
from scanner import run_scan, ScanResult
from config import load_config
from report_generator import generate_report
from __version__ import __version__

console = Console()

# ---------------------------------------------------------------------------
# Status colour mapping (for rich markup)
# ---------------------------------------------------------------------------

STATUS_STYLES = {
    "working": "bold green",
    "reachable": "yellow",
    "auth_missing": "blue",
    "auth_failed": "red",
    "needs_credits": "magenta",
    "rate_limited": "yellow",
    "timeout": "dark_orange",
    "error": "red",
    "offline": "dim red",
    "skipped": "dim",
    "unknown": "dim",
}

# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def cmd_scan(args: argparse.Namespace) -> None:
    """Test all image endpoints."""
    config = load_config()
    tier = Tier(args.tier) if args.tier else None
    provider_name = args.provider if args.provider else None

    console.print("\n[bold cyan]Scanning image endpoints...[/bold cyan]\n")
    results: list[ScanResult] = asyncio.run(
        run_scan(config, tier=tier, provider_name=provider_name)
    )

    # Display results table
    table = Table(title="Scan Results", show_lines=True)
    table.add_column("Provider", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Latency", justify="right")
    table.add_column("Model")
    table.add_column("Error")

    for r in results:
        style = STATUS_STYLES.get(r.status, "")
        status_cell = f"[{style}]{r.status}[/{style}]" if style else r.status
        latency = f"{r.latency_ms:.0f} ms" if r.latency_ms is not None else "-"
        model = r.model_used or "-"
        error = (r.error_detail[:80] + "...") if len(r.error_detail) > 80 else (r.error_detail or "-")
        table.add_row(r.provider_name, status_cell, latency, model, error)

    console.print(table)

    # Summary
    working = sum(1 for r in results if r.status == "working")
    console.print(
        f"\n[bold]{working}[/bold] / [bold]{len(results)}[/bold] endpoints working.\n"
    )

    if args.report:
        console.print("[cyan]Regenerating README...[/cyan]")
        output = generate_report(scan_results=results)
        console.print(f"[green]README generated ({len(output):,} chars)[/green]")


def cmd_report(args: argparse.Namespace) -> None:
    """Generate README from last scan results."""
    console.print("[cyan]Generating README report...[/cyan]")
    output = generate_report()
    console.print(f"[green]README.md generated ({len(output):,} chars)[/green]")


def cmd_list(args: argparse.Namespace) -> None:
    """List all providers in a formatted table."""
    tier = Tier(args.tier) if args.tier else None
    providers = get_providers(tier=tier)

    if args.format == "json":
        data = [dataclasses.asdict(p) for p in providers]
        # Convert Tier enum to string for JSON serialisation
        for item in data:
            item["tier"] = item["tier"].value if hasattr(item["tier"], "value") else str(item["tier"])
        console.print_json(json.dumps(data, indent=2, default=str))
        return

    if args.format == "csv":
        import csv
        import io

        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Provider", "Tier", "Endpoint", "Free Limits", "Models", "OpenAI Compatible"])
        for p in providers:
            writer.writerow([
                p.name,
                p.tier.value,
                p.endpoint,
                p.free_limits,
                ", ".join(p.models),
                p.openai_compatible,
            ])
        console.print(buf.getvalue())
        return

    # Default: rich table
    table = Table(title="AI Image Generation Providers", show_lines=True)
    table.add_column("Provider", style="bold cyan")
    table.add_column("Tier", style="magenta")
    table.add_column("Endpoint")
    table.add_column("Free Limits", style="green")
    table.add_column("Models")
    table.add_column("OpenAI Compatible", justify="center")

    for p in providers:
        models_str = ", ".join(p.models[:3])
        if len(p.models) > 3:
            models_str += f" +{len(p.models) - 3}"
        compat = "[green]Yes[/green]" if p.openai_compatible else "[dim]No[/dim]"

        table.add_row(
            p.name,
            p.tier.label,
            p.endpoint[:60] + ("..." if len(p.endpoint) > 60 else ""),
            p.free_limits or "-",
            models_str or "-",
            compat,
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(providers)} providers[/dim]")


def cmd_discover(args: argparse.Namespace) -> None:
    """AI-powered discovery of new providers (placeholder)."""
    console.print("[yellow]Discovery engine coming soon[/yellow]")


def cmd_benchmark(args: argparse.Namespace) -> None:
    """Measure generation speed (placeholder)."""
    console.print("[yellow]Benchmark plugin coming soon[/yellow]")


def cmd_models(args: argparse.Namespace) -> None:
    """Fetch available model lists (placeholder)."""
    console.print("[yellow]Model listing coming soon[/yellow]")


def cmd_export(args: argparse.Namespace) -> None:
    """Export provider data to various formats."""
    providers = get_providers()
    data = [dataclasses.asdict(p) for p in providers]

    # Normalise Tier enum values for serialisation
    for item in data:
        item["tier"] = item["tier"].value if hasattr(item["tier"], "value") else str(item["tier"])

    fmt = args.format
    output_path = args.output

    if fmt == "json":
        content = json.dumps(data, indent=2, default=str)
    elif fmt == "csv":
        import csv
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            # Flatten lists for CSV
            for k, v in row.items():
                if isinstance(v, list):
                    row[k] = ", ".join(str(i) for i in v)
            writer.writerow(row)
        content = buf.getvalue()
    elif fmt == "yaml":
        try:
            import yaml
        except ImportError:
            console.print("[red]PyYAML is required for YAML export. Install with: pip install pyyaml[/red]")
            return
        content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    elif fmt == "html":
        lines = [
            "<!DOCTYPE html>",
            "<html><head><title>AI Image Providers</title>",
            "<style>table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px;text-align:left}th{background:#4CAF50;color:white}tr:nth-child(even){background:#f2f2f2}</style>",
            "</head><body>",
            "<h1>AI Image Generation Providers</h1>",
            "<table><tr><th>Provider</th><th>Tier</th><th>Endpoint</th><th>Free Limits</th><th>Models</th></tr>",
        ]
        for item in data:
            models = item.get("models", [])
            models_str = ", ".join(models) if isinstance(models, list) else str(models)
            lines.append(
                f"<tr><td>{item['name']}</td><td>{item['tier']}</td>"
                f"<td>{item['endpoint']}</td><td>{item.get('free_limits', '')}</td>"
                f"<td>{models_str}</td></tr>"
            )
        lines.extend(["</table>", "</body></html>"])
        content = "\n".join(lines)
    else:
        console.print(f"[red]Unknown format: {fmt}[/red]")
        return

    if output_path:
        Path(output_path).write_text(content, encoding="utf-8")
        console.print(f"[green]Exported {len(data)} providers to {output_path} ({fmt})[/green]")
    else:
        console.print(content)


def cmd_compare(args: argparse.Namespace) -> None:
    """Compare outputs across providers (placeholder)."""
    console.print(f"[yellow]Compare plugin coming soon[/yellow]")
    console.print(f"[dim]Prompt: {args.prompt}[/dim]")
    if args.providers:
        console.print(f"[dim]Providers: {', '.join(args.providers)}[/dim]")


def cmd_costs(args: argparse.Namespace) -> None:
    """Compare pricing per image (placeholder)."""
    console.print("[yellow]Cost comparison coming soon[/yellow]")


def cmd_generate(args: argparse.Namespace) -> None:
    """Quick image generation via provider or cascade."""
    config = load_config()
    prompt = args.prompt
    output_path = args.output
    size = args.size
    provider_name = args.provider

    provider = None
    if provider_name:
        provider = get_provider(provider_name)
        if provider is None:
            console.print(f"[red]Unknown provider: {provider_name}[/red]")
            sys.exit(1)
    else:
        # Cascade: try free OpenAI-compatible providers first
        candidates = [
            p for p in PROVIDERS
            if p.openai_compatible and p.tier in (Tier.free, Tier.generous_free, Tier.free_credits)
        ]
        for candidate in candidates:
            if candidate.auth_style == "none" or (
                candidate.env_key and os.environ.get(candidate.env_key)
            ):
                provider = candidate
                break

        if provider is None:
            # Fall back to URL-based providers (no auth needed)
            for p in PROVIDERS:
                if p.auth_style in ("none", "url"):
                    provider = p
                    break

        if provider is None:
            console.print("[red]No suitable provider found. Set an API key or specify --provider.[/red]")
            sys.exit(1)

    console.print(f"[cyan]Using provider:[/cyan] [bold]{provider.name}[/bold]")
    console.print(f"[cyan]Prompt:[/cyan] {prompt}")

    # Check API key
    if provider.auth_style not in ("none", "url") and provider.env_key:
        api_key = os.environ.get(provider.env_key, "")
        if not api_key:
            console.print(
                f"[red]API key not set. Please set the {provider.env_key} environment variable.[/red]"
            )
            sys.exit(1)
    else:
        api_key = ""

    # Build auth headers
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if provider.auth_style == "bearer" and api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    elif provider.auth_style == "x-api-key" and api_key:
        headers["x-api-key"] = api_key
    elif provider.auth_style == "api-key" and api_key:
        headers["api-key"] = api_key

    try:
        if provider.openai_compatible:
            _generate_openai_compatible(provider, prompt, size, headers, output_path)
        elif provider.auth_style in ("none", "url") and "{prompt}" in provider.endpoint:
            _generate_url_based(provider, prompt, output_path)
        else:
            _generate_rest(provider, prompt, size, headers, output_path)
    except httpx.TimeoutException:
        console.print("[red]Request timed out. Try again or use a different provider.[/red]")
        sys.exit(1)
    except httpx.ConnectError:
        console.print("[red]Could not connect to the provider. Check your network or try a different provider.[/red]")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[red]Generation failed: {exc}[/red]")
        sys.exit(1)


def _generate_openai_compatible(
    provider, prompt: str, size: str, headers: dict, output_path: str,
) -> None:
    """Generate via an OpenAI-compatible endpoint."""
    payload = {
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json",
    }
    if provider.test_model:
        payload["model"] = provider.test_model

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        console.print("[dim]Sending request...[/dim]")
        resp = client.post(provider.endpoint, json=payload, headers=headers)

    if resp.status_code != 200:
        console.print(f"[red]API error ({resp.status_code}): {resp.text[:300]}[/red]")
        sys.exit(1)

    body = resp.json()
    data_list = body.get("data", [])
    if not data_list:
        console.print("[red]No image data in response.[/red]")
        sys.exit(1)

    entry = data_list[0]
    if "b64_json" in entry:
        img_bytes = base64.b64decode(entry["b64_json"])
        Path(output_path).write_bytes(img_bytes)
        console.print(f"[green]Image saved to {output_path}[/green]")
    elif "url" in entry:
        img_url = entry["url"]
        console.print(f"[green]Image URL: {img_url}[/green]")
        # Download the image
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            img_resp = client.get(img_url)
        if img_resp.status_code == 200:
            Path(output_path).write_bytes(img_resp.content)
            console.print(f"[green]Image downloaded to {output_path}[/green]")
        else:
            console.print(f"[yellow]Could not download image (HTTP {img_resp.status_code})[/yellow]")
    else:
        console.print("[red]Unexpected response format.[/red]")
        sys.exit(1)


def _generate_url_based(provider, prompt: str, output_path: str) -> None:
    """Generate via a URL-based endpoint (e.g. Pollinations)."""
    import urllib.parse

    encoded = urllib.parse.quote(prompt, safe="")
    url = provider.endpoint.replace("{prompt}", encoded)

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        console.print("[dim]Sending request...[/dim]")
        resp = client.get(url)

    if resp.status_code != 200:
        console.print(f"[red]API error ({resp.status_code}): {resp.text[:300]}[/red]")
        sys.exit(1)

    content_type = resp.headers.get("content-type", "")
    if not content_type.startswith("image/"):
        console.print(f"[red]Unexpected content type: {content_type}[/red]")
        sys.exit(1)

    Path(output_path).write_bytes(resp.content)
    console.print(f"[green]Image saved to {output_path}[/green]")


def _generate_rest(provider, prompt: str, size: str, headers: dict, output_path: str) -> None:
    """Generate via a generic REST API."""
    payload: dict = {"prompt": prompt}
    if provider.test_model:
        payload["model"] = provider.test_model

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        console.print("[dim]Sending request...[/dim]")
        resp = client.post(provider.endpoint, json=payload, headers=headers)

    if resp.status_code != 200:
        console.print(f"[red]API error ({resp.status_code}): {resp.text[:300]}[/red]")
        sys.exit(1)

    content_type = resp.headers.get("content-type", "")
    if content_type.startswith("image/"):
        Path(output_path).write_bytes(resp.content)
        console.print(f"[green]Image saved to {output_path}[/green]")
        return

    # Try parsing as JSON with base64 or URL
    try:
        body = resp.json()
    except Exception:
        console.print("[red]Could not parse response.[/red]")
        sys.exit(1)

    # Attempt common response shapes
    image_data = None
    if "data" in body and isinstance(body["data"], list) and body["data"]:
        entry = body["data"][0]
        if isinstance(entry, dict):
            image_data = entry.get("b64_json") or entry.get("url")
    elif "image" in body:
        image_data = body["image"]
    elif "output" in body:
        image_data = body["output"]

    if image_data and image_data.startswith("http"):
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            img_resp = client.get(image_data)
        if img_resp.status_code == 200:
            Path(output_path).write_bytes(img_resp.content)
            console.print(f"[green]Image downloaded to {output_path}[/green]")
        else:
            console.print(f"[yellow]Image URL returned but download failed (HTTP {img_resp.status_code})[/yellow]")
    elif image_data:
        # Assume base64
        try:
            img_bytes = base64.b64decode(image_data)
            Path(output_path).write_bytes(img_bytes)
            console.print(f"[green]Image saved to {output_path}[/green]")
        except Exception:
            console.print("[red]Could not decode image data.[/red]")
            sys.exit(1)
    else:
        console.print(f"[yellow]Response received but no image data found.[/yellow]")
        console.print(f"[dim]{json.dumps(body, indent=2, default=str)[:500]}[/dim]")


def cmd_proxy(args: argparse.Namespace) -> None:
    """Start a local OpenAI-compatible proxy (placeholder)."""
    port = args.port
    console.print(f"[yellow]Proxy server coming soon (port {port})[/yellow]")


def cmd_version(args: argparse.Namespace) -> None:
    """Print version."""
    console.print(f"ai-image-dir [bold]{__version__}[/bold]")


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ai-image-dir",
        description="AI Image Generation API Endpoints Directory",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. scan
    sp_scan = subparsers.add_parser("scan", help="Test all image endpoints")
    sp_scan.add_argument(
        "--tier",
        choices=[t.value for t in Tier],
        default=None,
        help="Filter by pricing tier",
    )
    sp_scan.add_argument(
        "--provider",
        default=None,
        help="Test a specific provider by name",
    )
    sp_scan.add_argument(
        "--report",
        action="store_true",
        help="Also regenerate README after scan",
    )

    # 2. report
    subparsers.add_parser("report", help="Generate README from last scan results")

    # 3. list
    sp_list = subparsers.add_parser("list", help="List all providers")
    sp_list.add_argument(
        "--tier",
        choices=[t.value for t in Tier],
        default=None,
        help="Filter by pricing tier",
    )
    sp_list.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    # 4. discover
    subparsers.add_parser("discover", help="AI-powered discovery of new providers")

    # 5. benchmark
    subparsers.add_parser("benchmark", help="Measure generation speed")

    # 6. models
    subparsers.add_parser("models", help="Fetch available model lists")

    # 7. export
    sp_export = subparsers.add_parser("export", help="Export provider data")
    sp_export.add_argument(
        "--format",
        choices=["json", "csv", "yaml", "html"],
        default="json",
        help="Export format (default: json)",
    )
    sp_export.add_argument(
        "--output",
        default=None,
        help="Output file path",
    )

    # 8. compare
    sp_compare = subparsers.add_parser("compare", help="Compare outputs across providers")
    sp_compare.add_argument("prompt", help="The prompt to compare")
    sp_compare.add_argument(
        "--providers",
        nargs="+",
        default=None,
        help="List of provider names to compare",
    )

    # 9. costs
    subparsers.add_parser("costs", help="Compare pricing per image")

    # 10. generate
    sp_generate = subparsers.add_parser("generate", help="Quick generate via cascade")
    sp_generate.add_argument("prompt", help="The image prompt")
    sp_generate.add_argument(
        "--provider",
        default=None,
        help="Specific provider (uses cascade if not set)",
    )
    sp_generate.add_argument(
        "--output",
        default="generated_image.png",
        help="Output file path (default: generated_image.png)",
    )
    sp_generate.add_argument(
        "--size",
        default="1024x1024",
        help="Image size (default: 1024x1024)",
    )

    # 11. proxy
    sp_proxy = subparsers.add_parser("proxy", help="Local OpenAI-compatible proxy")
    sp_proxy.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number (default: 8000)",
    )

    # 12. version
    subparsers.add_parser("version", help="Print version")

    # --- Parse and dispatch ---
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "scan": cmd_scan,
        "report": cmd_report,
        "list": cmd_list,
        "discover": cmd_discover,
        "benchmark": cmd_benchmark,
        "models": cmd_models,
        "export": cmd_export,
        "compare": cmd_compare,
        "costs": cmd_costs,
        "generate": cmd_generate,
        "proxy": cmd_proxy,
        "version": cmd_version,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
