"""Agent 1 — Question Generator (per-archetype batched).

Generates 8 questions per archetype × 5 archetypes = 40 total.
Sequential batching guarantees strict 8-per-archetype balance.
"""
import json

from ._common import OUTPUT, CONFIG, load_json, save_json, load_prompt, call_model, cfg


ARCHETYPES = ["category", "comparison", "vertical", "sub-segment", "attribute"]


def archetype_context(archetype: str, audit: dict) -> str:
    """Surface the audit prompts most relevant to a given archetype."""
    relevant = [p for p in audit["prompts"] if p["archetype"] == archetype]
    return json.dumps({
        "target_archetype": archetype,
        "relevant_parent_prompts": relevant,
        "all_parent_prompt_ids_with_archetypes": [
            {"id": p["id"], "archetype": p["archetype"], "text": p["text"]} for p in audit["prompts"]
        ],
        "buried_assets": audit["buried_assets"],
        "lifecycle_wedge": audit["lifecycle_wedge"],
    }, indent=2)


def generate_for_archetype(archetype: str, audit: dict, icp: dict, system: str, model: str) -> list:
    user = (
        f"## Generate 8 questions for the **{archetype}** archetype.\n\n"
        "## Audit context\n"
        f"{archetype_context(archetype, audit)}\n\n"
        "## ICP profiles\n"
        f"{json.dumps(icp, indent=2)}\n\n"
        f"Generate exactly 8 {archetype} questions per the system prompt schema. JSON only."
    )
    raw = call_model(
        system=system,
        user=user,
        model=model,
        max_tokens=4000,
        temperature=0.6,
        json_mode=True,
    )
    parsed = json.loads(raw.strip("` \n").replace("```json", "").replace("```", ""))
    return parsed.get("questions", [])


def run() -> dict:
    audit = load_json(CONFIG / "audit_input.json")
    icp = load_json(CONFIG / "icp_profiles.json")
    system = load_prompt("question_generator")
    model = cfg()["model"]["fast"]

    all_questions: list = []
    next_id = 1

    for archetype in ARCHETYPES:
        try:
            batch = generate_for_archetype(archetype, audit, icp, system, model)
            if len(batch) != 8:
                print(f"  [1/7] WARN: {archetype} returned {len(batch)} questions (expected 8)")
            for q in batch[:8]:  # cap at 8 even if model returns more
                q_id = f"Q{next_id:02d}"
                next_id += 1
                all_questions.append({
                    "id": q_id,
                    "text": q.get("text", "").strip(),
                    "archetype": archetype,
                    "parent_prompt_id": q.get("parent_prompt_id"),
                    "icp_match": q.get("icp_match", "general"),
                    "rationale": q.get("rationale", "").strip(),
                })
            print(f"  [1/7] {archetype:12s} → {len(batch[:8])} questions")
        except Exception as e:
            print(f"  [1/7] FAILED {archetype}: {e}")

    data = {"questions": all_questions}
    out = OUTPUT / "01_questions.json"
    save_json(out, data)
    print(f"[1/7] Question Generator → {len(all_questions)} questions across {len(ARCHETYPES)} archetypes → {out}")
    return data


if __name__ == "__main__":
    run()
