# Architecture

## Components

| Component | Role | Runs on |
| --- | --- | --- |
| Feishu (Lark) | Chat front-end for commands & results | Feishu cloud |
| OpenClaw Gateway | Always-on agent runtime (sessions, tools, scheduler) | Local machine |
| Feishu channel | WebSocket long connection to the Feishu open platform | Local machine |
| Skills / tools | `feishu_doc`, `feishu_drive`, `feishu_perm`, `feishu_wiki`, `exec`, file I/O, web fetch, cron | Local machine |
| Memory | Curated long-term memory (`MEMORY.md`) + raw daily notes (`memory/YYYY-MM-DD.md`) | Local workspace |
| Knowledge base (optional) | Private RAG over your own documents | Local / on-prem |

## Message flow

```
User ──(Feishu message)──► Feishu Open Platform
                                 │  (event over WebSocket)
                                 ▼
                          OpenClaw channel
                                 │
                                 ▼
                          Agent (LLM + memory + skills)
                                 │  tool calls
                    ┌────────────┼─────────────┐
                    ▼            ▼             ▼
              feishu_doc     exec/scripts    scheduler
                    │            │             │
                    └────────────┴─────────────┘
                                 │
                                 ▼
                       Result ──► back to Feishu chat
```

## Why a WebSocket connection

The Feishu channel uses a **long-lived WebSocket** (connection mode = `websocket`) instead of an inbound webhook. Benefits:

- **No public IP or exposed inbound port** needed — the agent dials out to Feishu.
- Works behind NAT and on a home/office machine.
- Simpler security surface: nothing listens for the internet.

## Access control

- **DMs**: `dm_policy = "pairing"` — a user must pair before the bot responds.
- **Groups**: `group_policy = "allowlist"` — only approved groups are served.

This keeps the agent reachable only by approved identities.

## Memory model

- **Curated long-term memory** (`MEMORY.md`): distilled, human-readable facts and decisions — loaded only in the owner's main session.
- **Raw daily notes** (`memory/YYYY-MM-DD.md`): an append-only log of what happened each day.
- This split keeps the agent's context small while preserving continuity across restarts.

## Extending

Any local script can become a capability the agent calls from chat. The `scripts/` directory shows the two simplest patterns:

1. **Notify** — push a message to a Feishu group (webhook).
2. **Run task → report** — execute a local task and return its result to chat.

Compose these into pipelines (content generation, reporting, document sync, reminders) driven entirely by chat commands.
