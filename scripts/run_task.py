#!/usr/bin/env python3
"""
Pattern: run a local task, then report the result back into Feishu.

The agent can call any script like this from chat. Replace `run_task()` with
your own automation (file processing, batch jobs, data pulls, reports...).

Usage:
  python run_task.py "input-file.md"            # demo mode: prints the result
  export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
  python run_task.py "input-file.md"            # also sends the result to Feishu

Design notes:
  - If FEISHU_WEBHOOK is not set, the script still runs and prints the result
    (so you can demo it locally with zero setup).
  - Keep tasks idempotent so a retry is safe.
  - Always report a short, human-readable outcome (success + key numbers).
  - On failure, report the error — don't fail silently in chat.
"""
import sys

from feishu_webhook import configured, send


def notify(text: str) -> None:
    """Send to Feishu if configured; otherwise stay local (demo mode)."""
    if configured():
        send(text)
    else:
        print("[local-only] FEISHU_WEBHOOK not set; result not sent.")


def run_task(arg: str) -> str:
    """Your real automation goes here. Example: count lines of a file."""
    with open(arg, "r", encoding="utf-8") as f:
        lines = sum(1 for _ in f)
    return f"Done. {arg}: {lines} lines processed."


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    try:
        result = run_task(arg)
        notify(f"[automation] {result}")
        print(result)
        return 0
    except Exception as exc:  # surface the failure too
        notify(f"[automation] FAILED: {exc}")
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
