---
name: brand-scraper
description: Scrapes a website using the Firecrawl API to extract complete brand identity data for use in building a new website. Use this skill whenever a user wants to clone, replicate, analyze, or draw inspiration from an existing website's design — including its colors, fonts, typography, logo, hero images, button styles, UI effects, and overall visual personality. Trigger this skill when the user mentions phrases like "pull the branding from", "scrape the design of", "get the colors/fonts/styles from", "analyze a website's design", "build a site inspired by", or any request that involves understanding or replicating a website's visual identity. Always use this skill proactively if the user pastes a URL and talks about building a new site.
---

# Brand Scraper

Extracts comprehensive brand identity, design system data, and visual assets from any public website using the Firecrawl API. The output is a structured brand report saved to `.tmp/` that can be fed directly into a website-building workflow.

## What this skill produces

A `brand_report.json` file (and human-readable `brand_report.md`) containing:
- **Colors**: tiered color roles — dark, light, mid-gray, light-gray, plus semantic accent colors (primary, secondary, tertiary)
- **Typography**: font families with explicit fallback stacks, sizes, weights, line heights for all heading levels and body text
- **Logos & Favicons**: direct URLs to logo, favicon, and OG image
- **Hero / Header images**: key visual imagery from the page
- **All images**: complete inventory of image URLs with context
- **UI components**: button styles (colors, radius, borders), input styles, shape accent color cycling rules
- **Layout & spacing**: base unit, border radius, padding patterns
- **Animations & effects**: transition styles, hover effects, motion personality
- **Brand personality**: tone, energy level, target audience, visual design keywords
- **Screenshot**: full-page screenshot URL for visual reference
- **Page content summary**: markdown of page content for context
- **Application details**: how to apply the brand in code (CSS variables, python-pptx RGB values, smart background-aware color selection)

---

## Workflow

### Step 1: Get the URL

If the user hasn't provided a URL, ask for it. Only one URL is needed — typically the homepage or a key landing page is best for brand extraction.

### Step 2: Run the scraper script

Run the execution script, passing the target URL:

```bash
python execution/scrape_brand.py --url "https://example.com"
```

The script will:
1. Call Firecrawl with formats: `["branding", "markdown", "screenshot", "images"]`
2. Parse and normalize all returned data
3. Save structured output to `.tmp/brand_report.json`
4. Save a human-readable summary to `.tmp/brand_report.md`

### Step 3: Read and present the results

After the script completes, read `.tmp/brand_report.md` and present the findings to the user in a clear, organized way. Highlight:

- The color palette (show hex values)
- Font families and key type sizes
- Logo and hero image URLs
- Notable UI effects or personality traits
- Any interesting design patterns observed in the markdown content

### Step 4: Offer next steps

Once the brand report is ready, offer to:
- Pass the brand data to a website-building workflow
- Download/save specific images (logo, hero images) locally
- Generate a CSS variables file from the color and typography data
- Produce a design token JSON file

---

## Output format

The `brand_report.json` follows this structure:

