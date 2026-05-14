# Quick-start checklist

> 60-second orientation. For deep methodology, read `PLAYBOOK.md`.

## Step 1 — Pick the scenario

| If the user says... | Do this |
|---|---|
| "Audit [brand] in ChatGPT" | Run the 14-prompt audit only. Produce workbook + one-pager + deck. ~half a day. |
| "Build a content pipeline for [brand]" | Audit + pipeline scaffold. Run stages 1–3 to validate before committing to stages 4–5. |
| "Apply the GEO playbook to [client]" | Full engagement: audit → strategy artefacts → pipeline → monitoring. ~5 hours of agent work. |
| "Set up weekly AI visibility monitoring for [brand]" | Just stand up the workbook + monitor agent. Skip the rest. |

## Step 2 — Discovery (ask the user)

1. Brand name + domain
2. Category (period tracker, fintech app, SaaS, etc.)
3. 5–10 named competitors
4. 3–5 buried assets (research collabs, peer-reviewed studies, certifications, unique features)
5. 3–5 ICPs
6. Deliverable scope (audit-only vs full pipeline)

## Step 3 — Configure

Copy from `templates/`:

```bash
cp templates/audit_input.template.json [client_dir]/config/audit_input.json
cp templates/icp_profiles.template.json [client_dir]/config/icp_profiles.json
cp templates/pipeline.template.yaml [client_dir]/config/pipeline.yaml
```

Fill in each one based on the discovery answers.

## Step 4 — Run the audit

See `methodology/01_audit.md` for the procedure. Output goes into the Monthly Tracking sheet of the workbook (generated next step).

## Step 5 — Generate strategy artefacts

```bash
python3 scripts/build_workbook.py    # 7-sheet xlsx
python3 scripts/build_onepager.py    # A4 pdf
python3 scripts/build_deck.py        # 10-slide pptx
```

(Builders in `methodology/` reference Python scripts that mirror the Flo Health originals.)

## Step 6 — Run the pipeline (if scope includes it)

```bash
cp -R pipeline-scaffold [client_dir]/[client-name]-content-pipeline
cd [client_dir]/[client-name]-content-pipeline
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit .env to add ANTHROPIC_API_KEY

python3 pipeline.py --stage questions   # ~30s, ~$0.06
python3 pipeline.py --stage answers     # ~4min, ~$5
python3 pipeline.py --stage topics      # ~1min, ~$0.50
# Quality gate A — human reviews 10 selected topics
python3 pipeline.py --stage angles      # ~5min, ~$2
python3 pipeline.py --stage write       # ~50min, ~$15
# Quality gate B — URL validation + legal/medical review
python3 pipeline.py --stage publish --dry-run    # validate
python3 pipeline.py --stage publish --status=draft   # upload as drafts
```

## Step 7 — Monitor weekly

```bash
python3 pipeline.py --stage monitor
```

Writes back to the workbook's Monthly Tracking sheet.

---

For the worked Flo Health example: `examples/flo-health/README.md`.

For deep methodology: `PLAYBOOK.md`.
