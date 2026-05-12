# Directive: Brand Scraper

## Purpose

Scrape a website's visual brand identity using the Firecrawl API and produce a structured brand report for use in website design and development.

## Inputs

- **URL** (required): The target website to scrape (homepage or key landing page)
- **Fresh** (optional, flag): Pass `--fresh` to bypass Firecrawl's 2-day cache
- **Output** (optional): Custom output filename stem (default: `brand_report`)

## Tools / Scripts

- **Execution script**: `execution/scrape_brand.py`
- **API**: Firecrawl `/v2/scrape` via `firecrawl-py` SDK
- **Formats used**: `branding`, `markdown`, `screenshot`, `images`

## Setup Requirements

1. Install dependencies:
   ```bash
   pip install firecrawl-py python-dotenv
   ```

2. Add API key to `.env`:
   ```
   FIRECRAWL_API_KEY=fc-YOUR_API_KEY
   ```

## Outputs

All outputs are saved to `.tmp/`:

| File | Description |
|------|-------------|
| `.tmp/brand_report.json` | Full structured brand data (machine-readable) |
| `.tmp/brand_report.md` | Human-readable summary with color tables, image links, typography details |

### What's extracted

- **Colors**: primary, secondary, accent, background, text, link, semantic colors
- **Typography**: font families (primary/heading/code), sizes (h1–body), weights, line heights
- **Logos & Brand Images**: logo URL, favicon URL, OG image URL
- **Hero/Header Images**: heuristically identified from URL patterns and early markdown mentions
- **All Images**: full inventory of image URLs on the page
- **UI Components**: button styles (primary/secondary), input field styles
- **Layout/Spacing**: base unit, border radius, padding patterns
- **Animations/Effects**: transition styles, motion personality
- **Brand Personality**: tone, energy, target audience
- **Screenshot**: full-page screenshot URL (expires after 24 hours)
- **Page Markdown**: full page content in markdown format

## Running the script

```bash
# Basic usage
python execution/scrape_brand.py --url "https://example.com"

# Force fresh scrape (bypass cache)
python execution/scrape_brand.py --url "https://example.com" --fresh

# Custom output filename
python execution/scrape_brand.py --url "https://example.com" --output acme_brand
```

## Error Handling & Edge Cases

### Missing API key
Script exits with a clear message pointing to `.env`. No silent failures.

### Scrape fails
- First failure → automatically retries with `maxAge=0` (fresh fetch)
- Second failure → exits with the error code. Surface to user and check [Firecrawl error docs](https://docs.firecrawl.dev/api-reference/errors).

### Branding field is empty
Some sites block scrapers or render purely in JavaScript. The script falls back to:
- Parsing CSS custom properties (`--color-*`, `--font-*`) from returned HTML
- Extracting `<img src>` attributes from raw HTML

Results are marked with a `_note` field indicating fallback mode.

### Images list is empty
Falls back to regex extraction of `<img src>` from HTML, capped at 50 images.

## Credit Usage

| Scenario | Credits |
|----------|---------|
| Single page scrape (branding + markdown + screenshot + images) | ~1–2 credits |
| Multiple pages | ~1–2 credits per page |

Firecrawl caches results for 2 days by default, so repeated scrapes of the same URL are served from cache (same credit cost, but much faster).

## Known Limitations & Gotchas

- **Screenshot URLs expire after 24 hours** — don't store them as permanent links.
- **JavaScript-heavy SPAs** may return empty branding; HTML fallback will fire automatically.
- **Private/authenticated pages** cannot be scraped without additional Firecrawl session/action setup.
- **Sites with aggressive bot protection** (Cloudflare, etc.) may require Enhanced Mode — this is not enabled by default to avoid extra credit cost. Update the script to add `enhanced_mode=True` if needed.

## Updates & Learnings

_(Add notes here as you discover API quirks, timing expectations, or better approaches)_

- Firecrawl `branding` format is part of the v2 API and does not cost extra credits.
- The `images` format returns a flat list of URLs; no alt text or context is provided.
- Hero image detection is heuristic (keyword-based + first markdown images). May miss some and include false positives.
