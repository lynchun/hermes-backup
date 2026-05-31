---
name: hermes-operations
description: "Monitor, debug, and harden Hermes Agent infrastructure — gateway health, cron delivery, security sweeps, and platform evaluation."
version: 1.0.0
author: Epictetus
platforms: [macos, linux]
metadata:
  hermes:
    tags: [operations, monitoring, security, cron, gateway, debugging]
---

# Hermes Operations

Keeping Hermes running, monitored, and secure. Covers gateway health monitoring, cron delivery debugging, recurring security sweeps, and messaging platform evaluation.

## When to Use

- Gateway seems down or messages aren't delivering
- Cron job ran but user didn't receive output
- Setting up recurring infrastructure monitoring
- Evaluating a new messaging platform
- Hardening the Hermes install after a security audit

## Gateway Health Monitoring

The gateway can go down silently (update stops it, crash, launchd failure). Cron jobs will run but delivery fails with no visible error — the scheduler logs "delivered" but the gateway isn't there to push messages.

### Watchdog Pattern

Create a no_agent cron job that:
1. Checks if the gateway process is alive (via launchd on macOS, systemd on Linux)
2. If alive: exits silently (no message, no cost)
3. If dead: sends a direct Telegram API alert — bypassing the dead gateway entirely

See `references/gateway-watchdog.md` for the full script and setup.

Key design decisions:
- **no_agent=true** — no LLM needed, just a shell script
- **Direct Telegram API** — the watchdog CANNOT rely on the gateway it's monitoring
- **Silent on success** — only alerts on failure, otherwise invisible
- **Every 15 minutes** — frequent enough to catch outages, not noisy

### Pitfalls

- On macOS, `launchctl list <label>` prints plist JSON, not a PID table. Use `launchctl list | grep <label>` to get the PID.
- The watchdog itself depends on the cron scheduler. If both gateway AND cron scheduler die, no alert. Low probability but worth knowing.
- Token must be readable from config.yaml or .env. The script falls back through both.

## Cron Delivery Debugging

When a cron job says it ran but the user didn't get output:

### Diagnostic Pipeline

```
1. cronjob list → check last_run_at, last_status, last_delivery_error
2. ~/.hermes/logs/agent.log → grep for job_id, check "Turn ended" and "delivered"
3. ~/.hermes/logs/gateway.log → check for delivery events at that timestamp
4. ~/.hermes/cron/output/<job_id>/ → check if output file exists and has content
```

### Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "delivered" in agent.log, nothing in gateway.log | Gateway was down | Restart gateway, check watchdog |
| Output file exists but only has prompt, no briefing | Response was in preceding turn, file captured only closing line | Read the file, check response_len in agent.log |
| Job never ran | Scheduler was down or job was paused | Check gateway status, check job enabled/paused |
| Delivery logged but user didn't receive | Wrong deliver target, gateway platform paused | Check deliver field, check /platform status |

## Recurring Security Sweeps

Weekly or monthly automated security audit of the local machine. See `references/security-sweep.md` for the full prompt template.

### Pattern

- **Model:** Codex (GPT-5) — better at threat reasoning than DeepSeek
- **Schedule:** Weekly (Mondays) or monthly (1st of month)
- **Mode:** Read-only — never modify system state
- **Deliver:** Telegram

### What It Checks

1. Launch daemons/agents — unsigned, user-writable paths
2. Firewall state and listening ports — non-localhost exposure
3. System integrity — SIP, Gatekeeper, FileVault, updates
4. Remote access — SSH config, authorized keys
5. Persistence — crontabs, login items, kernel extensions
6. Applications — unsigned or recently added
7. Running services — Docker, Ollama, etc.

## Messaging Platform Evaluation

When deciding whether to add a new messaging platform:

### Framework

| Factor | Weight | Check |
|--------|--------|-------|
| Reach | High | Does it cover contacts not on existing platforms? |
| Stability | High | Official API or reverse-engineered bridge? |
| Setup complexity | Medium | One command or multi-step with permissions? |
| Maintenance burden | High | Does it break on upstream updates? |
| Ban/restriction risk | Critical | Unofficial bridges carry account risk |

### iMessage vs WhatsApp

| | iMessage | WhatsApp |
|---|---|---|
| **Reach** | iPhone users only | Everyone |
| **Setup** | `brew install imsg` + Full Disk Access | `hermes whatsapp` + QR scan |
| **Stability** | Native Messages.app — rock solid | Baileys bridge — breaks on protocol updates |
| **Maintenance** | None | Re-pair after WhatsApp updates |
| **Ban risk** | None | Small but real (unofficial API) |
| **Two-way** | Send-only via terminal | Full gateway (receive + respond) |
| **Messages from** | Your number | Your number |

**Recommendation:** iMessage first (zero maintenance, covers most contacts). WhatsApp as backup for universal reach.

### iMessage Setup

```bash
brew install steipete/tap/imsg
```

Required permissions (must be granted manually):
1. **Full Disk Access** — System Settings → Privacy & Security → Full Disk Access → add terminal app
2. **Automation** — prompts on first send, allow Terminal to control Messages.app

Usage:
```bash
imsg chats --limit 10 --json          # list recent chats
imsg send --to "+61400123456" --text "Hello"   # send message
imsg send --to "+61400123456" --text "Hi" --service sms  # force SMS
```

Pitfall: the terminal app that launches Hermes needs Full Disk Access. If Hermes runs via launchd (gateway), the Hermes venv Python binary may also need it.

## References

- `references/gateway-watchdog.md` — full watchdog script, design rationale, and cron setup
- `references/security-sweep.md` — weekly Codex-powered security audit prompt template
- `references/cron-delivery-debugging.md` — diagnostic pipeline for silent cron delivery failures
