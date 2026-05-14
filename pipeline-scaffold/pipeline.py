"""Flo Content Pipeline — orchestrator.

Runs the 7-agent pipeline end-to-end, or any individual stage.

Usage:
    python3 pipeline.py --stage all
    python3 pipeline.py --stage questions
    python3 pipeline.py --stage publish --dry-run
    python3 pipeline.py --stage monitor

Dependencies (pip install -r requirements.txt):
    anthropic, python-dotenv, PyYAML, requests, openpyxl, python-slugify, markdown
"""
import argparse
import sys
import time
from pathlib import Path

from agents import (
    question_generator,
    answer_agent,
    topic_extractor,
    angle_agent,
    geo_writer,
    publisher,
    monitor,
)


STAGES = {
    "questions": question_generator.run,
    "answers":   answer_agent.run,
    "topics":    topic_extractor.run,
    "angles":    angle_agent.run,
    "write":     geo_writer.run,
    "publish":   publisher.run,
    "monitor":   monitor.run,
}

FULL_ORDER = ["questions", "answers", "topics", "angles", "write", "publish", "monitor"]


def main():
    parser = argparse.ArgumentParser(description="Flo Content Pipeline orchestrator")
    parser.add_argument("--stage", required=True,
                        choices=list(STAGES.keys()) + ["all"],
                        help="Stage to run, or 'all' for end-to-end")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only meaningful for publish stage")
    parser.add_argument("--status", default="draft",
                        choices=["draft", "future", "publish", "pending"],
                        help="WordPress post status (publish stage only)")
    args = parser.parse_args()

    if args.stage == "all":
        stages = FULL_ORDER
    else:
        stages = [args.stage]

    started = time.time()
    print(f"=== Flo Content Pipeline · stages: {stages} ===\n")

    for s in stages:
        fn = STAGES[s]
        if s == "publish":
            fn(dry_run=args.dry_run, status=args.status)
        else:
            fn()
        print()

    elapsed = time.time() - started
    print(f"=== Done · {elapsed:.1f}s ===")


if __name__ == "__main__":
    main()
