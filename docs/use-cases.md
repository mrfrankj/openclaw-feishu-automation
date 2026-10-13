# Use Cases

Real patterns this setup is used for (sanitized). Each is a single chat command.

## 1. Document generation → Feishu
"Take `report.md` and create a Feishu doc with it, then share to the team group."
The agent reads the file, calls `feishu_doc` to create/append, then `feishu_perm` to share.

## 2. Content pipeline
"Run the video pipeline for the new product and post the result."
The agent calls a local pipeline script (ffmpeg/Pillow based), then reports back with the output.

## 3. Daily notes / memory
"Summarize today's work into the daily note."
The agent writes a structured entry to `memory/YYYY-MM-DD.md`, keeping continuity.

## 4. Scheduled reminders
"Remind me tomorrow at 9:00 to follow up with lead X."
The agent schedules a wake event; the reminder fires in chat at the right time.

## 5. Environment helper
"Set up the LAN proxy so my phone can use this machine's tunnel."
The agent runs a prepared script and reports the resulting IP/port.

## 6. Knowledge-grounded Q&A
"According to our internal docs, what's our refund policy?"
The agent queries a private RAG knowledge base and answers with citations — no data leaves the machine.

---

Common thread: **the chat is the interface; the machine does the work; the memory keeps context.**
