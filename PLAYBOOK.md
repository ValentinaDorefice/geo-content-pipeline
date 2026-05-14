# GEO Content Pipeline — Playbook

> A reusable methodology for taking any brand from "invisible in AI search" to "cited authority" — with audit, strategy, multi-agent content pipeline, and weekly monitoring.

This playbook is the long-form companion to `SKILL.md`. Read it once before you start a client engagement; refer back when you hit a tricky step.

---

## Why this playbook exists

LLMs (ChatGPT, Perplexity, Claude, Gemini, Google AI Overview) increasingly answer user questions *instead of* showing a list of links. For brands, "ranking #1" is being replaced by "being cited in the AI's synthesized answer." The skill set this requires — **GEO** (Generative Engine Optimization) and **AEO** (Answer Engine Optimization) — is different enough from classic SEO that most teams need a structured methodology to make progress.

This playbook gives you that structure. It's not theory: every step here was applied to Flo Health in May 2026 and produced measurable artefacts in ~5 hours of work.

---

## The five mental models that drive everything

Internalise these and the rest of the playbook is bookkeeping.

### Model 1 — LLMs cite, they don't rank

Traditional SEO is about being #1 on a list of 10 blue links. AI answers are *synthesized* paragraphs that cite 2–5 sources. The goal shifts from "rank high" to "be the source the AI chose."

### Model 2 — Five levers decide AI citations

1. **Exact prompt-question match** — FAQPage schema where Q1 is the user's literal query
2. **Source authority weighting** — Wikipedia, .gov, .edu, peer-reviewed >> commercial
3. **Citation chains** — peer-reviewed → news → AI (recency matters)
4. **Recency** — 2-year-old content gets downweighted
5. **Conflict checking** — claims contradicted by multiple sources are dropped

If a piece of content doesn't pull on at least 3 of these, it won't be cited.

### Model 3 — Five prompt archetypes

Every commercially valuable query a brand cares about falls into one of these:

| Archetype | Example | Common winning move |
|---|---|---|
| **Category** | "best period tracker" | Lead with scale + features + lifecycle |
| **Comparison** | "Flo vs Clue" | Conditional framing: "Use X if A, use Y if B" |
| **Vertical/Specialty** | "best app for PCOS" | Position as tracking layer for the specialist |
| **Sub-segment** | "Flo for teens" | Build dedicated cornerstone + brand-specific sub-pages |
| **Attribute** | "most private period tracker" | Cede absolutist, redefine winnable adjacent category |

### Model 4 — The three citation outcomes

For any prompt × brand combination, the AI engine produces one of these:

| Outcome | What to do |
|---|---|
| **Cited & first-named, positive** | Defend — refresh stats, lock in lead |
| **Cited but mid-list or balanced** | Reframe — surface what makes the brand the *specific* answer |
| **Negative framing or absent** | Either build the missing content + schema, or honestly acknowledge brand can't win this absolute prompt |

### Model 5 — Brand assets break into 3 buckets

When you audit, you'll find:

| Bucket | Examples | What to do |
|---|---|---|
| **Surfaced + working** | Homepage, brand pages | Maintain |
| **Buried + valuable** | Research collaborations in `/newsroom/`, peer-reviewed studies in `/med-research/` | **Lift to top-level URLs** — the single biggest GEO unlock most clients have |
| **Missing** | Comparison pages, specialty cornerstones, FAQPage schema | Build via the content pipeline |

---

## Phase 1 — Audit (1–2 days)

### 1.1 — Define the prompt universe

Write 14 prompts the brand cares about, balanced across the 5 archetypes:

- 3 category prompts
- 2 comparison prompts
- 3 vertical/specialty prompts
- 2 sub-segment prompts
- 4 attribute prompts (this archetype tends to need more coverage because it includes safety/privacy/free/accuracy)

Phrase each prompt as a real user would search it. No marketing language. Use `templates/audit_input.template.json` as the schema.

### 1.2 — Run the audit

For each prompt × engine (start with ChatGPT-with-browsing as your baseline engine):

1. Query the engine
2. Capture the answer verbatim
3. Score on 4 dimensions:
   - **Presence** (Y/N)
   - **Position** (1 / 2 / 3+ / — / Absent)
   - **Sentiment** (1–5, see rubric below)
   - **Specificity** (Generic / Specific / Cited URL)
4. List competitors named
5. Capture key quote (≤300 chars)
6. List source URLs cited

#### Sentiment rubric

