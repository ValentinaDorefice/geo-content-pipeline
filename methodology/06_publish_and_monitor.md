# Methodology 06 — Publishing & Weekly Monitoring

> Operational cadence once the pipeline is up and running.

## Publishing cadence

| Action | Frequency | Owner |
|---|---|---|
| Stage 5 generates 50 article drafts | Once per quarter | Pipeline |
| Quality Gate B (URL validation + medical/legal) | Per batch | Human reviewer |
| Stage 6 uploads to WordPress as drafts | Same day as Gate B clearance | Pipeline |
| Schedule drafts to publish (Mon/Wed/Fri @ 9am) | Within 1 week | Content lead |
| Final human edit pass per article | Day before publish | Editor |
| Live publish | Auto-scheduled | WordPress |

50 articles × Mon/Wed/Fri = ~17 weeks of publishing cadence per pipeline run.

## Monitoring cadence

### Weekly (10 min)

```bash
python3 pipeline.py --stage monitor
```

What it does:
- Re-queries the 14 audit prompts × 4 engines (ChatGPT / Perplexity / Claude / Gemini)
- Scores each response on the same rubric
- Appends new rows to the workbook's Monthly Tracking sheet
- Outputs `output/07_monitor_YYYY-MM.json`

Alerts trigger when:
- A previously-cited prompt becomes absent
- Sentiment drops by 2+ points from prior week
- A new competitor enters the top-3 for any prompt
- An owned URL stops being cited

### Monthly (1 hr)

- Full review of the Scorecard sheet
- Compare month-over-month trend on the 5 primary KPIs
- Identify which Action Tracker items have shipped + their measured impact
- Add new actions discovered from this month's observations

### Quarterly (half a day)

- Full 14 × 4 audit re-test (manual + automated mix)
- Wikipedia / Wikidata watchlist review
- Competitor SoV deep dive — has any competitor's positioning shifted?
- Toolstack health check — are subscriptions still cost-effective?
- Report to leadership using the one-pager regenerated from the current workbook

## The 5 primary KPIs (track these monthly)

| KPI | Definition | Year-1 movement target |
|---|---|---|
| Citation Rate % | % of prompts where brand is named | +20pp (e.g. 64% → 85%) |
| First-Named Rate % | % of prompts where brand is named first | +24pp (e.g. 21% → 45%) |
| Avg Sentiment | Cited-only average (1–5) | +0.6 (e.g. 2.9 → ≥3.5) |
| Negative Framing % | % of cited prompts with sentiment ≤2 | -7pp (e.g. 17% → <10%) |
| Absence Count | Prompts where brand isn't cited | -3 (e.g. 5 → ≤2) |

## Secondary KPIs (drivers)

| KPI | Definition |
|---|---|
| Source Diversity | # of distinct brand URLs cited across the prompt universe |
| Schema Coverage | % of priority pages with FAQ + Org + Software/Product schema |
| Comparison URL Coverage | # of `/brand-vs-X/` pages live |
| Academic Citation Index | Peer-reviewed papers citing the brand per quarter |

## Business-outcome KPIs (the only ones that pay rent)

| KPI | Definition |
|---|---|
| AI Referral Traffic | Sessions from `chat.openai.com`, `perplexity.ai`, `claude.ai`, `gemini.google.com` |
| AI-Attributed Conversions | Sign-ups / installs / leads where in-app survey indicates AI assistant as discovery source |
| Branded Search Lift | YoY growth in branded search volume |

## Toolstack for ongoing monitoring

| Phase | Tool | Cost |
|---|---|---|
| Week 1 | Manual tracking spreadsheet | $0 |
| Month 1 | Profound or Otterly (automated multi-engine tracking) | $300–800/mo |
| Month 2 | DataForSEO MCP (programmatic SERP + AI mention API) | $0.30–1.50 per 1K queries |
| Month 2 | Wikipedia watchlists + Brand24 / Mention | $0–99/mo |
| Month 3 | Ahrefs / Semrush (topical authority + competitor backlinks) | existing license likely |
| Quarter 2 | In-house dashboard | build internal |

Year-1 stack budget: ~$15–35K all-in.

## What "winning" looks like at 6 months

A brand running this pipeline competently for 6 months should see:

- Citation rate up 10–20pp
- At least 2 previously-absent prompts now citing the brand
- A new owned URL appearing in AI citations every month (cumulative)
- Wikipedia entry refreshed to include any reform / certification narrative the brand cares about
- AI referral traffic measurable (often 1–3% of total) and growing

## What "failing" looks like

Watch for:
- Citation rate flat or declining → content isn't compounding; check schema + URL architecture
- New articles published but never cited by AI → likely missing FAQPage schema or weak answer-first ledes
- Sentiment dropping → adversarial sources (Mozilla / Consumer Reports / industry critics) are gaining ground; consider defensive content
- Single source domain over-cited (e.g. only `/about` is showing up) → URL architecture issue; lift cornerstones to top-level paths

## Recovery playbook

If KPIs regress, the standard sequence is:

1. **Audit the regressed prompt** — what did the AI answer change to cite instead?
2. **Identify the new winning source** — third-party listicle? academic paper? government report?
3. **Check if your URL still exists and is still authoritative** — sometimes content was deleted, renamed, or had its schema broken in a CMS migration
4. **Tactical move**: refresh the date, refresh the stats, re-submit to Search Console
5. **Strategic move**: build a new piece of content that out-specifies the new winner

## Done.

You now have a full reusable methodology. For the worked example showing how this was actually applied: `examples/flo-health/README.md`.
