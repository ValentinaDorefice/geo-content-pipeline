"""Agent 6 — WordPress Publisher.

Reads articles from Agent 5's manifest and publishes them to WordPress via REST API.
Auth via Application Passwords (https://wordpress.org/documentation/article/application-passwords/).

Default behaviour: uploads as DRAFT. Use --status=future + schedule_pattern to schedule.
NEVER auto-publishes live without explicit override — content of medical/safety nature
must clear human review.

For a Claude-native version, the same operations work via a WordPress MCP server
(e.g., github.com/wp-ai/wp-mcp). The code structure here maps cleanly to MCP tool calls:
  POST /wp-json/wp/v2/posts        →  wp_create_post(...)
  POST /wp-json/wp/v2/media        →  wp_upload_media(...)
  GET  /wp-json/wp/v2/categories   →  wp_list_categories(...)
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from ._common import OUTPUT, cfg, load_json, save_json

load_dotenv()


class WordPressClient:
    """Thin wrapper around WP REST API. Same shape as a Claude MCP server would expose."""

    def __init__(self, url: str | None = None, user: str | None = None, app_pw: str | None = None):
        self.url = (url or os.environ.get("WORDPRESS_URL", "")).rstrip("/")
        self.user = user or os.environ.get("WORDPRESS_USER", "")
        self.app_pw = app_pw or os.environ.get("WORDPRESS_APP_PASSWORD", "")
        if not (self.url and self.user and self.app_pw):
            raise RuntimeError("WordPress credentials missing from .env")
        self.auth = (self.user, self.app_pw)

    def create_post(self, *, title: str, content: str, status: str = "draft",
                    categories: list[int] | None = None, tags: list[int] | None = None,
                    meta: dict | None = None, date: str | None = None,
                    author: int | None = None, slug: str | None = None) -> dict:
        payload: dict[str, Any] = {
            "title": title,
            "content": content,
            "status": status,
        }
        if categories: payload["categories"] = categories
        if tags: payload["tags"] = tags
        if meta: payload["meta"] = meta
        if date: payload["date"] = date
        if author: payload["author"] = author
        if slug: payload["slug"] = slug

        r = requests.post(f"{self.url}/posts", auth=self.auth, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def list_categories(self) -> list[dict]:
        r = requests.get(f"{self.url}/categories?per_page=100", auth=self.auth, timeout=30)
        r.raise_for_status()
        return r.json()

    def upload_media(self, file_path: Path, alt_text: str = "") -> dict:
        with open(file_path, "rb") as fh:
            headers = {
                "Content-Disposition": f'attachment; filename="{file_path.name}"',
            }
            r = requests.post(f"{self.url}/media", auth=self.auth, headers=headers,
                              data=fh.read(), timeout=60)
        r.raise_for_status()
        media = r.json()
        if alt_text:
            requests.post(f"{self.url}/media/{media['id']}", auth=self.auth,
                          json={"alt_text": alt_text}, timeout=30)
        return media


def schedule_dates(n_articles: int, pattern: str = "weekday-mornings") -> list[str]:
    """Generate ISO8601 publish dates for n_articles, spaced by pattern."""
    out: list[str] = []
    if pattern == "weekday-mornings":
        # Mon/Wed/Fri at 09:00 starting next Monday
        d = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        while d.weekday() != 0:
            d += timedelta(days=1)
        offsets = [0, 2, 4]  # Mon, Wed, Fri
        week = 0
        for i in range(n_articles):
            day_in_week = offsets[i % 3]
            target = d + timedelta(weeks=week, days=day_in_week)
            out.append(target.isoformat())
            if (i + 1) % 3 == 0:
                week += 1
    else:
        # Default: daily 09:00
        d = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        for i in range(n_articles):
            out.append((d + timedelta(days=i)).isoformat())
    return out


def md_to_html(md: str) -> str:
    """Very minimal markdown→HTML for WP. For production, use the markdown library."""
    try:
        import markdown
        return markdown.markdown(md, extensions=["fenced_code", "tables", "footnotes"])
    except ImportError:
        # Fallback: just preserve as-is in a <div>
        return f"<div class='md-passthrough'><pre>{md}</pre></div>"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML-ish frontmatter block from the markdown body."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    block = text[4:end].strip()
    body = text[end + 5:]
    fm: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v.startswith("[") and v.endswith("]"):
            v = [s.strip().strip('"') for s in v[1:-1].split(",") if s.strip()]
        fm[k.strip()] = v
    return fm, body


def run(dry_run: bool | None = None, status: str = "draft") -> dict:
    dry_run = dry_run if dry_run is not None else (os.environ.get("PIPELINE_DRY_RUN", "false").lower() == "true")
    manifest = load_json(OUTPUT / "05_articles_manifest.json")["articles"]
    schedule = schedule_dates(len(manifest), pattern=cfg()["publishing"]["scheduling_pattern"])

    published = []
    if dry_run:
        print(f"  [6/7] DRY RUN — would publish {len(manifest)} articles to WordPress")
        for art, date in zip(manifest, schedule):
            published.append({**art, "wp_status": status, "wp_scheduled_for": date, "wp_id": None, "wp_url": None})
    else:
        wp = WordPressClient()
        default_cat = cfg()["publishing"]["default_category_id"]
        for i, (art, date) in enumerate(zip(manifest, schedule), 1):
            md_text = Path(art["path"]).read_text()
            fm, body = parse_frontmatter(md_text)
            html = md_to_html(body)
            try:
                resp = wp.create_post(
                    title=fm.get("title", art["title"]),
                    content=html,
                    status=status,
                    slug=art["slug"],
                    date=date if status == "future" else None,
                    categories=[default_cat],
                )
                published.append({**art, "wp_status": resp.get("status"),
                                  "wp_scheduled_for": date, "wp_id": resp.get("id"),
                                  "wp_url": resp.get("link")})
                print(f"  [6/7] {i}/{len(manifest)} {status}: {art['slug']} → id={resp.get('id')}")
            except Exception as e:
                print(f"  [6/7] FAILED {art['slug']}: {e}")
                published.append({**art, "wp_status": "error", "error": str(e)})

    out = OUTPUT / "06_published.json"
    save_json(out, {"published": published, "dry_run": dry_run, "status": status})
    print(f"[6/7] Publisher → {len(published)} entries → {out}")
    return {"published": published}


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    status = "draft"
    for arg in sys.argv[1:]:
        if arg.startswith("--status="):
            status = arg.split("=", 1)[1]
    run(dry_run=dry, status=status)
