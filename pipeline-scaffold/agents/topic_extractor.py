"""Agent 3 — Topic Extractor.

Ranks the 40 answered questions and selects the top 10 topics for long-form content.
"""
import json
from pathlib import Path

from ._common import OUTPUT, CONFIG, load_json, save_json, load_prompt, call_model, cfg


def run() -> dict:
    answers = load_json(OUTPUT / "02_answers.json")["answers"]
    questions = load_json(OUTPUT / "01_questions.json")["questions"]
    audit = load_json(CONFIG / "audit_input.json")

    # Merge questions + answers into a compact input
    qa_pairs = []
    qmap = {q["id"]: q for q in questions}
    for a in answers:
        q = qmap.get(a.get("question_id"))
        if not q:
            continue
        qa_pairs.append({
            "id": q["id"],
            "question": q["text"],
            "archetype": q["archetype"],
            "parent_prompt_id": q["parent_prompt_id"],
            "icp": q.get("icp_match"),
            "citation_potential": a.get("citation_potential", 0),
            "answer_lead": a.get("answer_lead", ""),
            "competitors_named": a.get("competitors_named", []),
            "flo_strengths_relevant": a.get("flo_strengths_relevant", []),
            "open_questions": a.get("open_questions", []),
        })

    system = load_prompt("topic_extractor")
    user = (
        "## 40 answered questions\n"
        f"{json.dumps(qa_pairs, indent=2)}\n\n"
        "## Audit context (strategic gaps + buried assets)\n"
        f"{json.dumps({'prompts': audit['prompts'], 'buried_assets': audit['buried_assets'], 'lifecycle_wedge': audit['lifecycle_wedge']}, indent=2)}\n\n"
        "Select exactly 10 topics per the system prompt. Output JSON only."
    )
    raw = call_model(
        system=system,
        user=user,
        max_tokens=4000,
        temperature=0.2,
        json_mode=True,
    )
    data = json.loads(raw.strip("` \n").replace("```json", "").replace("```", ""))
    out = OUTPUT / "03_topics.json"
    save_json(out, data)
    print(f"[3/7] Topic Extractor → {len(data['selected_topics'])} topics → {out}")
    return data


if __name__ == "__main__":
    run()
