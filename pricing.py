"""Static pricing data for image-generation providers.

Prices are USD per 1024x1024 image at the standard quality the provider
advertises. Values are pulled from public pricing pages and updated
periodically; they should be treated as approximate, not authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass

from providers import Provider, Tier, PROVIDERS


@dataclass(frozen=True)
class Pricing:
    """Per-image pricing for a single provider."""

    provider_name: str
    usd_per_image: float        # Standard 1024x1024 cost in USD
    free_images_per_month: int  # Approximate free allotment (0 if none)
    notes: str = ""

    @property
    def cost_per_1000(self) -> float:
        return self.usd_per_image * 1000


# Pricing as of provider documentation reviewed during the last update.
# Free providers report 0.0; routers and Discord-only providers report -1 as
# "not directly comparable" so the costs command can flag them.
PRICING: dict[str, Pricing] = {
    "HuggingFace Inference":   Pricing("HuggingFace Inference",   0.0,     9000, "Free with rate limits"),
    "Cloudflare Workers AI":   Pricing("Cloudflare Workers AI",   0.0006, 10000, "10K images/day on free plan"),
    "Pollinations.ai":         Pricing("Pollinations.ai",         0.0,    -1,    "Unlimited best-effort, no SLA"),
    "Google Gemini (Imagen)":  Pricing("Google Gemini (Imagen)",  0.03,    1500, "$0.03/image after free tier"),
    "Together AI":             Pricing("Together AI",             0.018,   270,  "$5 free credits on signup"),
    "Clipdrop / Stability":    Pricing("Clipdrop / Stability",    0.04,    100,  "Free tier limited"),
    "Prodia":                  Pricing("Prodia",                  0.003,   3000, "100 free/day, paid plan from $0.003"),
    "Dezgo":                   Pricing("Dezgo",                   0.0035,  0,    "Pay-per-image after free tier"),
    "StarryAI API":            Pricing("StarryAI API",            0.05,    150,  "5/day free"),
    "Craiyon":                 Pricing("Craiyon",                 0.0,    -1,    "Free with watermark, slow"),
    "Segmind":                 Pricing("Segmind",                 0.004,   25,   "100 free credits on signup"),
    "AirBrush API":            Pricing("AirBrush API",            0.02,    50,   "50 free credits"),
    "Leonardo.ai":             Pricing("Leonardo.ai",             0.005,   900,  "~30 free images/day"),
    "Ideogram":                Pricing("Ideogram",                0.08,    300,  "10/day free, $0.08 paid"),
    "Limewire":                Pricing("Limewire",                0.012,   300,  "10 credits/day free"),
    "RunPod Serverless":       Pricing("RunPod Serverless",       0.001,   50,   "BYO model, GPU-second billing"),
    "OpenAI (DALL-E)":         Pricing("OpenAI (DALL-E)",         0.04,    125,  "DALL-E 3 standard, $5 free credits"),
    "Stability AI":            Pricing("Stability AI",            0.04,    25,   "SD 3.5 Large, 25 free credits"),
    "Fireworks AI":            Pricing("Fireworks AI",            0.0039,  250,  "FLUX schnell, $1 free credits"),
    "Replicate":               Pricing("Replicate",               0.0055,  90,   "Varies by model, free tier limited"),
    "DeepInfra":               Pricing("DeepInfra",               0.0009,  5500, "FLUX schnell pricing"),
    "Novita AI":               Pricing("Novita AI",               0.003,   1600, "Free credits on signup"),
    "fal.ai":                  Pricing("fal.ai",                  0.025,   400,  "$10 free credits"),
    "BFL (Black Forest Labs)": Pricing("BFL (Black Forest Labs)", 0.055,   0,    "FLUX Pro 1.1"),
    "SiliconFlow":             Pricing("SiliconFlow",             0.004,   0,    "Free credits on signup"),
    "Hyperbolic":              Pricing("Hyperbolic",              0.01,    1000, "$10 free credits, FLUX/SDXL"),
    "Midjourney":              Pricing("Midjourney",              -1,      0,    "Subscription only, Discord-based"),
    "Adobe Firefly":           Pricing("Adobe Firefly",           0.04,    25,   "25 credits/mo free, then PAYG"),
    "NightCafe":               Pricing("NightCafe",               0.02,    150,  "5 free credits/day"),
    "Getimg.ai":               Pricing("Getimg.ai",               0.0095,  100,  "$0.01-0.05 per image"),
    "Monster API":             Pricing("Monster API",             0.004,   0,    "Pay-per-use"),
    "Dreamstudio":             Pricing("Dreamstudio",             0.04,    25,   "SDXL via Stability v1 API"),
    "OpenRouter":              Pricing("OpenRouter",              -1,      0,    "Marks up underlying provider price"),
    "Eden AI":                 Pricing("Eden AI",                 -1,      0,    "Aggregator markup varies"),
    "AI/ML API":               Pricing("AI/ML API",               -1,      0,    "Aggregator markup varies"),
    "Automatic1111 (WebUI)":   Pricing("Automatic1111 (WebUI)",   0.0,    -1,    "Self-hosted, electricity only"),
    "ComfyUI":                 Pricing("ComfyUI",                 0.0,    -1,    "Self-hosted, electricity only"),
    "Fooocus":                 Pricing("Fooocus",                 0.0,    -1,    "Self-hosted, electricity only"),
    "SD.Next":                 Pricing("SD.Next",                 0.0,    -1,    "Self-hosted, electricity only"),
    "InvokeAI":                Pricing("InvokeAI",                0.0,    -1,    "Self-hosted, electricity only"),
    "Stable Diffusion.cpp":    Pricing("Stable Diffusion.cpp",    0.0,    -1,    "Self-hosted, electricity only"),
}


def get_pricing(provider: Provider | str) -> Pricing | None:
    """Look up pricing for a provider by Provider instance or name."""
    name = provider.name if isinstance(provider, Provider) else provider
    return PRICING.get(name)


def estimate_monthly_cost(
    provider: Provider | str,
    images_per_month: int,
) -> float | None:
    """Estimate monthly cost in USD for *images_per_month* images.

    Returns None when the provider's pricing is non-comparable (e.g. Midjourney
    subscription, routers). Free allotment is subtracted before multiplying.
    """
    p = get_pricing(provider)
    if p is None or p.usd_per_image < 0:
        return None
    free = max(p.free_images_per_month, 0)
    billable = max(images_per_month - free, 0)
    return round(billable * p.usd_per_image, 4)


def all_pricing_sorted(
    by: str = "usd_per_image",
    include_unknown: bool = False,
) -> list[Pricing]:
    """Return all pricing entries sorted by the given attribute.

    Parameters
    ----------
    by:
        Attribute name to sort by (``usd_per_image``, ``free_images_per_month``).
    include_unknown:
        When True, providers with ``usd_per_image == -1`` are included at the end.
    """
    items = list(PRICING.values())
    visible = [p for p in items if p.usd_per_image >= 0]
    hidden = [p for p in items if p.usd_per_image < 0]

    visible.sort(key=lambda p: getattr(p, by))
    if include_unknown:
        return visible + hidden
    return visible


def coverage_check() -> list[str]:
    """Return names of providers in PROVIDERS that are missing from PRICING."""
    return [p.name for p in PROVIDERS if p.name not in PRICING]