| Score | Meaning |
|---|---|
| 1 | Active anti-recommendation ("we do not recommend X for teens") |
| 2 | Balanced-negative ("X is comprehensive but has privacy concerns") |
| 3 | Neutral / balanced ("one of several options to consider") |
| 4 | Positive (named with a specific strength) |
| 5 | Strongly positive ("Best Overall", first-named with multiple proof points) |

### 1.3 — Identify buried assets

Search the brand's domain for content that is **strategically valuable but architecturally invisible**:

- `site:brand.com/newsroom/` — press releases often contain peer-reviewed research nobody surfaces
- `site:brand.com/research/` or `/insights/` — original data behind paywall-of-discoverability
- `site:brand.com /science/` — medical/scientific authority hidden in academic subdomain

Flag these as Tier-1 priorities for the content pipeline. The pipeline's GEO Writer will lift them onto top-level URLs.

### 1.4 — Map the competitor landscape

For each prompt where the brand isn't winning, identify:
- Who *is* cited
- What axis they win on (academic origin? privacy architecture? specialty depth? scale?)
- Whether their moat is structurally non-copyable (e.g., Phendo's Columbia University origin)

This map informs which prompts to fight for vs which to cede honestly.

---

## Phase 2 — Strategy artefacts (half a day)

Three deliverables, each builds on the audit:

### 2.1 — Prompt-Tracking Workbook (`.xlsx`, 7 sheets)

| Sheet | Purpose |
|---|---|
| Cover | Instructions, rubric, cadence |
| Prompt Universe | The 14 prompts with archetype + priority |
| Monthly Tracking | Raw observations (the source of truth) |
| Scorecard | Auto-aggregated KPIs (formulas) |
| Competitor SoV | Share-of-voice heatmap |
| Source Citation Log | Tracks shift from third-party → owned URLs |
| Action Tracker | Prioritized remediation linked to prompts |

Builder: `methodology/02_workbook.md` has the Python script that generates this from `audit_baseline.json`.

### 2.2 — Audit One-Pager (`.pdf`, A4)

One-page leadership leave-behind. Sections:

- Header band with brand name + baseline date
- TL;DR (3 sentences)
- 4 KPI tiles (citation rate · first-named rate · avg sentiment · prompts absent)
- Win/Loss columns (5 prompts each)
- 4 drivers of representation
- 3-tier opportunity ladder (days / weeks / months)
- Year-1 targets strip

Builder: `methodology/03_onepager.md`.

### 2.3 — Strategy Deck (`.pptx`, 10 slides)

Full executive presentation:

1. Title
2. The headline (KPIs + 3 takeaways)
3. Method (archetypes + dimensions)
4. What's broken (14-prompt heatmap + the most damaging quote)
5. Why LLMs surface what they do (5 levers + worked example)
6. Competitor landscape
7. Drivers of the gap
8. 3-tier opportunity ladder
9. Monitoring (KPIs + toolstack)
10. What you'd do first (the single 30-day move)

Builder: `methodology/04_deck.md`.

---

## Phase 3 — Content pipeline (the multi-agent system)

The pipeline is **7 single-purpose agents**, each evaluable and replaceable independently:

```
14-prompt audit
       ↓
[1] Question Generator     → 40 questions × 5 archetypes (8 per batch)
       ↓
[2] Answer Agent           → 40 deep answers, sourced, citation-scored
       ↓
[3] Topic Extractor        → 10 topics ranked by citation potential + strategic value
       ↓
[4] Angle Agent            → 50 ICP-targeted content briefs (10 × 5)
       ↓
[5] GEO Writer             → 50 publish-ready blogs with FAQPage + Article schema
       ↓
[6] Publisher              → WordPress REST API (drafts by default)
       ↓
[7] Monitor                → weekly re-query across ChatGPT/Perplexity/Claude/Gemini
       ↓                     writes back to the workbook
       └─→ feeds back into the next iteration of the audit
```

Each agent's contract:

- **Reads JSON** (input from the previous stage's output)
- **Writes JSON** (output for the next stage)
- **Uses a Markdown system prompt** in `prompts/` (editable without touching code)
- **Has an `if __name__ == '__main__'` entry point** so you can run it standalone

The orchestrator (`pipeline.py`) is just plumbing: `python3 pipeline.py --stage all` or `--stage [questions|answers|topics|angles|write|publish|monitor]`.

Cost envelope:

| Stage | Wall time | API cost |
|---|---|---|
| 1. Question Generator (Haiku, batched) | 30s | $0.06 |
| 2. Answer Agent (Sonnet, 4 concurrent) | 4 min | $5 |
| 3. Topic Extractor (Sonnet) | 1 min | $0.50 |
| 4. Angle Agent (Sonnet, concurrent) | 5 min | $2 |
| 5. GEO Writer (Sonnet, concurrent) | 50 min | $15 |
| 6. Publisher (REST API) | 5 min | $0 |
| 7. Monitor (Sonnet + web search, weekly) | 10 min | $1 |
| **Cold-start total** | **~75 min** | **~$22** |

Steady-state monthly cost (re-running Monitor weekly + monthly content refresh): ~$5/month.

---

## Phase 4 — Quality gates

Don't run the pipeline straight through on first try. Insert two gates:

### Gate A — Between Stage 3 (Topics) and Stage 4 (Angles)

Human review:
- Are the 10 topics strategically right?
- Are all 5 ICPs covered?
- Is the "rejected themes" list well-reasoned (especially product-blocker deferrals)?
- Are buried assets surfaced?

If yes → run Stage 4. If no → tune Stage 3's system prompt and re-run.

### Gate B — Between Stage 5 (Writer) and Stage 6 (Publisher)

URL validation + medical/legal review:
- Run `requests.head()` against every cited URL — flag 404s before publishing
- For health/finance/legal verticals: human reviewer must sign off
- Check that the lifecycle wedge / unique brand claims aren't overstated
- Confirm FAQPage Q1 matches the brief's `lead_question` verbatim

Then `--stage publish --status=draft` (never `--status=publish` from automation alone).

---

## Phase 5 — Monitoring (weekly cadence forever)

Run the Monitor agent weekly. It:

1. Re-queries the 14 audit prompts across ChatGPT / Perplexity / Claude / Gemini
2. Scores each response (presence/position/sentiment/specificity)
3. Appends new rows to the workbook's Monthly Tracking sheet
4. Triggers alerts when:
   - A previously-cited prompt becomes absent
   - Sentiment drops by 2+ points
   - A new competitor enters the top-3
   - A flo.health URL stops being cited

Quarterly: re-test the full prompt universe with humans (engines drift; the auto-monitor catches macro changes, humans catch nuance).

---

## Failure modes and how to recover

| Symptom | Likely cause | Fix |
|---|---|---|
| Stage 1 returns ≠ 40 questions | Model didn't follow strict count | Per-archetype batching (already implemented) |
| Stage 2 fails with auth error | dotenv didn't override shell env | Use `load_dotenv(override=True)` (already implemented) |
| Stage 2 URLs are 404 | Agent lacks web access | Enable `web_search_20250305` tool in `_common.py`, +$3 per run |
| Stage 3 picks generic topics | Audit context too thin | Add more buried assets + lifecycle context to `audit_input.json` |
| Stage 5 articles read like marketing | Writer prompt too permissive | Strengthen the "no superlatives without source" constraint |
| Publisher 401s | App Password mistyped | Regenerate WordPress Application Password |
| Monitor results look random | Engine queried with default temperature | Set `temperature=0` for monitor calls |

---

## Adapting to a new client / topic area

When applying this skill to a new brand, the things that change:

| Component | Change required? | How |
|---|---|---|
| `pipeline.py` orchestrator | No | Reuse as-is |
| `agents/*.py` agent code | No | Reuse as-is |
| `prompts/*.md` system prompts | No | Brand-agnostic by design |
| `config/audit_input.json` | **Yes** | Replace with the new brand's 14 prompts, archetypes, baseline, buried assets, lifecycle wedge |
| `config/icp_profiles.json` | **Yes** | Replace with the new brand's 1–5 ICPs |
| `config/pipeline.yaml` | Minor | Adjust model selection / concurrency / cost caps if needed |
| Workbook/onepager/deck builders | Minor | Update brand-name strings and palette; the structure is reusable |

The two configuration files in `config/` are where 95% of the per-client customisation lives. Everything else is the same machine.

---

## Reading order for a new operator

If you're picking this skill up for the first time:

1. **Read this PLAYBOOK** end-to-end (you're here)
2. **Read `examples/flo-health/README.md`** to see a real engagement shape
3. **Skim `methodology/01_audit.md`** for the audit procedure
4. **Skim `pipeline-scaffold/agents/_common.py`** to understand the shared client / config / prompt-loading pattern
5. **Run the Flo example end-to-end** with the configs in `examples/flo-health/` — cheapest way to learn the system

Then start a real client.

---

## License & attribution

This methodology was developed for Flo Health and is reusable under an open-collaboration model. When applying to a new client, the only constraint is: **never overclaim**. Honest segmentation is what makes the rest of the strategy work.
