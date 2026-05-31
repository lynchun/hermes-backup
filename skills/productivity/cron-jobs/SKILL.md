---
name: cron-jobs
description: "Patterns, pitfalls, and proven recipes for Hermes cron jobs — no_agent scripts, delivery targets, watchers, and debugging."
version: 1.0.0
---

# Cron Jobs — Patterns & Pitfalls

Use when creating, debugging, or modifying Hermes cron jobs.

## Critical Pitfalls

### `deliver=origin` does NOT work for CLI sessions

Cron jobs with `deliver=origin` can only resolve a delivery target when there's an active gateway session (Telegram, Discord, etc.). In CLI-only contexts, the scheduler logs `no delivery target resolved for deliver=origin` and the output is lost.

**Fix:** Use `deliver=telegram:<chat_id>` for Telegram delivery, or `deliver=local` (saves to disk only) then have the agent poll the output directory.

### no_agent bash scripts: avoid pipe-to-Python patterns

Bash scripts that pipe to `python3 -c "..."` often fail with SIGPIPE (exit 141) when run by the cron scheduler, even though they work fine in a terminal. The pipe breaks silently and the output is lost.

**Fix:** Write the script as standalone Python (`.py` extension). The cron scheduler runs `.py` files with `sys.executable` (same Python as the gateway), and error handling is explicit.

### Debugging silent cron failures

Cron output files live at `~/.hermes/cron/output/<job_id>/`. Each file is named by timestamp. Check `Status:` field — `script failed` means non-zero exit, `silent (empty output)` means the script ran but produced no stdout.

For no_agent scripts: add `print()` statements that log what the script found (e.g., `[HH:MM:SS] N new messages`). This appears in the cron output file and makes debugging trivial.

## Proven Patterns

### iMessage/new-message watcher

Two-file pattern for polling external data sources:

1. **State file** (`~/.hermes/.imsg_last_check`) — stores the last-seen timestamp
2. **Inbox file** (`~/.hermes/.imsg_inbox`) — stores new items found since last check

The watcher script:
- Reads state file for last checkpoint
- Writes new checkpoint immediately (so next run has a baseline)
- Polls data source for items newer than checkpoint
- Writes any new items to inbox file
- Prints summary to stdout (visible in cron output)

This pattern works for any polling-based watcher: messages, RSS feeds, file changes.

### Gateway health watchdog

no_agent script that checks if Hermes gateway is running and sends a direct Telegram alert if not. Must bypass the gateway itself (use direct Telegram Bot API curl call) since the gateway is what's dead.

Script location: `~/.hermes/scripts/gateway-watchdog.sh`
Schedule: `every 15m`, no_agent=true, deliver=telegram:<chat_id>

## Reference Files

- `references/imsg-watcher.py` — Full iMessage polling script
- `references/gateway-watchdog.sh` — Gateway health check script
