# Methodology 05 — The 7-Agent Content Pipeline

> Multi-agent system that turns the audit into published, AI-citation-optimized content. ~$22 cold-start. ~2 hours wall time.

## Architecture

```
audit_input.json + icp_profiles.json
       │
       ▼
[1] Question Generator     →  40 questions × 5 archetypes (8 per archetype, sequential batches)
       ▼
[2] Answer Agent           →  40 deep answers, sourced, citation-scored (4 concurrent calls)
       ▼
[3] Topic Extractor        →  10 topics ranked by citation potential + strategic value
       ▼
[4] Angle Agent            →  50 ICP-targeted content briefs (10 × 5)
       ▼
[5] GEO Writer             →  50 publish-ready blogs with FAQPage + Article schema
       ▼
[6] Publisher              →  WordPress REST API (drafts by default)
       ▼
[7] Monitor                →  weekly re-query across ChatGPT / Perplexity / Claude / Gemini
                              writes back to the workbook
```

## Each agent's contract

Every agent:

- **Reads JSON** from the previous stage's output
- **Writes JSON** to its own output file
- **Loads its system prompt from a markdown file** in `prompts/`
- **Has an `if __name__ == '__main__'` entry point** so it can be run standalone

This means every agent is **independently evaluable and replaceable**.

## Stage 1 — Question Generator

| Input | `audit_input.json` + `icp_profiles.json` |
|---|---|
| Output | `output/01_questions.json` — 40 questions |
| Model | Haiku (cheap, structured) |
| Approach | **Sequential batching per archetype** — 5 calls × 8 questions each |
| Cost | ~$0.06 |
| Wall time | ~30s |

Why sequential batching: requesting 40 questions in one call leads to archetype imbalance (the model favors certain archetypes). 5 batches × 8 enforces 8/8/8/8/8.

## Stage 2 — Answer Agent

| Input | `output/01_questions.json` |
|---|---|
| Output | `output/02_answers.json` — 40 deep answers |
| Model | Sonnet (reasoning + research) |
| Approach | **4 concurrent calls** via ThreadPoolExecutor |
| Cost | ~$5 |
| Wall time | ~4 min |

Each answer is scored on `citation_potential` (1–10), names competitors, lists sources with evidence tiers, and flags open questions for human verification.

**Optional upgrade**: add `web_search_20250305` tool to the model call for URL grounding. +$3 per run. Recommended for production runs since the agent otherwise reconstructs URLs from training data and ~25% can 404.

## Stage 3 — Topic Extractor

| Input | `output/01_questions.json` + `output/02_answers.json` + audit context |
|---|---|
| Output | `output/03_topics.json` — 10 selected topics + rejected themes |
| Model | Sonnet (single call, reasoning-heavy) |
| Cost | ~$0.50 |
| Wall time | ~1 min |

Selects topics by: citation potential + strategic gap closure + buried-asset surfacing + ICP coverage. Explicitly **defers topics blocked by product gaps** (e.g., "wait until HealthKit sync is restored before writing a Flo vs Apple Health comparison").

## Stage 4 — Angle Agent

| Input | `output/03_topics.json` + `icp_profiles.json` |
|---|---|
| Output | `output/04_briefs.json` — 50 ICP-targeted briefs |
| Model | Sonnet (4 concurrent calls) |
| Cost | ~$2 |
| Wall time | ~5 min |

Each topic × 5 ICPs = 5 distinct briefs with different:
- Hook
- Lead question (the verbatim FAQ Q1)
- Tone
- Proof points (drawn from `buried_assets` and `lifecycle_wedge`)
- CTA matching the ICP's awareness stage

## Stage 5 — GEO Writer

| Input | `output/04_briefs.json` |
|---|---|
| Output | `output/articles/*.md` (50 markdown files) + `output/05_articles_manifest.json` |
| Model | Sonnet (4 concurrent calls, large max_tokens) |
| Cost | ~$15 |
| Wall time | ~50 min |

Each article ships with:
- Answer-first lede ≤60 words
- Comparison table with named competitors
- FAQPage with ≥6 Q&As (Q1 verbatim matches the brief's `lead_question`)
- 4+ internal links to cornerstone URLs
- 3 primary sources with [^n] footnotes
- JSON-LD block at the bottom (FAQPage + Article + optional MedicalCondition/Product/Organization)
- Author byline placeholder + date stamp

## Stage 6 — Publisher (WordPress)

| Input | `output/05_articles_manifest.json` |
|---|---|
| Output | `output/06_published.json` — WordPress post IDs + scheduled dates |
| Tool | WordPress REST API (`/wp-json/wp/v2/posts`) with Application Password auth |
| Default | **Uploads as drafts** (`status="draft"`) |
| Cost | $0 |
| Wall time | ~5 min |

Schedule pattern: weekday mornings (Mon/Wed/Fri at 9am). Never auto-publishes to live — human sign-off required between drafts and `--status=publish`.

For a Claude-native version, the same operations map cleanly to a WordPress MCP server (e.g., wp-mcp). The code structure is MCP-ready:

```
POST /wp-json/wp/v2/posts       →  wp_create_post()
POST /wp-json/wp/v2/media       →  wp_upload_media()
GET  /wp-json/wp/v2/categories  →  wp_list_categories()
```

## Stage 7 — Monitor

| Input | `audit_input.json` (the 14 prompts) |
|---|---|
| Output | `output/07_monitor_YYYY-MM.json` + new rows in workbook |
| Models | Claude (with web search) as the canonical engine; ChatGPT/Perplexity/Gemini as additional via their respective APIs |
| Cost | ~$1/week |
| Wall time | ~10 min/week |

Each cycle: re-query the 14 prompts × N engines, score the responses with an LLM judge against the same rubric as the audit, append new observations to the workbook's Monthly Tracking sheet.

## Quality gates

**Gate A — between Stage 3 and Stage 4** — Human reviews the 10 selected topics:
- All ICPs covered?
- Buried assets surfaced?
- Rejected-topics list well-reasoned?
- Are any product-blocker deferrals missing?

**Gate B — between Stage 5 and Stage 6** — URL validation + medical/legal review:
- Run `requests.head()` against every cited URL — flag 404s
- For health/finance/legal: human reviewer signs off
- Confirm FAQPage Q1 matches the brief's `lead_question` verbatim

## Cost summary

| Stage | Cost | Time |
|---|---|---|
| 1. Questions | $0.06 | 30s |
| 2. Answers | $5 | 4 min |
| 3. Topics | $0.50 | 1 min |
| 4. Angles | $2 | 5 min |
| 5. Writer | $15 | 50 min |
| 6. Publisher | $0 | 5 min |
| 7. Monitor (weekly) | $1 | 10 min |
| **Cold-start total** | **~$22** | **~75 min** |
| **Steady-state (monthly)** | **~$4–6** | **~40 min** |

## Next step

`06_publish_and_monitor.md` — operational cadence and weekly monitoring details.
