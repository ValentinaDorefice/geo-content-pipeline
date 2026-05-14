---
name: geo-content-pipeline
description: End-to-end Generative Engine Optimization (GEO) and AI Search Visibility methodology — from 14-prompt brand audit through to a 7-agent automated content pipeline that publishes AI-citation-optimized articles to WordPress and tracks weekly visibility across ChatGPT, Perplexity, Claude, and Gemini. Use when the user wants to (1) audit how a brand appears in AI search engines, (2) build a content production pipeline targeting AI citations, (3) set up weekly AI visibility monitoring, (4) apply the methodology to a new client, topic area, or industry. Triggers on phrases like "GEO audit", "AI search visibility", "LLM brand audit", "AEO content pipeline", "build a content pipeline for [brand]", "audit [brand] in ChatGPT", "AI citation strategy", "generative engine optimization", "AI visibility tracking", "apply the GEO playbook to [client]".
---

# GEO Content Pipeline — Skill Manifest

This skill packages a complete, production-tested methodology for **Generative Engine Optimization (GEO) and AI search visibility**. It was originally built and validated for Flo Health (women's health app, May 2026 baseline) and is now reusable for any brand in any topic area.

## What this skill does

When invoked, this skill walks the user through one of four scenarios:

| Scenario | What happens |
|---|---|
| **Full new-client onboarding** | Audit a brand from scratch → strategy → pipeline → monitoring |
| **Audit only** | Run the 14-prompt LLM brand audit and produce KPI workbook + one-pager + 10-slide deck |
| **Pipeline only** (audit already done) | Stand up the 7-agent content production pipeline with brand-specific configs |
| **Add a topic area** to an existing client | Extend an existing brand's prompt universe and re-run targeted stages |

## Pre-flight checklist (always confirm with the user first)

Before invoking any pipeline stage, confirm:

1. **The brand and domain.** Get the brand name, primary domain, and category.
2. **The scope.** Audit only? Audit + strategy deck? Audit + full pipeline? Monitoring only?
3. **The competitors.** A 5–10 competitor list scoped to the category.
4. **The buried assets.** What does the brand own that's not being surfaced? (Mayo Clinic-style research collaborations, peer-reviewed studies, certifications, unique features, lifecycle moats.)
5. **The ICPs.** Up to 5 ideal customer profiles with awareness stage + search behaviour.
6. **The deliverable format.** Workbook only? Workbook + deck? Workbook + deck + running pipeline?
7. **Budget and timeline.** Live API runs cost ~$22 end-to-end; cheaper sub-stages exist.

## Invocation logic

### Step 1 — Discovery (5–10 min interactive)

Ask the user the pre-flight checklist questions. Capture answers into:
- `templates/audit_input.template.json` → produce `audit_input.json`
- `templates/icp_profiles.template.json` → produce `icp_profiles.json`

Both templates live in this skill's `templates/` folder.

### Step 2 — Run the audit (15 min — manual or via this agent)

The audit is **14 prompts × 5 archetypes** (category, comparison, vertical/specialty, sub-segment, attribute). For each prompt:
- Query ChatGPT (or Claude with web search as proxy) with the prompt
- Score on 4 dimensions: presence, position, sentiment, specificity
- Record competitors named, key quotes, source URLs

Output: `output/audit_baseline.json` + populated Monthly Tracking sheet of the workbook.

See **methodology/01_audit.md** for the full procedure and scoring rubric.

### Step 3 — Build the deliverables

Three artefacts, each generated programmatically:

1. **Prompt-Tracking Workbook** (`.xlsx`, 7 sheets) — KPI scorecard auto-aggregated from raw observations. Template + builder in `methodology/02_workbook.md`.
2. **Audit One-Pager** (`.pdf`, A4) — leadership leave-behind with KPIs, win/loss grid, top opportunities, year-1 targets. Builder in `methodology/03_onepager.md`.
3. **Strategy Deck** (`.pptx`, 10 slides) — full executive presentation: TL;DR / method / heatmap / GEO mechanics / competitor map / drivers / 3-tier opportunity ladder / KPI framework / 30-day move. Builder in `methodology/04_deck.md`.

All three reuse the same brand palette (configurable per client) and feed from the same `audit_baseline.json`.

### Step 4 — Set up the content pipeline (optional, when scope is full)

Copy the `pipeline-scaffold/` folder into the client's working directory and customise:

1. Replace `config/audit_input.json` with the client's version from Step 2
2. Replace `config/icp_profiles.json` with the client's ICPs
3. Update `config/pipeline.yaml` (model choices, concurrency, cost caps)
4. Create `.env` from `.env.example` (ANTHROPIC_API_KEY required; WordPress creds optional)
5. `pip install -r requirements.txt`
6. Run stages sequentially: `python3 pipeline.py --stage questions` etc.

The 7-agent pipeline is brand-agnostic — the agent prompts in `prompts/` read brand details from configs at runtime.

See **methodology/05_pipeline.md** for the full agent contract.

### Step 5 — Publish + Monitor (ongoing)

- **Publish** via WordPress REST API (`agents/publisher.py`) — uploads as drafts by default, never auto-publishes to live. Maps cleanly to a WordPress MCP if available.
- **Monitor** weekly with `agents/monitor.py` — re-queries the 14 prompts across ChatGPT / Perplexity / Claude / Gemini and writes observations back into the workbook.

See **methodology/06_publish_and_monitor.md** for the operational cadence.

## Files in this skill

```
geo-content-pipeline/
├── SKILL.md                         ← this manifest
├── PLAYBOOK.md                      ← the full methodology document (reading order: read this in order)
├── README.md                        ← quick-start checklist
├── templates/
│   ├── audit_input.template.json    ← schema for the 14-prompt audit (filled in per client)
│   ├── icp_profiles.template.json   ← schema for ICPs (1–5 per client)
│   └── pipeline.template.yaml       ← runtime config defaults
├── pipeline-scaffold/               ← copy this folder to bootstrap a new client
│   ├── pipeline.py                  ← orchestrator (run --stage all OR per-stage)
│   ├── agents/                      ← 7 single-purpose agents
│   ├── prompts/                     ← 5 editable system prompts (no brand specifics)
│   ├── config/                      ← drop-in audit_input.json + icp_profiles.json
│   ├── requirements.txt
│   └── .env.example
├── methodology/
│   ├── 01_audit.md                  ← how to run the 14-prompt audit
│   ├── 02_workbook.md               ← workbook structure + formula reference
│   ├── 03_onepager.md               ← one-pager spec
│   ├── 04_deck.md                   ← 10-slide deck structure
│   ├── 05_pipeline.md               ← 7-agent contract
│   └── 06_publish_and_monitor.md    ← WordPress + weekly tracking
└── examples/
    └── flo-health/                  ← original Flo Health worked example
        ├── audit_input.json
        ├── icp_profiles.json
        └── README.md                ← what was done, what worked, what we learned
```

## When NOT to use this skill

- **Generic SEO** (traditional Google ranking optimisation) — use the `seo` skill instead
- **Single-page audit** — use `seo-page` for a focused on-page check
- **Schema-only work** — use `seo-schema` for JSON-LD validation
- **Local / GBP** — use `seo-local` or `seo-maps`
- **Content rewriting without LLM citation strategy** — use a content skill, not this one

This skill is specifically for **brands that need to appear in AI-generated answers** (ChatGPT, Perplexity, Gemini, Claude, Google AI Overview) and want a measurable, repeatable program for it.

## Cost envelope (per client, full run)

| Stage | Tokens | Cost |
|---|---|---|
| Audit (manual + LLM-assisted) | — | $0–5 |
| Workbook + One-pager + Deck | — | $0 (no API needed) |
| Pipeline Q-gen | small | $0.06 |
| Answer Agent | medium | $5 |
| Topic Extractor | small | $0.50 |
| Angle Agent | medium | $2 |
| GEO Writer | large | $15 |
| Publisher | n/a | $0 |
| Monitor (weekly) | medium | $1/week |
| **Total cold-start** | | **~$22** |
| **Monthly steady-state** | | **~$4–6** |

## Pre-shipped worked example

`examples/flo-health/` contains the full Flo Health audit input + ICPs + lessons learned, so a new user can study the shape of a real client engagement before configuring their own.
