"""
scrape_brand.py
---------------
Scrapes a website using the Firecrawl API and extracts comprehensive brand
identity data: colors, typography, fonts, logos, images, UI components, and more.

Usage:
    python execution/scrape_brand.py --url "https://example.com"
    python execution/scrape_brand.py --url "https://example.com" --fresh   # bypass cache
    python execution/scrape_brand.py --url "https://example.com" --output custom_report

Outputs:
    .tmp/brand_report.json  - Full structured brand data
    .tmp/brand_report.md    - Human-readable summary

Requirements:
    pip install firecrawl-py python-dotenv
    FIRECRAWL_API_KEY must be set in .env
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Load environment
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional; env vars may be set directly

try:
    from firecrawl import Firecrawl
except ImportError:
    print("ERROR: firecrawl-py is not installed. Run: pip install firecrawl-py")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    key = os.environ.get("FIRECRAWL_API_KEY", "")
    if not key:
        print(
            "ERROR: FIRECRAWL_API_KEY is not set.\n"
            "Add it to your .env file:\n"
            "  FIRECRAWL_API_KEY=fc-YOUR_API_KEY"
        )
        sys.exit(1)
    return key


def extract_hero_images(all_images: list[str], markdown: str) -> list[str]:
    """
    Heuristically identify hero/header/logo images from the full image list.
    Looks for images whose URLs contain keywords like 'hero', 'header', 'banner',
    'logo', 'og', 'cover', 'feature', 'bg', or 'background'.
    Also checks for images that appear early in the markdown content.
    """
    HERO_KEYWORDS = [
        "hero", "header", "banner", "logo", "og-", "og_", "cover",
        "feature", "splash", "background", "bg-", "bg_", "masthead",
        "jumbotron", "billboard",
    ]
    hero = []
    for url in all_images:
        lower = url.lower()
        if any(kw in lower for kw in HERO_KEYWORDS):
            hero.append(url)

    # Also look for first image referenced in markdown (often the hero)
    md_images = re.findall(r'!\[.*?\]\((https?://[^\)]+)\)', markdown or "")
    for img in md_images[:3]:  # first 3 markdown images
        if img not in hero:
            hero.append(img)

    return hero


def build_markdown_report(data: dict) -> str:
    """Convert the structured brand report dict into a readable markdown document."""
    url = data.get("source_url", "Unknown")
    scraped_at = data.get("scraped_at", "")
    b = data.get("branding", {})
    colors = b.get("colors", {})
    typography = b.get("typography", {})
    fonts = b.get("fonts", [])
    spacing = b.get("spacing", {})
    components = b.get("components", {})
    images_obj = b.get("images", {})
    personality = b.get("personality", {})
    animations = b.get("animations", {})
    all_images = data.get("all_images", [])
    hero_images = data.get("hero_images", [])
    screenshot = data.get("screenshot_url", "")

    lines = [
        f"# Brand Report: {url}",
        f"_Scraped at: {scraped_at}_",
        "",
        "---",
        "",
        "## Color Scheme",
        f"- **Mode**: {b.get('colorScheme', 'unknown')}",
    ]

    if colors:
        lines.append("")
        lines.append("| Role | Hex |")
        lines.append("|------|-----|")
        for role, value in colors.items():
            if value:
                lines.append(f"| {role} | `{value}` |")

    lines += ["", "---", "", "## Typography"]

    font_families = typography.get("fontFamilies", {})
    if font_families:
        for role, family in font_families.items():
            if family:
                lines.append(f"- **{role.capitalize()} font**: {family}")

    if fonts:
        all_font_names = ", ".join(f.get("family", "") for f in fonts if f.get("family"))
        lines.append(f"- **All font families**: {all_font_names}")

    font_sizes = typography.get("fontSizes", {})
    if font_sizes:
        lines.append("")
        lines.append("### Font Sizes")
        lines.append("| Element | Size |")
        lines.append("|---------|------|")
        for element, size in font_sizes.items():
            if size:
                lines.append(f"| {element} | {size} |")

    font_weights = typography.get("fontWeights", {})
    if font_weights:
        lines.append("")
        lines.append("### Font Weights")
        for weight_name, weight_value in font_weights.items():
            if weight_value:
                lines.append(f"- **{weight_name}**: {weight_value}")

    lines += ["", "---", "", "## Spacing & Layout"]
    if spacing.get("baseUnit"):
        lines.append(f"- **Base unit**: {spacing['baseUnit']}px")
    if spacing.get("borderRadius"):
        lines.append(f"- **Border radius**: {spacing['borderRadius']}")
    if spacing.get("padding"):
        lines.append(f"- **Padding**: {spacing['padding']}")

    lines += ["", "---", "", "## UI Components"]

    btn_primary = components.get("buttonPrimary", {})
    if btn_primary:
        lines.append("")
        lines.append("### Primary Button")
        for k, v in btn_primary.items():
            if v:
                lines.append(f"- **{k}**: `{v}`")

    btn_secondary = components.get("buttonSecondary", {})
    if btn_secondary:
        lines.append("")
        lines.append("### Secondary Button")
        for k, v in btn_secondary.items():
            if v:
                lines.append(f"- **{k}**: `{v}`")

    input_style = components.get("input", {})
    if input_style:
        lines.append("")
        lines.append("### Input Fields")
        for k, v in input_style.items():
            if v:
                lines.append(f"- **{k}**: `{v}`")

    if animations:
        lines += ["", "---", "", "## Animations & Effects"]
        for k, v in animations.items():
            if v:
                lines.append(f"- **{k}**: {v}")

    if personality:
        lines += ["", "---", "", "## Brand Personality"]
        for k, v in personality.items():
            if v:
                lines.append(f"- **{k.capitalize()}**: {v}")

    lines += ["", "---", "", "## Brand Images"]
    if images_obj.get("logo"):
        lines.append(f"- **Logo**: [{images_obj['logo']}]({images_obj['logo']})")
    if b.get("logo") and b.get("logo") != images_obj.get("logo"):
        lines.append(f"- **Logo (alt)**: [{b['logo']}]({b['logo']})")
    if images_obj.get("favicon"):
        lines.append(f"- **Favicon**: [{images_obj['favicon']}]({images_obj['favicon']})")
    if images_obj.get("ogImage"):
        lines.append(f"- **OG Image**: [{images_obj['ogImage']}]({images_obj['ogImage']})")

    if hero_images:
        lines += ["", "### Hero / Header Images"]
        for img in hero_images:
            lines.append(f"- [{img}]({img})")

    if screenshot:
        lines += ["", "---", "", "## Screenshot"]
        lines.append(f"![Page screenshot]({screenshot})")
        lines.append(f"_(URL expires after 24 hours)_")

    if all_images:
        lines += ["", "---", "", f"## All Images ({len(all_images)} total)"]
        lines.append("<details><summary>Click to expand full image list</summary>")
        lines.append("")
        for img in all_images:
            lines.append(f"- [{img}]({img})")
        lines.append("")
        lines.append("</details>")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main scraper
# ---------------------------------------------------------------------------

def scrape_brand(url: str, fresh: bool = False, output_stem: str = "brand_report") -> dict:
    api_key = get_api_key()
    firecrawl = Firecrawl(api_key=api_key)

    print(f"[brand-scraper] Scraping: {url}")
    print(f"[brand-scraper] Cache mode: {'fresh (maxAge=0)' if fresh else 'default (2-day cache)'}")

    scrape_kwargs = {
        "formats": ["branding", "markdown", "screenshot", "images"],
    }
    if fresh:
        scrape_kwargs["max_age"] = 0

    # First attempt
    try:
        result = firecrawl.scrape(url, **scrape_kwargs)
    except Exception as e:
        if not fresh:
            print(f"[brand-scraper] First attempt failed: {e}. Retrying with fresh fetch...")
            try:
                scrape_kwargs["max_age"] = 0
                result = firecrawl.scrape(url, **scrape_kwargs)
            except Exception as e2:
                print(f"[brand-scraper] ERROR: Scrape failed after retry: {e2}")
                sys.exit(1)
        else:
            print(f"[brand-scraper] ERROR: Scrape failed: {e}")
            sys.exit(1)

    # result can be a dict-like object or a model; normalize it
    if hasattr(result, "model_dump"):
        result = result.model_dump()
    elif hasattr(result, "__dict__"):
        result = vars(result)

    # Extract fields
    branding = result.get("branding") or {}
    markdown = result.get("markdown") or ""
    screenshot = result.get("screenshot") or ""
    all_images = result.get("images") or []

    # Fallback: if branding is empty, try to extract basic info from HTML
    if not branding:
        print("[brand-scraper] WARNING: Branding data not returned. Attempting HTML fallback...")
        html = result.get("html") or result.get("rawHtml") or ""
        branding = _fallback_extract_from_html(html)

    # Fallback: if all_images is empty, parse from html
    if not all_images:
        html = result.get("html") or result.get("rawHtml") or ""
        all_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        all_images = [img for img in all_images if img.startswith("http")][:50]

    hero_images = extract_hero_images(all_images, markdown)

    # Build the report
    report = {
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "branding": branding,
        "all_images": all_images,
        "hero_images": hero_images,
        "screenshot_url": screenshot,
        "page_markdown": markdown,
    }

    # Save outputs
    tmp_dir = Path(".tmp")
    tmp_dir.mkdir(exist_ok=True)

    json_path = tmp_dir / f"{output_stem}.json"
    md_path = tmp_dir / f"{output_stem}.md"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[brand-scraper] Saved JSON report: {json_path}")

    md_report = build_markdown_report(report)
    md_path.write_text(md_report, encoding="utf-8")
    print(f"[brand-scraper] Saved Markdown report: {md_path}")

    # Print a quick summary to stdout for the orchestrator
    colors = branding.get("colors", {})
    primary = colors.get("primary", "N/A")
    fonts = [f.get("family", "") for f in branding.get("fonts", []) if f.get("family")]
    logo = branding.get("logo") or branding.get("images", {}).get("logo", "N/A")

    print("\n=== Brand Summary ===")
    print(f"  Source URL  : {url}")
    print(f"  Color Scheme: {branding.get('colorScheme', 'unknown')}")
    print(f"  Primary Color: {primary}")
    print(f"  Fonts       : {', '.join(fonts) if fonts else 'N/A'}")
    print(f"  Logo        : {logo}")
    print(f"  Images found: {len(all_images)} total, {len(hero_images)} hero/header")
    print(f"  Screenshot  : {'Yes' if screenshot else 'No'}")
    print(f"  Outputs     : {json_path}, {md_path}")
    print("=====================\n")

    return report


def _fallback_extract_from_html(html: str) -> dict:
    """Basic CSS variable extraction as a fallback when branding API returns nothing."""
    if not html:
        return {}

    css_vars = re.findall(r'--(color|font|bg|background|text|primary|secondary)[^:]*:\s*([^;]+);', html, re.IGNORECASE)
    colors_found = {}
    for name, value in css_vars:
        value = value.strip()
        if re.match(r'#[0-9a-fA-F]{3,8}', value) or value.startswith("rgb"):
            colors_found[name] = value

    font_families = re.findall(r"font-family:\s*['\"]?([A-Za-z][A-Za-z0-9 _-]+)['\"]?", html)
    unique_fonts = list(dict.fromkeys(font_families))[:5]

    return {
        "colors": colors_found,
        "fonts": [{"family": f} for f in unique_fonts],
        "_note": "Extracted via HTML CSS fallback — Firecrawl branding field was empty",
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape brand identity data from a website using Firecrawl."
    )
    parser.add_argument("--url", required=True, help="Target website URL to scrape")
    parser.add_argument(
        "--fresh",
        action="store_true",
        default=False,
        help="Bypass Firecrawl cache and force a fresh scrape (maxAge=0)",
    )
    parser.add_argument(
        "--output",
        default="brand_report",
        help="Output filename stem (without extension). Default: brand_report",
    )
    args = parser.parse_args()

    scrape_brand(url=args.url, fresh=args.fresh, output_stem=args.output)
