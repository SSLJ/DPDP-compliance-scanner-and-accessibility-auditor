# Brand Data

This folder stores extracted brand identity data from websites scraped using the `brand-scraper` skill.

## Contents

| File | Bank / Brand | Extracted |
|------|-------------|-----------|
| `south_indian_bank.json` | South Indian Bank (SIB) | 2026-05-12 |
| `south_indian_bank.md` | South Indian Bank (SIB) | 2026-05-12 |

## File Format

Each brand extraction is saved in two formats:
- **`.json`** — machine-readable structured data (colors, typography, assets, CSS vars, python-pptx values)
- **`.md`** — human-readable summary with tables and code blocks

## How to add more brands

Run the brand scraper:
```bash
python execution/scrape_brand.py --url "https://example.com" --output brand_name
```
Then move the outputs from `.tmp/` into this folder.
