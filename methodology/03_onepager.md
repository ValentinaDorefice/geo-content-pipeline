# Methodology 03 — The Leadership One-Pager

> A4 PDF, 1 page, designed to drop into any presentation or send as a leave-behind.

## What it shows

Top-to-bottom layout:

1. **Header band** — Brand name + baseline date + audit scope
2. **TL;DR box** — 3 sentences capturing the strategic situation
3. **4 KPI tiles** — citation rate · first-named rate · avg sentiment · prompts absent
4. **Win/Loss columns** — 5 prompts each, green = positive citations, red = absent or negative
5. **Drivers of representation** — 4 root causes: top positive, top negative, top structural gap, top buried asset
6. **3-tier opportunity ladder** — Days / Weeks / Months with 5 actions each
7. **Year-1 targets strip** — citation rate %, first-named %, sentiment, negative framing %, absent count

## Layout

Use the navy/teal/sand palette:
- Navy `#1F2A44` — header, footers, primary tiles
- Teal `#2A9D8F` — section accents, secondary tiles, divider rules
- Sand `#F4E6C3` — TL;DR box, targets strip
- Red `#C0392B` — negative tiles, anti-recommendation flags
- Green `#27AE60` — positive tiles, ship-ready actions

## Builder

A4 portrait, ~14mm margins. Built with ReportLab in Python. Reference implementation in the Flo example folder.

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

W, H = A4
c = canvas.Canvas(out, pagesize=A4)
# Header band
c.setFillColor(HexColor("#1F2A44"))
c.rect(0, H - 24*mm, W, 24*mm, fill=1, stroke=0)
# ... etc.
c.save()
```

Full working script: `flo-content-pipeline/...` (mirror it for new clients).

## When to use

- After the audit, when the client wants a single page they can take to leadership
- As a recurring quarterly artefact — regenerate from updated workbook data
- Standalone for procurement / vendor-evaluation meetings

## When NOT to use

- For technical SEO discussions — use the workbook directly
- For implementation team — they want the 3-tier opportunity ladder broken out into a backlog, not summarized
- For the medical/legal reviewer — they need the full audit JSON

## Next step

`04_deck.md` — the 10-slide strategy deck.
