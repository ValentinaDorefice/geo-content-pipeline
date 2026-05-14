# Methodology 01 — The 14-Prompt Audit

> The first thing you do for any new client. ~half a day of work. Produces `audit_baseline.json` which feeds everything else.

## Goal

Establish a measurable baseline of how the brand appears in AI search engines across a balanced prompt universe — so subsequent work has a before-vs-after benchmark.

## Inputs

- Brand name + domain
- Category context (competitors known to win in this space)
- The 14 prompts (see structure below)

## Output

`audit_baseline.json` containing 14 prompts × per-engine observations, with per-prompt:
- presence (Y/N)
- position (1 / 2 / 3+ / — / Absent)
- sentiment (1–5)
- specificity (Generic / Specific / Cited URL)
- competitors named
- key quote
- source URLs cited

## The prompt universe — 14 prompts, 5 archetypes

Allocate prompts roughly:

| Archetype | Count | Examples |
|---|---|---|
| category | 3 | "best X app", "what's the best X" |
| comparison | 2 | "Brand vs Competitor", "Brand or Apple Health" |
| vertical / specialty | 3 | "best for [condition]", "X for [niche]" |
| sub-segment | 2 | "X for teens", "X for IUD users" |
| attribute | 4 | "is X safe", "most private X", "best free X", "most accurate X" |

Why 4 attribute prompts: defensive / privacy / pricing queries are where most brands have the weakest positions and the most upside.

## Audit procedure (per prompt)

### Step 1 — Query the engine

Use ChatGPT-with-browsing as baseline (or Claude API with `web_search_20250305` tool as proxy). For each prompt:

1. Type the prompt verbatim into the engine
2. Capture the engine's complete response
3. Save the response

### Step 2 — Score the four dimensions

**Presence** — was the brand named? (Y/N)

**Position** — if cited, where in the answer?

| Score | Meaning |
|---|---|
| 1 | First-named brand/product |
| 2 | Second-named |
| 3+ | Third or later |
| — | Cited but not in a ranked list (e.g. "Brand offers X feature…") |
| Absent | Not mentioned |

**Sentiment** — quality of the framing

| Score | Meaning |
|---|---|
| 1 | Active anti-recommendation |
| 2 | Balanced-negative |
| 3 | Neutral / balanced |
| 4 | Positive (with a specific strength) |
| 5 | Strongly positive — "best overall", first-named with multiple proof points |

**Specificity** — how specific is the citation?

| Score | Meaning |
|---|---|
| Generic | Brand name only mention |
| Specific | Brand named with a verifiable claim (number, certification, named feature) |
| Cited URL | A specific brand URL appears in the AI's citation list |

### Step 3 — Capture qualitative context

- **Competitors named** — full list, in order
- **Key quote** — the most damaging or most useful sentence about the brand (≤300 chars)
- **Source URLs cited** — every URL the AI engine links in its response

### Step 4 — Map to strategic gaps

For each prompt, flag:
- **Absent prompts** — content gaps (highest leverage opportunities)
- **Negative-framing prompts** — defensive priorities
- **Already-winning prompts** — refresh opportunities (often outdated stats)

## Identifying buried assets

Run these searches on the brand's domain:

```
site:brand.com/newsroom/
site:brand.com/research/
site:brand.com/insights/
site:brand.com/science/
site:brand.com/blog/ peer-reviewed
site:brand.com/blog/ study
site:brand.com partnership
```

Look for:
- Press releases announcing peer-reviewed research (often buried in `/newsroom/`)
- University or hospital partnership announcements (often only in PR)
- Industry-first certifications or audits
- Original-data studies (most brands publish these and forget)

These are Tier-1 GEO assets — the content pipeline will surface them.

## Identifying the lifecycle wedge

For each brand, find the structurally non-copyable claim:

- A SaaS product → integration depth, native lifecycle (trial → paid → enterprise)
- A consumer app → cohort longitudinality (data the user contributed over years)
- A healthcare/wellness brand → cycle-to-condition continuity, family-stage continuity
- An ecommerce brand → category breadth, shipping infrastructure
- A B2B platform → ecosystem-level integrations

The lifecycle wedge is what the GEO Writer will reference in every category page so it's visible to AI engines.

## Scoring effort

For 14 prompts × 1 engine (baseline): ~3 hours of focused human work + ~$2 of API spend if you automate the engine queries.

For 14 prompts × 4 engines (expanded baseline): ~half a day human + ~$8 API.

## What good looks like

A fully-scored audit produces:
- ≥30% of prompts where brand is first-named (in mature brands) or ≥10% (in new/recovering brands)
- All 14 prompts with at least the 4 quantitative dimensions filled in
- ≥3 buried assets identified
- 1 lifecycle wedge sentence written

If any of these are missing, the strategy phase has nothing to work with.

## Output schema reference

See `templates/audit_input.template.json` for the exact structure.

## Next step

Once `audit_baseline.json` is populated, move to `02_workbook.md`.
