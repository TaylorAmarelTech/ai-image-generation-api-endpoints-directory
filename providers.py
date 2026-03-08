"""
Provider registry for AI image generation services.

Contains a Tier enum, Provider dataclass, and a comprehensive PROVIDERS list
covering 40+ providers across 7 tiers: free, generous_free, free_credits,
freemium, payg, router, and local.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Tier(str, Enum):
    """Classification of provider pricing tiers."""

    free = "free"
    generous_free = "generous_free"
    free_credits = "free_credits"
    freemium = "freemium"
    payg = "payg"
    router = "router"
    local = "local"

    @property
    def label(self) -> str:
        """Return a human-readable description of the tier."""
        labels = {
            Tier.free: "Truly Free",
            Tier.generous_free: "Generous Free Tier",
            Tier.free_credits: "Free Credits on Signup",
            Tier.freemium: "Freemium",
            Tier.payg: "Pay-as-you-go",
            Tier.router: "Router / Aggregator",
            Tier.local: "Local / Self-hosted",
        }
        return labels[self]


@dataclass
class Provider:
    """Describes an AI image generation provider and its capabilities."""

    name: str
    tier: Tier
    endpoint: str
    env_key: str | None = None
    auth_style: str = "bearer"          # "bearer", "x-api-key", "query", "none", "url"
    free_limits: str = ""
    models: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)  # ["txt2img", "img2img", "inpaint", "upscale", ...]
    max_resolution: str = ""
    output_formats: list[str] = field(default_factory=lambda: ["png"])
    supports_batch: bool = False
    supports_negative_prompt: bool = True
    supports_controlnet: bool = False
    supports_lora: bool = False
    openai_compatible: bool = False
    a1111_compatible: bool = False
    signup_url: str = ""
    test_model: str = ""
    notes: str = ""
    status: str = "unknown"
    latency_ms: float | None = None
    error_detail: str = ""


# ---------------------------------------------------------------------------
# Provider registry
# ---------------------------------------------------------------------------

PROVIDERS: list[Provider] = [
    # ===================================================================
    # Tier 1: Truly Free
    # ===================================================================
    Provider(
        name="HuggingFace Inference",
        tier=Tier.free,
        endpoint="https://router.huggingface.co/v1/images/generations",
        env_key="HUGGINGFACE_API_KEY",
        auth_style="bearer",
        free_limits="~300 req/hr",
        models=["FLUX.1-dev", "SDXL", "SD 3.5"],
        capabilities=["txt2img", "img2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://huggingface.co/join",
        test_model="stabilityai/stable-diffusion-xl-base-1.0",
    ),
    Provider(
        name="Cloudflare Workers AI",
        tier=Tier.free,
        endpoint="https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
        env_key="CLOUDFLARE_API_TOKEN",
        auth_style="bearer",
        free_limits="10K images/day",
        models=["SDXL Lightning", "Dreamshaper"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://dash.cloudflare.com/",
        test_model="@cf/stabilityai/stable-diffusion-xl-base-1.0",
    ),
    Provider(
        name="Pollinations.ai",
        tier=Tier.free,
        endpoint="https://image.pollinations.ai/prompt/{prompt}",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited (best-effort)",
        models=["FLUX", "SDXL"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=False,
        signup_url="https://pollinations.ai",
        test_model="flux",
        notes="URL-based, no API key needed",
    ),
    Provider(
        name="Google Gemini (Imagen)",
        tier=Tier.free,
        endpoint="https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict",
        env_key="GOOGLE_API_KEY",
        auth_style="query",
        free_limits="50 images/day (free tier)",
        models=["Imagen 3"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://ai.google.dev/",
        test_model="imagen-3.0-generate-002",
    ),
    Provider(
        name="Together AI",
        tier=Tier.free,
        endpoint="https://api.together.xyz/v1/images/generations",
        env_key="TOGETHER_API_KEY",
        auth_style="bearer",
        free_limits="$5 free credits",
        models=["FLUX.1-schnell-Free", "SDXL", "SD 3.5"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://www.together.ai/",
        test_model="black-forest-labs/FLUX.1-schnell-Free",
    ),
    Provider(
        name="Clipdrop / Stability",
        tier=Tier.free,
        endpoint="https://clipdrop-api.co/text-to-image/v1",
        env_key="STABILITY_API_KEY",
        auth_style="x-api-key",
        free_limits="Limited free tier",
        models=["Stable Diffusion"],
        capabilities=["txt2img", "img2img", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://clipdrop.co/",
    ),
    Provider(
        name="Prodia",
        tier=Tier.free,
        endpoint="https://api.prodia.com/v1/sd/generate",
        env_key="PRODIA_API_KEY",
        auth_style="x-api-key",
        free_limits="100 free/day",
        models=["SD 1.5", "SDXL", "FLUX"],
        capabilities=["txt2img", "img2img"],
        max_resolution="1024x1024",
        output_formats=["png"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://prodia.com/",
        test_model="sdxl",
    ),
    Provider(
        name="Dezgo",
        tier=Tier.free,
        endpoint="https://api.dezgo.com/text2image",
        env_key="DEZGO_API_KEY",
        auth_style="x-api-key",
        free_limits="Free tier available",
        models=["SDXL", "SD 3"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://dezgo.com/",
    ),
    Provider(
        name="StarryAI API",
        tier=Tier.free,
        endpoint="https://api.starryai.com/creations/",
        env_key="STARRYAI_API_KEY",
        auth_style="bearer",
        free_limits="5 images/day",
        models=["StarryAI"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://starryai.com/",
    ),
    Provider(
        name="Craiyon",
        tier=Tier.free,
        endpoint="https://api.craiyon.com/v3",
        env_key=None,
        auth_style="none",
        free_limits="Free (slow, watermarked)",
        models=["Craiyon v3"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["jpeg"],
        supports_batch=True,
        supports_negative_prompt=True,
        signup_url="https://www.craiyon.com/",
        notes="Slow generation, watermarked output",
    ),
    Provider(
        name="Segmind",
        tier=Tier.free,
        endpoint="https://api.segmind.com/v1/sdxl1.0-txt2img",
        env_key="SEGMIND_API_KEY",
        auth_style="x-api-key",
        free_limits="100 free credits",
        models=["SDXL", "FLUX", "Realistic Vision"],
        capabilities=["txt2img", "img2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_lora=True,
        signup_url="https://www.segmind.com/",
    ),

    Provider(
        name="AirBrush API",
        tier=Tier.free,
        endpoint="https://api.airbrush.ai/v1/text-to-image",
        env_key="AIRBRUSH_API_KEY",
        auth_style="bearer",
        free_limits="50 free credits",
        models=["Stable Diffusion", "SDXL"],
        capabilities=["txt2img", "img2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://www.airbrush.ai/",
    ),

    # ===================================================================
    # Tier 2: Generous Free Tier
    # ===================================================================
    Provider(
        name="Leonardo.ai",
        tier=Tier.generous_free,
        endpoint="https://cloud.leonardo.ai/api/rest/v1/generations",
        env_key="LEONARDO_API_KEY",
        auth_style="bearer",
        free_limits="150 tokens/day (~30 images)",
        models=["Phoenix", "Kino XL"],
        capabilities=["txt2img", "img2img", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        signup_url="https://leonardo.ai/",
    ),
    Provider(
        name="Ideogram",
        tier=Tier.generous_free,
        endpoint="https://api.ideogram.ai/generate",
        env_key="IDEOGRAM_API_KEY",
        auth_style="bearer",
        free_limits="10 images/day (free plan)",
        models=["Ideogram 2.0"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://ideogram.ai/",
    ),
    Provider(
        name="Limewire",
        tier=Tier.generous_free,
        endpoint="https://api.limewire.com/api/image/generation",
        env_key="LIMEWIRE_API_KEY",
        auth_style="bearer",
        free_limits="10 credits/day",
        models=["FLUX Pro", "DALL-E 3"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://limewire.com/",
    ),
    Provider(
        name="RunPod Serverless",
        tier=Tier.generous_free,
        endpoint="https://api.runpod.ai/v2/{endpoint_id}/runsync",
        env_key="RUNPOD_API_KEY",
        auth_style="bearer",
        free_limits="$0.50 free credits",
        models=[],
        capabilities=["txt2img", "img2img"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        signup_url="https://www.runpod.io/",
        notes="Bring your own model",
    ),

    # ===================================================================
    # Tier 3: Free Credits on Signup
    # ===================================================================
    Provider(
        name="OpenAI (DALL-E)",
        tier=Tier.free_credits,
        endpoint="https://api.openai.com/v1/images/generations",
        env_key="OPENAI_API_KEY",
        auth_style="bearer",
        free_limits="$5 credits",
        models=["DALL-E 3", "DALL-E 2", "GPT-Image"],
        capabilities=["txt2img", "img2img", "inpaint"],
        max_resolution="1024x1792",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=False,
        supports_negative_prompt=False,
        openai_compatible=True,
        signup_url="https://platform.openai.com/signup",
        test_model="dall-e-3",
    ),
    Provider(
        name="Stability AI",
        tier=Tier.free_credits,
        endpoint="https://api.stability.ai/v2beta/stable-image/generate/core",
        env_key="STABILITY_API_KEY",
        auth_style="bearer",
        free_limits="25 free credits",
        models=["Stable Diffusion 3.5", "SDXL", "Ultra"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="1536x1536",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        signup_url="https://platform.stability.ai/",
    ),
    Provider(
        name="Fireworks AI",
        tier=Tier.free_credits,
        endpoint="https://api.fireworks.ai/inference/v1/images/generations",
        env_key="FIREWORKS_API_KEY",
        auth_style="bearer",
        free_limits="$1 free credits",
        models=["FLUX", "Playground v3"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://fireworks.ai/",
    ),
    Provider(
        name="Replicate",
        tier=Tier.free_credits,
        endpoint="https://api.replicate.com/v1/predictions",
        env_key="REPLICATE_API_TOKEN",
        auth_style="bearer",
        free_limits="Free tier",
        models=["FLUX", "SDXL"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        signup_url="https://replicate.com/",
    ),
    Provider(
        name="DeepInfra",
        tier=Tier.free_credits,
        endpoint="https://api.deepinfra.com/v1/openai/images/generations",
        env_key="DEEPINFRA_API_KEY",
        auth_style="bearer",
        free_limits="$5 free credits",
        models=["FLUX.1", "SDXL Turbo"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://deepinfra.com/",
    ),
    Provider(
        name="Novita AI",
        tier=Tier.free_credits,
        endpoint="https://api.novita.ai/v3/async/txt2img",
        env_key="NOVITA_API_KEY",
        auth_style="bearer",
        free_limits="Free credits",
        models=["SDXL", "SD 1.5", "FLUX"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        signup_url="https://novita.ai/",
    ),
    Provider(
        name="fal.ai",
        tier=Tier.free_credits,
        endpoint="https://fal.run/fal-ai/flux/dev",
        env_key="FAL_KEY",
        auth_style="bearer",
        free_limits="$10 free credits",
        models=["FLUX", "SDXL", "ControlNet"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        signup_url="https://fal.ai/",
    ),
    Provider(
        name="BFL (Black Forest Labs)",
        tier=Tier.free_credits,
        endpoint="https://api.bfl.ml/v1/flux-pro-1.1",
        env_key="BFL_API_KEY",
        auth_style="bearer",
        free_limits="Free beta",
        models=["FLUX Pro", "FLUX.1"],
        capabilities=["txt2img"],
        max_resolution="1440x1440",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=False,
        signup_url="https://docs.bfl.ml/",
    ),
    Provider(
        name="SiliconFlow",
        tier=Tier.free_credits,
        endpoint="https://api.siliconflow.cn/v1/images/generations",
        env_key="SILICONFLOW_API_KEY",
        auth_style="bearer",
        free_limits="Free credits",
        models=["FLUX", "Kolors", "SDXL"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://siliconflow.cn/",
    ),
    Provider(
        name="Hyperbolic",
        tier=Tier.free_credits,
        endpoint="https://api.hyperbolic.xyz/v1/image/generation",
        env_key="HYPERBOLIC_API_KEY",
        auth_style="bearer",
        free_limits="$10 free credits",
        models=["SDXL", "FLUX"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://hyperbolic.xyz/",
    ),

    # ===================================================================
    # Tier 4: Freemium
    # ===================================================================
    Provider(
        name="Midjourney",
        tier=Tier.freemium,
        endpoint="(Discord-based)",
        env_key=None,
        auth_style="none",
        free_limits="$10/mo basic plan",
        models=["Midjourney v6.1"],
        capabilities=["txt2img", "img2img", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png"],
        supports_batch=True,
        supports_negative_prompt=False,
        signup_url="https://www.midjourney.com/",
        notes="No standard REST API, Discord bot interface",
    ),
    Provider(
        name="Adobe Firefly",
        tier=Tier.freemium,
        endpoint="https://firefly-api.adobe.io/v3/images/generate",
        env_key="ADOBE_FIREFLY_CLIENT_ID",
        auth_style="bearer",
        free_limits="25 credits/mo free",
        models=["Firefly 3"],
        capabilities=["txt2img", "img2img", "inpaint"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://firefly.adobe.com/",
    ),

    Provider(
        name="NightCafe",
        tier=Tier.freemium,
        endpoint="https://api.nightcafe.studio/creations",
        env_key="NIGHTCAFE_API_KEY",
        auth_style="bearer",
        free_limits="5 free credits/day",
        models=["SDXL", "DALL-E 3", "Stable Diffusion"],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://nightcafe.studio/",
        notes="Community-oriented art generation platform",
    ),

    # ===================================================================
    # Tier 5: Pay-as-you-go
    # ===================================================================
    Provider(
        name="Getimg.ai",
        tier=Tier.payg,
        endpoint="https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image",
        env_key="GETIMG_API_KEY",
        auth_style="bearer",
        models=["SDXL", "FLUX", "Stable Cascade"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        signup_url="https://getimg.ai/",
        notes="$0.01-0.05/image",
    ),
    Provider(
        name="Monster API",
        tier=Tier.payg,
        endpoint="https://api.monsterapi.ai/v1/generate/sdxl-base",
        env_key="MONSTER_API_KEY",
        auth_style="bearer",
        models=["SDXL", "SD 1.5"],
        capabilities=["txt2img", "img2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://monsterapi.ai/",
        notes="Pay-per-use",
    ),

    Provider(
        name="Dreamstudio",
        tier=Tier.payg,
        endpoint="https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        env_key="STABILITY_API_KEY",
        auth_style="bearer",
        models=["SDXL", "SD 1.5"],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=False,
        signup_url="https://dreamstudio.ai/",
        notes="Stability AI's hosted generation UI/API, pay-per-use",
    ),

    # ===================================================================
    # Tier 6: Routers / Aggregators
    # ===================================================================
    Provider(
        name="OpenRouter",
        tier=Tier.router,
        endpoint="https://openrouter.ai/api/v1/images/generations",
        env_key="OPENROUTER_API_KEY",
        auth_style="bearer",
        models=[],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://openrouter.ai/",
        notes="Routes to multiple image providers",
    ),
    Provider(
        name="Eden AI",
        tier=Tier.router,
        endpoint="https://api.edenai.run/v2/image/generation",
        env_key="EDEN_AI_API_KEY",
        auth_style="bearer",
        models=[],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        signup_url="https://www.edenai.co/",
        notes="Unified API for 10+ providers",
    ),
    Provider(
        name="AI/ML API",
        tier=Tier.router,
        endpoint="https://api.aimlapi.com/images/generations",
        env_key="AIML_API_KEY",
        auth_style="bearer",
        models=[],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        openai_compatible=True,
        signup_url="https://aimlapi.com/",
        notes="Multi-provider image router",
    ),

    # ===================================================================
    # Tier 7: Local / Self-hosted
    # ===================================================================
    Provider(
        name="Automatic1111 (WebUI)",
        tier=Tier.local,
        endpoint="http://localhost:7860/sdapi/v1/txt2img",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        a1111_compatible=True,
        notes="Most popular local SD interface",
    ),
    Provider(
        name="ComfyUI",
        tier=Tier.local,
        endpoint="http://localhost:8188/api/prompt",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        notes="Node-based workflow SD interface",
    ),
    Provider(
        name="Fooocus",
        tier=Tier.local,
        endpoint="http://localhost:7865/v1/generation/text-to-image",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        notes="Simplified local SD",
    ),
    Provider(
        name="SD.Next",
        tier=Tier.local,
        endpoint="http://localhost:7860/sdapi/v1/txt2img",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg", "webp"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        a1111_compatible=True,
        notes="Fork of A1111 with extra backends",
    ),
    Provider(
        name="InvokeAI",
        tier=Tier.local,
        endpoint="http://localhost:9090/api/v1/images/",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img", "img2img", "inpaint", "upscale"],
        max_resolution="2048x2048",
        output_formats=["png", "jpeg"],
        supports_batch=True,
        supports_negative_prompt=True,
        supports_controlnet=True,
        supports_lora=True,
        notes="Professional local SD workflow",
    ),
    Provider(
        name="Stable Diffusion.cpp",
        tier=Tier.local,
        endpoint="http://localhost:8080/txt2img",
        env_key=None,
        auth_style="none",
        free_limits="Unlimited",
        models=[],
        capabilities=["txt2img"],
        max_resolution="1024x1024",
        output_formats=["png"],
        supports_batch=False,
        supports_negative_prompt=True,
        supports_controlnet=False,
        supports_lora=False,
        notes="Lightweight C++ inference",
    ),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_providers(tier: Tier | None = None) -> list[Provider]:
    """Return providers, optionally filtered by tier."""
    if tier is None:
        return list(PROVIDERS)
    return [p for p in PROVIDERS if p.tier == tier]


def get_provider(name: str) -> Provider | None:
    """Return a provider by name (case-insensitive)."""
    name_lower = name.lower()
    for provider in PROVIDERS:
        if provider.name.lower() == name_lower:
            return provider
    return None
