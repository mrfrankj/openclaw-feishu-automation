#!/usr/bin/env python3
"""
Pattern: run a local task, then report the result back into Feishu.

The agent can call any script like this from chat. Replace `run_task()` with
your own automation (file processing, batch jobs, data pulls, reports...).

Usage:
  export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
  python run_task.py "input-file.md"

Design notes:
  - Keep tasks idempotent so a retry is safe.
  - Always report a short, human-readable outcome (success + key numbers).
  - On failure, report the error — don't fail silently in chat.
"""
import subprocess
import sys

from feishu_webhook import send


def run_task(arg: str) -> str:
    """Your real automation goes here. Example: count lines of a file."""
    with open(arg, "r", encoding="utf-8") as f:
        lines = sum(1 for _ in f)
    return f"Done. {arg}: {lines} lines processed."


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "sample_docs/handbook.md"
    try:
        result = run_task(arg)
        send(f"[automation] {result}")
        print(result)
        return 0
    except Exception as exc:  # surface the failure in chat too
        try:
            send(f"[automation] FAILED: {exc}")
        finally:
            print(f"FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