```json
{
  "source_url": "https://example.com",
  "scraped_at": "2025-01-01T00:00:00Z",
  "branding": {
    "colorScheme": "light|dark",
    "logo": "https://...",
    "colors": {
      "dark": "#...",
      "light": "#...",
      "midGray": "#...",
      "lightGray": "#...",
      "primary": "#...",
      "secondary": "#...",
      "accent": "#...",
      "background": "#...",
      "textPrimary": "#...",
      "textSecondary": "#...",
      "accentColors": ["#...", "#...", "#..."]
    },
    "fonts": [
      {"family": "Inter", "fallback": "Arial, sans-serif"},
      {"family": "Lora", "fallback": "Georgia, serif"}
    ],
    "typography": {
      "fontFamilies": {
        "primary": "Inter",
        "heading": "Poppins",
        "body": "Lora",
        "code": "Roboto Mono"
      },
      "fontFallbacks": {
        "heading": "Arial",
        "body": "Georgia"
      },
      "headingThreshold": "24pt",
      "fontSizes": {"h1": "48px", "h2": "36px", "body": "16px"},
      "fontWeights": {"regular": 400, "bold": 700}
    },
    "spacing": {"baseUnit": 8, "borderRadius": "8px"},
    "components": {
      "buttonPrimary": {"background": "#...", "textColor": "#...", "borderRadius": "8px"},
      "buttonSecondary": {"background": "transparent", "textColor": "#...", "borderColor": "#..."},
      "shapes": {
        "accentCycling": true,
        "accentOrder": ["orange", "blue", "green"],
        "note": "Non-text shapes cycle through accent colors to maintain visual interest"
      }
    },
    "images": {
      "logo": "https://...",
      "favicon": "https://...",
      "ogImage": "https://..."
    },
    "animations": {},
    "personality": {
      "tone": "professional",
      "energy": "medium",
      "keywords": ["branding", "corporate identity", "visual identity"]
    },
    "applicationDetails": {
      "colorModel": "RGB",
      "cssVariables": true,
      "smartColorSelection": "Selects text color (dark/light) based on background luminance",
      "pythonPptxCompatible": true
    }
  },
  "all_images": ["https://...", "https://..."],
  "hero_images": ["https://..."],
  "screenshot_url": "https://...",
  "page_markdown": "..."
}
```

The `brand_report.md` is a human-friendly version of the same data, formatted with sections for quick reading.

---

## Real extraction example: Anthropic brand

This is what the skill extracted from Anthropic's brand guidelines — a concrete reference for what good output looks like.

### Colors

**Main Colors (tiered roles):**

| Role | Hex | Usage |
|------|-----|-------|
| Dark | `#141413` | Primary text, dark backgrounds |
| Light | `#faf9f5` | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |

**Accent Colors (cycled on non-text shapes):**

| Role | Hex |
|------|-----|
| Orange (primary accent) | `#d97757` |
| Blue (secondary accent) | `#6a9bcc` |
| Green (tertiary accent) | `#788c5d` |

### Typography

| Role | Font | Fallback | Threshold |
|------|------|----------|-----------|
| Headings | Poppins | Arial | 24pt and larger |
| Body text | Lora | Georgia | All other text |

**Smart font application rules:**
- Apply Poppins to all headings ≥ 24pt; fall back to Arial if unavailable
- Apply Lora to body text; fall back to Georgia if unavailable
- No font installation required — works with existing system fonts
- Pre-install Poppins + Lora for best results

### Shape & Accent Color Rules

- Non-text shapes use accent colors (not main colors)
- Cycle order: orange → blue → green
- Maintains visual interest while staying on-brand
- Text color auto-selects dark/light based on background luminance

### Application details

- Colors applied as RGB values (e.g., via `python-pptx`'s `RGBColor` class)
- Color fidelity maintained across different systems
- CSS custom properties pattern: `--color-dark: #141413; --color-accent-orange: #d97757;`

---

## Error handling

- **Missing API key**: The script will exit with a clear message. Tell the user to add `FIRECRAWL_API_KEY=fc-...` to `.env`.
- **Scrape fails (non-200)**: Retry once with `maxAge=0` to bypass cache, then surface the error code to the user.
- **Branding field is empty/null**: Some sites block scrapers or render entirely in JS. In this case, fall back to parsing the `html` format for CSS custom properties (`--color-*`, `--font-*`) and image `src` attributes. Report partial results clearly.
- **Images list is empty**: The `images` format may not always return results. Fall back to extracting `<img>` src attributes from the raw HTML.

---

## Notes on credit usage

Each brand scrape call uses approximately **1 credit** for base scrape + formats. The `branding` format does not cost extra credits. Screenshot format does not add extra credits either. Total per run: ~1–2 credits.

If the user wants to scrape **multiple pages** (e.g., homepage + product page + about page), tell them this will cost ~1–2 credits per page and ask for confirmation before running.
