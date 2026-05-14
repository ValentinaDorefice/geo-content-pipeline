"""Shared helpers for all agents."""
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import anthropic
import yaml
from dotenv import load_dotenv

load_dotenv(override=True)  # .env is authoritative; ignore stray shell env vars

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
CONFIG = ROOT / "config"
OUTPUT = ROOT / "output"
SAMPLES = ROOT / "samples"


def cfg() -> dict:
    with open(CONFIG / "pipeline.yaml") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> Any:
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text()


def client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in .env")
    return anthropic.Anthropic(api_key=key)


def call_model(
    system: str,
    user: str,
    model: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.4,
    json_mode: bool = False,
) -> str:
    """Single Claude API call with retry."""
    c = client()
    model = model or cfg()["model"]["primary"]

    last_err = None
    for attempt in range(3):
        try:
            msg = c.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            text = "".join(b.text for b in msg.content if b.type == "text")
            if json_mode:
                # Strip code fences if present, then validate JSON
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
                json.loads(text)  # raises if invalid
            return text
        except (anthropic.APIError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Model call failed after 3 attempts: {last_err}")


def slugify(text: str, max_len: int = 70) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-")
