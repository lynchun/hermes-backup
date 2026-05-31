---
name: messaging-automation
description: "Automated messaging workflows — iMessage watchers, auto-reply rules, voice/persona matching, and cron-based polling patterns for messaging platforms."
version: 1.0.0
author: Epictetus
platforms: [macos]
metadata:
  hermes:
    tags: [messaging, iMessage, cron, automation, voice]
    related_skills: [imessage]
---

# Messaging Automation

Patterns for setting up automated messaging workflows: watchers that poll for new messages, auto-reply rules with voice matching, and cron-based reliability patterns. Currently covers iMessage; WhatsApp and other platforms will be added as they're set up.

## When to Load

- Setting up a new messaging platform watcher or auto-responder
- Debugging a cron-based watcher that isn't detecting messages
- Adding auto-reply rules with persona/voice matching
- User asks to "watch for replies" or "auto-respond for me"

## iMessage Watcher Pattern

### Prerequisites

```bash
brew install steipete/tap/imsg
```

Requires Full Disk Access for the terminal app running Hermes (System Settings → Privacy → Full Disk Access). The `imsg` CLI reads `~/Library/Messages/chat.db` directly.

### Architecture

```
┌─────────────┐    every 2min    ┌──────────────┐    writes    ┌──────────────┐
│ cron runner  │ ───────────────→ │ imsg-watch.py │ ──────────→ │ .imsg_inbox   │
│ (no_agent)   │                 │  (Python)      │            │ (JSON array)  │
└─────────────┘                  └──────────────┘             └──────────────┘
                                       │
                                  reads/writes
                                       │
                                  ┌──────────────┐
                                  │ .imsg_last_   │
                                  │ check (UTC ts)│
                                  └──────────────┘
```

- State file (`~/.hermes/.imsg_last_check`): UTC timestamp of last poll
- Inbox file (`~/.hermes/.imsg_inbox`): JSON array of new incoming messages
- Agent checks inbox proactively during active sessions or when user asks

### Cron Setup

```bash
cronjob(action='create', name='iMessage Watcher', schedule='every 2m',
         script='imsg-watch.py', no_agent=True, deliver='local')
```

Use `deliver='local'` — the script writes to the inbox file rather than relying on cron delivery. Delivery to `origin` does NOT work for CLI sessions (only gateway platforms like Telegram).

### Auto-Reply Rules

When the agent detects a new message in the inbox, it:

1. Identifies the contact and context
2. Drafts a reply in the user's voice (see voice patterns below)
3. Presents the draft for approval (NEVER send without approval)
4. On approval, sends via `imsg send`

Exception: for low-stakes, well-defined patterns (e.g., "if Ma proposes cafe time between 10am-11:30am, reply 'Ok'"), the user may authorize direct auto-reply.

### Voice Patterns (Lyndon)

- **Casual Australian**: "mate", "dude", "bro", "outta"
- **Warm but efficient**: names people, gets to the point
- **Emoji user**: 😊 😅 🧐 😂
- **Relationship-context-aware**:
  - **Mum (Ma):** Brief, practical, uses "u" instead of "you"
  - **Close friends:** Banter, jokes, "bro"/"dude"
  - **Acquaintances:** Full sentences, thoughtful, polite
- **Self-deprecating humor**, never too formal
- **Message length varies**: short with family, longer when giving advice

### Sending Messages

```bash
# Send text
imsg send --to "+614XXXXXXXX" --text "your message"

# List chats to find contacts
imsg chats --limit 30 --json

# View recent history for a chat
imsg history --chat-id <id> --limit 10 --json
```

## Cron Script Reliability

### Pitfall: Bash Pipes → SIGPIPE (exit 141)

Bash scripts that pipe `imsg | python3 -c "..."` silently fail with exit 141 (SIGPIPE) when run by the cron scheduler, even though they work when run manually from a terminal. The pipe breaks because the cron subprocess environment handles stdio differently.

**Fix:** Use standalone Python scripts (`.py`) instead of bash scripts with embedded Python. The cron scheduler runs `.py` files with `sys.executable` (the Hermes venv Python), sets `HERMES_HOME`, and properly captures stdout/stderr.

### Pitfall: Working Manually ≠ Working in Cron

Scripts that work perfectly in `bash script.sh` or `python3 script.py` from an interactive terminal may fail silently under the cron scheduler. Always test with the exact cron environment:

```bash
# Simulate cron execution
HERMES_HOME=~/.hermes ~/.hermes/hermes-agent/venv/bin/python3 ~/.hermes/scripts/your-script.py
```

### Add Logging from the Start

Every cron watcher script should:
1. Print status to stdout (visible in `~/.hermes/cron/output/<job_id>/` files)
2. Log errors to stderr
3. Wrap `main()` in try/except with `sys.exit(1)` on failure

This makes debugging trivial — the cron output file shows exactly what happened.

## Templates

See `templates/imsg-watch.py` for the reference iMessage watcher implementation. Copy and adapt for new messaging platforms.

## Pitfalls

- **`deliver='origin'` does not work for CLI sessions.** Use `deliver='local'` and have the agent check the inbox file.
- **imsg requires Full Disk Access** for the process reading `~/Library/Messages/chat.db`. The cron scheduler runs as a subprocess of the gateway (launchd user agent), which inherits user TCC permissions.
- **imsg chats are sorted by `last_message_at` descending.** The watcher can break early once it hits a chat older than the last checkpoint.
- **State file timestamp granularity matters.** If the watcher runs at the same second as an incoming message, sub-second ordering can cause missed messages. Round checkpoint timestamps conservatively.
- **Never auto-send without approval** unless the user has explicitly authorized a specific auto-reply rule for that contact and scenario.
