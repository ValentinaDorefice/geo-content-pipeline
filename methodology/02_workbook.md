# Methodology 02 — The Prompt-Tracking Workbook

> 7-sheet Excel workbook. The source of truth for the monitoring program. Auto-aggregates KPIs from raw observations.

## What it produces

A `.xlsx` file with formula-driven KPIs that update as new monthly observations are added. Designed for non-technical stakeholders to read.

## The 7 sheets

| # | Sheet | Purpose |
|---|---|---|
| 1 | **Cover** | Instructions, rubric, cadence — the operator's guide |
| 2 | **Prompt Universe** | The 14 prompts with archetype + P0/P1/P2 priority + notes |
| 3 | **Monthly Tracking** | Raw observation log — the source of truth |
| 4 | **Scorecard** | Auto-aggregated KPIs (`COUNTIFS`, `AVERAGEIFS`) |
| 5 | **Competitor SoV** | Share-of-voice heatmap (wildcard `COUNTIFS`) |
| 6 | **Source Citation Log** | Tracks shift from third-party → owned URLs |
| 7 | **Action Tracker** | Prioritized P0/P1/P2 remediations linked to prompts |

## Schema for Monthly Tracking sheet

Columns A-M:

| Col | Field | Type | Validated |
|---|---|---|---|
| A | Month (`YYYY-MM`) | string | — |
| B | Prompt ID | string | dropdown of P01–P14 |
| C | Prompt Text | formula | `VLOOKUP(B, 'Prompt Universe'!A:F, 2, FALSE)` |
| D | Archetype | formula | `VLOOKUP(B, 'Prompt Universe'!A:F, 3, FALSE)` |
| E | Engine | string | dropdown: ChatGPT / Perplexity / Claude / Gemini / Bing Copilot / Google AI Overview |
| F | Flo Cited | Y/N | dropdown |
| G | Position | string | dropdown: 1 / 2 / 3+ / — / Absent |
| H | Sentiment | int | dropdown: 1–5 (conditional formatting: red ≤2, yellow =3, green ≥4) |
| I | Specificity | string | dropdown: Generic / Specific / Cited URL |
| J | Competitors Named | string | comma-separated list |
| K | Key Quote | string | ≤300 chars |
| L | Source URLs Cited | string | semicolon-separated |
| M | Notes | string | free text |

## Scorecard formulas

For each month-row:

```
Observations         = COUNTIF('Monthly Tracking'!A:A, [month])
Flo Cited            = COUNTIFS('Monthly Tracking'!A:A, [month], 'Monthly Tracking'!F:F, "Y")
Citation Rate %      = Flo Cited / Observations
First-Named Count    = COUNTIFS('Monthly Tracking'!A:A, [month], 'Monthly Tracking'!G:G, "1")
First-Named %        = First-Named Count / Flo Cited
Avg Sentiment        = AVERAGEIFS('Monthly Tracking'!H:H, ...)
Negative Framing %   = COUNTIFS(... H:H, "<=2") / Flo Cited
```

All formulas use absolute column references so they survive adding rows.

## Competitor SoV formula

Each cell uses a wildcard `COUNTIFS` against the Competitors Named column:

```
=COUNTIFS('Monthly Tracking'!$A:$A, [month_col]$3, 'Monthly Tracking'!$J:$J, "*"&$A[competitor_row]&"*")
```

Color-scaled heatmap. Add competitors by adding rows; formulas auto-extend.

## Source Citation Log formula

Same wildcard pattern against the Source URLs Cited column. Pre-populated source list categorizes by:
- **Owned** (flo.health, support.flo.health, brand.com)
- **Negative** (FTC, Mozilla Foundation, TBIJ)
- **Authoritative** (Mayo Clinic, NHS, FDA, WHO)
- **Academic** (.edu, PMC, PubMed)
- **Listicle** (third-party listicles)

The goal is to watch the **owned** count grow over months as cornerstone content is published.

## Builder script

The actual workbook is built with Python + openpyxl. Reference implementation:

```python
# pseudocode — full implementation matches the Flo workbook builder
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule

wb = Workbook()
# Add 7 sheets, populate headers, write formulas, apply conditional formatting
# See the Flo Health workbook for the working version
```

The full builder lives at: `/Users/valentinadorefice/Library/Mobile Documents/com~apple~CloudDocs/CLAUDE SKILL SEO/flo-content-pipeline/` (the Flo client folder includes a reusable builder).

## Cadence for re-runs

- **Weekly**: spot-check 5 priority prompts on 3 engines → 15 new rows
- **Monthly**: full 14-prompt re-test × 1 engine → 14 rows
- **Quarterly**: full 14 × all 4 engines → 56 rows

The Scorecard auto-updates as rows are added. No manual recalculation needed (formulas live in cells).

## Next step

`03_onepager.md` — the leadership leave-behind that pulls KPIs from the workbook.
