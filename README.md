# Chat-Driven Automation with a Local AI Agent (OpenClaw + Feishu)

Turn repetitive knowledge work into **"say it in chat, and it's done."** A self-hosted AI agent wired to **Feishu (Lark)** takes natural-language commands from a chat and triggers real actions on a machine — grounded by a private knowledge base and a persistent memory.

> **No data leaves your infrastructure.** The agent, its memory, and its knowledge base all run on your own machine.

---

## Why

Repetitive work (document generation, batch processing, research, reporting) eats hours every week. Instead of clicking through steps or copy-pasting between apps, you type an instruction in chat — and the agent executes it, keeps a memory of what it did, and reports back in the same chat.

Typical wins:

- "Turn this file into a formatted Feishu doc and share it."
- "Summarize today's notes into `memory/2026-10-13.md`."
- "Run the content pipeline for the new product and post the result."
- "Remind me tomorrow 9am to follow up with client X."

## How it works

```
        Feishu (Lark) chat
                │  natural-language command
                ▼
     ┌───────────────────────┐
     │   OpenClaw agent      │  (self-hosted, always on)
     │  ─────────────────    │
     │  memory  (MEMORY.md,  │
     │           daily notes)│
     │  skills  (feishu_doc, │
     │           drive, exec)│
     │  knowledge base (RAG) │
     └───────────┬───────────┘
                 │ tool calls
                 ▼
   real actions on the machine
   (files, scripts, docs, APIs, schedules)
                 │
                 ▼
        result returned to chat
```

- **Chat front-end**: Feishu Open Platform, connected over a **WebSocket** long connection (no public IP / inbound port required).
- **Agent**: OpenClaw, running locally, with a **persistent memory** (curated long-term memory + raw daily notes) so context survives restarts.
- **Tools / skills**: document read/write (`feishu_doc`), cloud drive (`feishu_drive`), permissions (`feishu_perm`), wiki (`feishu_wiki`), plus shell execution, file I/O, web fetch, and scheduling.
- **Grounding**: an optional private **RAG** knowledge base so answers cite your own documents.

## Stack

`OpenClaw` · `Feishu / Lark Open Platform` · `WebSocket` · `Docker` · `Python` · `RAG` · `Automation scripts`

## Quickstart

```bash
# 1. Install OpenClaw (Node.js project)
npm install -g openclaw

# 2. Create a Feishu app in the Feishu Open Platform console,
#    enable the bot + the events you need, then configure the channel.
#    See config/openclaw.feishu.example.json for the shape (secrets redacted).

# 3. Start the gateway
openclaw gateway start

# 4. Open a DM with your bot and send a command, e.g.:
#    "Create a doc titled 'Weekly Report' and append today's summary."
```

## Repo layout

```
config/     # example (redacted) OpenClaw + Feishu channel config
scripts/    # small, standalone examples (webhook notify, task runner)
docs/       # architecture + real use cases
demo/       # 30s walkthrough (placeholder)
```

## What makes this useful

- **Runs unattended**: an always-on gateway plus scheduling means tasks fire without you watching.
- **Keeps context**: curated long-term memory + daily logs = the agent remembers decisions and preferences across sessions.
- **Extensible**: add any local script as a capability; the agent calls it from chat.

## Security notes

- Secrets (`app_id`, `app_secret`, API keys) live only in local config / env — **never** in this repo.
- Use Feishu **pairing** for DMs and an **allowlist** for groups, so only approved users can command the agent.
- The agent only acts on the machine it runs on; bring-your-own access scope.

---

*Built by [Kang Jiusheng](https://www.upwork.com/) — AI integration & agent automation.*
MIT License.
