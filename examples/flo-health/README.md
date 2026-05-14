# Worked Example — Flo Health (May 2026)

> The first client this methodology was applied to. Study this folder before configuring a new client — it's the cleanest way to understand the shape of a real engagement.

## Context

**Flo Health** is the world's most-used period and women's-health tracker (380M+ members). May 2026 baseline. Single-engine audit (ChatGPT with browsing); designed to scale to Perplexity / Claude / Gemini in Q2.

## What was found

| Metric | Baseline |
|---|---|
| AI citation rate | **64%** (9 of 14 prompts) |
| First-named rate | **21%** (3 of 14) |
| Avg sentiment (cited only) | **2.9** / 5 |
| Prompts absent entirely | **5** (most-private, perimenopause, best-free, PCOS, endometriosis) |
| Active anti-recommendation | **1** (teen segment — "Do not recommend Flo for teenagers given the FTC enforcement…") |

### Where Flo wins

- **Best period tracker** (P02) — first-named, sentiment 4
- **Best for trying to conceive** (P07) — first-named, sentiment 4 (but with outdated "35M" stat — 380M is current)
- **Best pregnancy tracker** (P08) — "Best Overall", sentiment 5
- **Flo for IUD users** (P14) — co-recommendation with Spot On
- **Best female wellness apps** (P01) — mid-list mention

### Where Flo loses

- **Is Flo safe** (P03) — FTC settlement narrative uncontested; sentiment 2
- **Flo vs Clue** (P05) — Clue cited first; sentiment 2
- **Flo for teens** (P13) — active anti-recommendation; sentiment 1
- **Most private** (P04) — Drip/Euki/Periodical own this; Flo absent
- **Best perimenopause** (P06) — Balance/Caria own this; Flo absent
- **Best free** (P10) — Euki/Drip/Clue free tier own this; Flo absent
- **Best for PCOS** (P11) — AskPCOS (Monash University) owns this; Flo absent
- **Best for endometriosis** (P12) — Phendo (Columbia University) owns this; Flo absent

## Strategic insights from the audit

1. **The pattern**: Flo wins on category + scale + features. Loses on specialty + privacy-absolutist queries.
2. **The biggest single drag**: FTC settlement narrative, currently uncontested by Flo's own content. Affects 5+ prompts.
3. **The buried assets that should be surfaced**:
   - Mayo Clinic perimenopause research collaboration (in `/newsroom/`, not `/perimenopause/`)
   - >50% endometriosis diagnosis study (in `/newsroom/`, not `/endometriosis/`)
   - Anonymous Mode (open-sourced 2023, post-quantum crypto in 2024)
4. **The lifecycle wedge**: cycle → TTC → pregnancy → postpartum → perimenopause in one app, with 380M+ users contributing data over years. **No competitor can copy this** — Balance can't suddenly have your 15 years of cycle data.

## The 30-day move

**Publish Flo's privacy chronology (2019–2026)** as a dated, factual narrative on `/flo-privacy-faqs/`. Why:
- One asset, 5+ AI-answer shifts (safety, vs Clue, teens, most-private, best-free)
- Zero engineering, only legal review
- Impossible for competitors to copy (only Flo can write Flo's history)
- Compounds permanently across every comparison and safety query

## What was actually built in this engagement

| Artefact | What it is | Location |
|---|---|---|
| **Prompt-tracking workbook** | 7-sheet xlsx with formula-driven KPIs | `Flo_GEO_Prompt_Tracking.xlsx` |
| **Audit one-pager** | A4 PDF leadership leave-behind | `Flo_GEO_Audit_OnePager.pdf` |
| **Strategy deck** | 10-slide PPTX | `Flo_GEO_Deck.pptx` |
| **Multi-agent pipeline** | Runnable Python, 7 agents, end-to-end | `flo-content-pipeline/` |
| **End-to-end summary slide** | Single-slide what-was-done | `Flo_GEO_What_We_Did.pptx` |

All under `/CLAUDE SKILL SEO/` in the user's iCloud Drive.

## Live-test results from the pipeline (May 2026)

Stages 1, 2, and 3 were run live against real Claude API:

| Stage | Output | Cost | Wall time | Quality |
|---|---|---|---|---|
| 1. Questions (batched) | 40 questions, 8 per archetype | $0.06 | 34s | All 5 archetypes balanced; all 5 ICPs covered |
| 2. Answers | 40 deep answers | ~$5 | 4 min | Mean citation potential **7.90**, 39/40 ≥7, 100% named competitors honestly |
| 3. Topics | 10 selected + 6 rejected | $0.50 | 46s | 8/10 high strategic value, all 5 ICPs covered, 10/10 buried-asset unlocks, 3 product-blocker deferrals |

**Cumulative spend after 3 stages: $5.56** for 90 distinct outputs.

## Configs used (in this folder)

- `audit_input.json` — Flo's 14 prompts, archetypes, baselines, buried assets, lifecycle wedge
- `icp_profiles.json` — 5 ICPs (TTC, PCOS, perimenopause, privacy-first, teen/young adult)

These are the **real files** that drove the live test runs. Use them as the shape reference when you write your own client's configs.

## What we'd do differently next time

1. **Enable web search in the Answer Agent from day 1** — saves the URL-validation pass and prevents ~25% hallucinated URLs. Cost +$3 per run.
2. **Run Stage 1 in batched mode from the first try** — the initial single-call version produced an imbalanced 8/8/6/6/12 archetype distribution. Sequential batching enforces 8 per archetype.
3. **`load_dotenv(override=True)` always** — without it, stray shell env vars silently shadow `.env`. We hit this on the first Stage 2 run.

## Where this work was demoed

This methodology was developed as part of an AI search-visibility strategy engagement, demonstrating end-to-end capability: audit → strategy → multi-agent production → monitoring. The deliverable set was designed to evaluate against criteria like:
- depth of audit (data-driven, not generalities)
- GEO/AEO knowledge (why LLMs surface specific results)
- toolstack judgement (real-world tools, real cost ranges)
- metric thinking (business outcomes, not vanity metrics)
- category context (women's health, privacy stakes, competitor landscape)
