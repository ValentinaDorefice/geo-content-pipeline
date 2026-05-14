# Methodology 04 — The 10-Slide Strategy Deck

> 16:9 widescreen PPTX. Editable. Presented to leadership in 20–30 minutes.

## Slide-by-slide structure

| # | Slide | Purpose |
|---|---|---|
| 1 | **Title** | Brand name + audit subtitle + presenter byline |
| 2 | **The headline** | 4 KPI tiles + 3 strategic takeaways |
| 3 | **Method** | 14 prompts × 5 archetypes × 4 measurable dimensions — proves rigor |
| 4 | **What's broken** | 14-prompt heatmap (green/yellow/red) + the most damaging verbatim quote |
| 5 | **Why LLMs surface what they do** | The 5 GEO levers + a worked example (why a competitor wins a specific prompt) |
| 6 | **Competitor landscape** | Table of named competitors with what they win and why — closes with the brand's lifecycle wedge |
| 7 | **Drivers of the gap** | 3 root causes: URL architecture, buried research, missing schema |
| 8 | **The fix** | 3-tier opportunity ladder (Days / Weeks / Months) — 5–7 actions each |
| 9 | **Monitoring** | KPIs (primary / secondary / business outcomes) + phased toolstack (Profound, Otterly, DataForSEO MCP, Brand24, Ahrefs, in-house dashboard) |
| 10 | **What to do first** | Full-bleed closing slide — the single 30-day move with reasoning + execution plan |

## Critical design choices

- **Slide headings are sentences, not labels.** "Flo wins where features matter. Loses where authority does." beats "Audit findings."
- **Each slide says ONE thing.** If a slide has more than 1 takeaway, split it.
- **The closing slide is full-bleed and decisive.** Not a wishy-washy "next steps" — a specific commitment.

## Color palette (consistent with one-pager and workbook)

- Navy `#1F2A44` — header bands, primary tiles
- Teal `#2A9D8F` — section accents, slide numbers
- Sand `#F4E6C3` — callouts, targets, "what no competitor has" boxes
- Red `#C0392B` — losses, anti-recommendations
- Green `#27AE60` — wins, ship-ready

## Builder

Built with python-pptx, 13.333×7.5 in (16:9). Reference implementation in the Flo example folder.

## Mapping to evaluation criteria

When this deck is presented (e.g., for a job interview or pitch), the slides map to common evaluation rubrics:

| Criterion | Where it shows up |
|---|---|
| Depth of audit (data not generalities) | Slides 2, 4, 6 |
| GEO/AEO knowledge (why LLMs surface what they do) | Slide 5 |
| Toolstack judgement | Slide 9 |
| Metric thinking tied to business outcomes | Slide 9 (third KPI block) |
| Brand-context understanding | Slide 4 (verbatim quote) + Slide 6 (competitor map) |
| Strategic decisiveness | Slide 10 (the 30-day move) |

## Speaker notes — recommended

- Slide 4 — read the verbatim anti-recommendation quote out loud. It's the emotional anchor.
- Slide 5 — work through the GEO levers example slowly. This is where you demonstrate expertise.
- Slide 9 — be specific about cost ranges. Year-1 stack ~$15–35K is concrete.
- Slide 10 — close with a single sentence: "If I could only do one thing, this is it."

## Next step

`05_pipeline.md` — the 7-agent content production system.
