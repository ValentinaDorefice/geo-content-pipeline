"""Agent 5 — GEO Writer.

For each brief, produces a publish-ready blog post with answer-first lede,
comparison table, FAQPage JSON-LD, and Article schema.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ._common import OUTPUT, CONFIG, load_json, save_json, load_prompt, call_model, cfg, slugify


def write_one(brief: dict, audit_context: str, system: str) -> dict:
    user = (
        "## Content brief\n"
        f"{json.dumps(brief, indent=2)}\n\n"
        "## Audit context (Flo's strategic position — use when relevant)\n"
        f"{audit_context}\n\n"
        "Write the article per the system prompt schema and structure. JSON only."
    )
    raw = call_model(
        system=system,
        user=user,
        model=cfg()["model"]["writer"],
        max_tokens=8000,
        temperature=0.4,
        json_mode=True,
    )
    return json.loads(raw.strip("` \n").replace("```json", "").replace("```", ""))


def run() -> list:
    briefs = load_json(OUTPUT / "04_briefs.json")["briefs"]
    audit_context = json.dumps(load_json(CONFIG / "audit_input.json"))[:6000]
    system = load_prompt("geo_writer")
    concurrency = cfg()["generation"]["answer_concurrency"]

    articles_dir = OUTPUT / "articles"
    articles_dir.mkdir(parents=True, exist_ok=True)

    manifest: list = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(write_one, b, audit_context, system): b for b in briefs}
        for i, fut in enumerate(as_completed(futures), 1):
            b = futures[fut]
            try:
                result = fut.result()
                fm = result.get("frontmatter", {})
                md = result.get("article_markdown", "")
                slug = fm.get("slug") or slugify(fm.get("title", b["brief_id"]))
                path = articles_dir / f"{slug}.md"
                fm_block = "---\n" + "\n".join(f"{k}: {json.dumps(v) if not isinstance(v, str) else v}" for k, v in fm.items()) + "\n---\n\n"
                path.write_text(fm_block + md)
                manifest.append({
                    "brief_id": b["brief_id"],
                    "title": fm.get("title"),
                    "slug": slug,
                    "path": str(path),
                    "wordcount": fm.get("wordcount"),
                    "primary_keyword": fm.get("primary_keyword"),
                })
                print(f"  [5/7] wrote {i}/{len(briefs)}: {slug}.md")
            except Exception as e:
                print(f"  [5/7] FAILED {b['brief_id']}: {e}")

    save_json(OUTPUT / "05_articles_manifest.json", {"articles": manifest})
    print(f"[5/7] GEO Writer → {len(manifest)} articles → {articles_dir}")
    return manifest


if __name__ == "__main__":
    run()
