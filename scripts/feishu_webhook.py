#!/usr/bin/env python3
"""
Send a plain-text message to a Feishu (Lark) group via an incoming webhook.

This is the smallest possible "agent → chat" output path: useful as a building
block when a local task needs to report back into a Feishu group.

Setup:
  1. In the target Feishu group: Settings -> Bots -> Add custom bot -> copy the webhook URL.
  2. Export it:  export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"

Usage:
  python feishu_webhook.py "Build finished: 3 videos rendered."
"""
import json
import os
import sys
import urllib.request

WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "").strip()


def configured() -> bool:
    """True if a webhook URL is available (i.e. we can actually send)."""
    return bool(WEBHOOK)


def send(text: str) -> dict:
    if not WEBHOOK:
        raise SystemExit("FEISHU_WEBHOOK is not set.")
    payload = {"msg_type": "text", "content": {"text": text}}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "Hello from automation."
    print(send(msg))
