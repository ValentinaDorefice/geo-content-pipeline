"""Agent 2 — Answer Agent.

Deep research-style answer for each of the 40 questions.
Runs answers in parallel (configurable concurrency) for speed.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ._common import OUTPUT, CONFIG, load_json, save_json, load_prompt, call_model, cfg


def answer_one(q: dict, audit_context: str, system: str, model: str) -> dict:
    user = (
        "## Audit context (so you understand Flo's strategic position)\n"
        f"{audit_context}\n\n"
        "## Question to answer\n"
        f"{json.dumps(q, indent=2)}\n\n"
        "Answer per the system prompt schema. JSON only."
    )
    raw = call_model(
        system=system,
        user=user,
        model=model,
        max_tokens=cfg()["generation"]["answer_max_tokens"],
        temperature=0.3,
        json_mode=True,
    )
    return json.loads(raw.strip("` \n").replace("```json", "").replace("```", ""))


def run(questions_path: Path | None = None) -> list:
    questions = load_json(questions_path or OUTPUT / "01_questions.json")["questions"]
    audit_context = json.dumps(load_json(CONFIG / "audit_input.json"))[:6000]
    system = load_prompt("answer_agent")
    model = cfg()["model"]["primary"]
    concurrency = cfg()["generation"]["answer_concurrency"]

    answers: list = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(answer_one, q, audit_context, system, model): q for q in questions}
        for i, fut in enumerate(as_completed(futures), 1):
            q = futures[fut]
            try:
                answers.append(fut.result())
                print(f"  [2/7] answered {i}/{len(questions)}: {q['id']}")
            except Exception as e:
                print(f"  [2/7] FAILED {q['id']}: {e}")
                answers.append({"question_id": q["id"], "error": str(e)})

    answers.sort(key=lambda a: a.get("question_id", ""))
    out = OUTPUT / "02_answers.json"
    save_json(out, {"answers": answers})
    print(f"[2/7] Answer Agent → {len(answers)} answers → {out}")
    return answers


if __name__ == "__main__":
    run()
