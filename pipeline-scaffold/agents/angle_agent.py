"""Agent 4 — Angle Agent.

For each of the 10 topics, produces 5 ICP-targeted content briefs = 50 briefs total.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ._common import OUTPUT, CONFIG, load_json, save_json, load_prompt, call_model, cfg


def angle_one(topic: dict, icps: list, system: str) -> dict:
    user = (
        "## Topic to spin into 5 ICP angles\n"
        f"{json.dumps(topic, indent=2)}\n\n"
        "## 5 ICP profiles\n"
        f"{json.dumps(icps, indent=2)}\n\n"
        "Produce 5 briefs per the system prompt schema. JSON only."
    )
    raw = call_model(
        system=system,
        user=user,
        max_tokens=4000,
        temperature=0.5,
        json_mode=True,
    )
    return json.loads(raw.strip("` \n").replace("```json", "").replace("```", ""))


def run() -> dict:
    topics = load_json(OUTPUT / "03_topics.json")["selected_topics"]
    icps = load_json(CONFIG / "icp_profiles.json")["icps"]
    system = load_prompt("angle_agent")
    concurrency = cfg()["generation"]["answer_concurrency"]

    all_briefs: list = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(angle_one, t, icps, system): t for t in topics}
        for i, fut in enumerate(as_completed(futures), 1):
            t = futures[fut]
            try:
                result = fut.result()
                all_briefs.extend(result.get("briefs", []))
                print(f"  [4/7] angled {i}/{len(topics)}: {t['topic_id']} ({len(result.get('briefs', []))} briefs)")
            except Exception as e:
                print(f"  [4/7] FAILED {t['topic_id']}: {e}")

    out = OUTPUT / "04_briefs.json"
    save_json(out, {"briefs": all_briefs})
    print(f"[4/7] Angle Agent → {len(all_briefs)} briefs → {out}")
    return {"briefs": all_briefs}


if __name__ == "__main__":
    run()
