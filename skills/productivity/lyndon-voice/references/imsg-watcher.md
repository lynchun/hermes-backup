# iMessage Watcher System

Polls iMessage for new incoming messages every 2 minutes.

## Architecture

- Script: `~/.hermes/scripts/imsg-watch.py` (Python, standalone)
- State: `~/.hermes/.imsg_last_check` (UTC timestamp)
- Inbox: `~/.hermes/.imsg_inbox` (JSON array of new messages)
- Flush: `~/.hermes/scripts/flush-pending.py` (resends missed cron deliveries)
- Cron: job `9efeab4aeefa`, `deliver=local`, `no_agent`, runs every 2min
- Tool: `/opt/homebrew/bin/imsg` (requires Full Disk Access for Terminal.app)

## Setup

```bash
brew install steipete/tap/imsg
# Grant Full Disk Access to Terminal.app in System Settings
```

## Debugging History

### SIGPIPE exit 141 (May 2026)
**Symptom:** Cron output files showed "script failed" with exit code 141. No messages detected.
**Root cause:** Bash script with `imsg chats | python3 -c "..."` pipe broke under cron scheduler's subprocess environment.
**Fix:** Rewrote as standalone Python script (`imsg-watch.py`) using `subprocess.run()` instead of pipe.

### deliver=origin silent failure (May 2026)
**Symptom:** Cron ran but "no delivery target resolved for deliver=origin". Lyndon never saw new messages.
**Root cause:** `deliver=origin` requires a persistent gateway session (Telegram, Discord). CLI sessions have no persistent delivery target.
**Fix:** Use `deliver=local` for no_agent scripts. Output saved to cron output directory. Flush manually or via flush-pending.py.

### Cron update race (May 2026)
**Symptom:** Updated cron from bash script to Python, but next tick still used old script.
**Root cause:** Scheduler may dispatch a tick before the job update is committed.
**Fix:** Wait one tick cycle before assuming the update took effect.

### Gateway offline = crons don't fire (May 2026)
**Symptom:** When laptop lid closed or sleeping, no cron jobs execute at all (not just delivery failure).
**Root cause:** Cron scheduler runs inside the gateway process. Gateway stops when system sleeps.
**Fix:** `sudo pmset -c sleep 0` prevents sleep on AC power. Also: flush-pending.py resends any missed reports when gateway comes back online.

### Codex model name invalid (May 2026)
**Symptom:** All Codex API calls failed: "The 'gpt-5.1-codex-max' model is not supported when using Codex with a ChatGPT account."
**Root cause:** `gpt-5.1-codex-max` is not a real Codex model. Valid Codex models: `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex`, `gpt-5.3-codex-spark` (Pro only), `gpt-5.2-codex`.
**Fix:** `hermes config set model.default gpt-5.3-codex`. Update all cron job model overrides to match.
