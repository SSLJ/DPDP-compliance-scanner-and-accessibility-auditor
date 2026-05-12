---
name: brand-guidelines
description: Applies South Indian Bank's (SIB) official brand colors, typography, and visual identity to any artifact. Use it when SIB brand colors, style guidelines, visual formatting, or banking UI standards need to be applied — for documents, presentations, web UI, or any SIB-branded output.
license: Complete terms in LICENSE.txt
---

# South Indian Bank — Brand Guidelines

## Overview

Brand identity extracted from South Indian Bank's live web properties:
- **Main website**: `https://www.southindianbank.bank.in/`
- **e-Banking portal (SIBerNet)**: `https://sibernet.southindianbank.bank.in/`

**Keywords**: SIB, South Indian Bank, SIBerNet, branding, banking UI, corporate identity, visual identity, brand colors, typography, visual formatting

---

## Colors

### Primary Brand Color
- **SIB Maroon**: `#B01E23` — used consistently across all properties (header, primary buttons, logo, active states, top bar)

### Main Website Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary (SIB Maroon) | `#B01E23` | Header bg, primary buttons, logo, accents |
| Secondary Button Border | `#E99090` | Light red border on secondary/outline buttons |
| Body Background | `#FFFFFF` | Page background (white) |
| Primary Text | `#212529` | Headings, body text (dark charcoal) |
| White Text | `#FFFFFF` | Text on dark/maroon backgrounds |

### e-Banking Portal (SIBerNet) Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary (SIB Maroon) | `#B01E23` | Top header bar, Login button |
| Page Background | `#F5F5F5` | Light grey/off-white body |
| Footer Background | `#2F2F2F` | Dark charcoal footer |
| Input Background | `#FFFFFF` | White input fields |
| Input Border | `#CCCCCC` | Light grey 1px border on inputs |

---

## Typography

### Main Website

| Role | Font | Size | Weight | Color |
|------|------|------|--------|-------|
| Body Text | Plus Jakarta Sans | 16px | 400 | `#212529` |
| Headings (H2) | Plus Jakarta Sans | 32px | 500 | `#212529` |
| Nav Links | Plus Jakarta Sans | — | — | `#FFFFFF` (on header) |

**Google Font**: `Plus Jakarta Sans` — loaded via Google Fonts CDN

### e-Banking Portal (SIBerNet)

| Role | Font | Fallback |
|------|------|----------|
| Headings | Open Sans | Arial, Helvetica, sans-serif |
| Body / Labels | Arial | Helvetica, sans-serif |
| Input Fields | Arial | Helvetica, sans-serif |

---

## Logo & Brand Assets

### Main Website
| Asset | URL |
|-------|-----|
| Primary Logo | `https://www.southindianbank.bank.in/images/logo.png` |
| Favicon | `https://www.southindianbank.bank.in/images/favicon.png` |

### e-Banking Portal (SIBerNet)
| Asset | URL |
|-------|-----|
| SIB White Logo (header) | `https://sibernet.southindianbank.bank.in/corp/static/img/siblogowhite_latest.png` |
| SIBerNet Logo | `https://sibernet.southindianbank.bank.in/corp/static/img/sibernet-logo-new.png` |
| Login Slider Image | `https://sibernet.southindianbank.bank.in/corp/static/img/login-images/sib-01.jpg` |

---

## UI Components

### Primary Button
- **Background**: `#B01E23` (Maroon)
- **Text Color**: `#FFFFFF` (White)
- **Border Radius**: `4–5px`
- **Font**: Plus Jakarta Sans (main site) / Open Sans (portal)

### Secondary Button
- **Background**: `#FFFFFF` (White)
- **Border**: `1px solid #E99090` (light red/pink)
- **Text Color**: `#B01E23` (Maroon)
- **Border Radius**: `4–5px`

### Input Fields (SIBerNet)
- **Background**: `#FFFFFF` (White)
- **Border**: `1px solid #CCCCCC` (light grey)
- **Border Radius**: `4–5px`
- **Font**: Arial / Helvetica

---

## Brand Copy & Taglines

| Context | Tagline |
|---------|---------|
| Main website hero | `"EXPERIENCE NEXT-GEN BANKING"` |
| SIBerNet portal | `"GO DIGITAL WITH SIB'S QUICK, SAFE & RELIABLE BANKING"` |
| Page title (main) | `"South Indian Bank: Personal Banking, NRI Banking, Business Banking Services"` |
| Page title (portal) | `"South Indian Bank - Log in to Internet Banking"` |

---

## Applying the Brand

### Smart Color Selection
- **Dark/maroon background** → text color: `#FFFFFF`
- **White/light background** → text color: `#212529` (primary) or `#B01E23` (accent/links)

### CSS Custom Properties

```css
:root {
  /* South Indian Bank Brand */
  --sib-maroon: #B01E23;
  --sib-white: #FFFFFF;
  --sib-bg-main: #FFFFFF;
  --sib-bg-portal: #F5F5F5;
  --sib-text-primary: #212529;
  --sib-footer-bg: #2F2F2F;
  --sib-btn-secondary-border: #E99090;
  --sib-input-border: #CCCCCC;

  /* Typography — Main Site */
  --sib-font-main: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif;
  /* Typography — Portal */
  --sib-font-portal: 'Open Sans', Arial, Helvetica, sans-serif;

  /* Components */
  --sib-border-radius: 5px;
}
```

### python-pptx Color Values (RGB)

```python
from pptx.dml.color import RGBColor

SIB_MAROON        = RGBColor(0xB0, 0x1E, 0x23)   # #B01E23 — primary brand
SIB_WHITE         = RGBColor(0xFF, 0xFF, 0xFF)   # #FFFFFF
SIB_TEXT_PRIMARY  = RGBColor(0x21, 0x25, 0x29)   # #212529 — body/headings
SIB_PORTAL_BG     = RGBColor(0xF5, 0xF5, 0xF5)   # #F5F5F5 — portal background
SIB_FOOTER        = RGBColor(0x2F, 0x2F, 0x2F)   # #2F2F2F — footer
SIB_BTN_BORDER    = RGBColor(0xE9, 0x90, 0x90)   # #E99090 — secondary button border
```
