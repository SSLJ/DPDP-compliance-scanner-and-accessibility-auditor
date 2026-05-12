# South Indian Bank — Extracted Brand Data

**Source**: Live browser extraction from [southindianbank.bank.in](https://www.southindianbank.bank.in/) and [SIBerNet portal](https://sibernet.southindianbank.bank.in/)
**Extracted**: 2026-05-12 | **Method**: Browser DevTools computed styles

---

## Color Palette

### Main Site

| Swatch | Hex | Role |
|--------|-----|------|
| 🟥 | `#B01E23` | **SIB Maroon** — primary brand, header, buttons, logo |
| ⬜ | `#FFFFFF` | **White** — page background, text on dark |
| 🔲 | `#212529` | **Dark Charcoal** — body text, headings |

### e-Banking Portal (SIBerNet)

| Swatch | Hex | Role |
|--------|-----|------|
| 🟥 | `#B01E23` | **SIB Maroon** — top bar, login button |
| ⬜ | `#F5F5F5` | **Off-White** — page/body background |
| 🔲 | `#2F2F2F` | **Footer Charcoal** — footer background |
| ⬜ | `#CCCCCC` | **Input Border Grey** — input field borders |
| 🌸 | `#E99090` | **Secondary Button Border** — light red-pink |

---

## Typography

### Main Site
- **Font**: Plus Jakarta Sans *(Google Fonts)*
- **Fallback**: Arial, Helvetica, sans-serif
- **Body**: 16px / weight 400
- **H2**: 32px / weight 500
- **Nav links**: White (`#FFFFFF`) on maroon header

### e-Banking Portal
- **Headings**: Open Sans — ~24px
- **Body / Labels**: Arial, Helvetica — ~13px

---

## Logo & Asset URLs

### Main Site
| Asset | URL |
|-------|-----|
| Logo | `https://www.southindianbank.bank.in/images/logo.png` |
| Favicon | `https://www.southindianbank.bank.in/images/favicon.png` |

### SIBerNet Portal
| Asset | URL |
|-------|-----|
| White Logo (header) | `https://sibernet.southindianbank.bank.in/corp/static/img/siblogowhite_latest.png` |
| SIBerNet Logo | `https://sibernet.southindianbank.bank.in/corp/static/img/sibernet-logo-new.png` |
| Login Hero Image | `https://sibernet.southindianbank.bank.in/corp/static/img/login-images/sib-01.jpg` |

---

## UI Components

### Primary Button
```
Background : #B01E23
Text       : #FFFFFF
Radius     : 5px
Font       : Plus Jakarta Sans (main) / Open Sans (portal)
```

### Secondary Button
```
Background : #FFFFFF
Text       : #B01E23
Border     : 1px solid #E99090
Radius     : 5px
```

### Input Fields
```
Background : #FFFFFF
Border     : 1px solid #CCCCCC
Radius     : 5px
Font       : Arial, Helvetica
```

---

## Brand Copy

| Context | Text |
|---------|------|
| Main site hero | `EXPERIENCE NEXT-GEN BANKING` |
| Portal tagline | `GO DIGITAL WITH SIB'S QUICK, SAFE & RELIABLE BANKING` |
| Page title (main) | `South Indian Bank: Personal Banking, NRI Banking, Business Banking Services` |
| Page title (portal) | `South Indian Bank - Log in to Internet Banking` |

---

## CSS Custom Properties

```css
:root {
  --sib-maroon:               #B01E23;
  --sib-white:                #FFFFFF;
  --sib-bg-main:              #FFFFFF;
  --sib-bg-portal:            #F5F5F5;
  --sib-text-primary:         #212529;
  --sib-footer-bg:            #2F2F2F;
  --sib-btn-secondary-border: #E99090;
  --sib-input-border:         #CCCCCC;
  --sib-font-main:            'Plus Jakarta Sans', Arial, Helvetica, sans-serif;
  --sib-font-portal:          'Open Sans', Arial, Helvetica, sans-serif;
  --sib-border-radius:        5px;
}
```

## python-pptx RGB Values

```python
from pptx.dml.color import RGBColor

SIB_MAROON        = RGBColor(0xB0, 0x1E, 0x23)  # #B01E23 — primary brand
SIB_WHITE         = RGBColor(0xFF, 0xFF, 0xFF)  # #FFFFFF
SIB_TEXT_PRIMARY  = RGBColor(0x21, 0x25, 0x29)  # #212529 — body/headings
SIB_PORTAL_BG     = RGBColor(0xF5, 0xF5, 0xF5)  # #F5F5F5 — portal background
SIB_FOOTER        = RGBColor(0x2F, 0x2F, 0x2F)  # #2F2F2F — footer
SIB_BTN_BORDER    = RGBColor(0xE9, 0x90, 0x90)  # #E99090 — secondary button border
```
