---
name: hermes-reliability
description: "Monitor Hermes gateway health, detect silent cron delivery failures, and maintain operational reliability. Use when debugging 'I didn't get my briefing' or setting up health checks."
version: 1.0.0
platforms: [macos, linux]
---

# Hermes Reliability

Operational patterns for keeping Hermes running reliably -- gateway health
monitoring, cron delivery verification, and silent-failure detection.

## Trigger Conditions

- User reports a cron job didn't deliver ("where's my briefing?")
- Setting up a new Hermes install or profile
- After a `hermes update` -- verify gateway came back up
- Debugging missing cron deliveries

## The Silent Delivery Failure

The most common reliability failure mode: **cron ran, scheduler logged "delivered",
but the user never received anything.**

Root cause: the gateway was offline. The cron scheduler hands off delivery to
the gateway, and if the gateway isn't running, the message evaporates. The
scheduler doesn't queue or retry -- it logs "delivered" optimistically.

### Diagnosis

```bash
# 1. Check if the cron job ran
grep "JOB_ID" ~/.hermes/logs/agent.log | grep "Turn ended"

# 2. Look for delivery confirmation
grep "JOB_ID.*deliver" ~/.hermes/logs/agent.log

# 3. Cross-reference: was the gateway running at that time?
grep "HH:MM" ~/.hermes/logs/gateway.log

# If agent.log says "delivered" but gateway.log has no entries for that hour,
# the gateway was down. The message was lost.
```

### Recovery

The cron output is cached at `~/.hermes/cron/output/<job_id>/` -- the most
recent `.md` file contains the generated content. Re-run with:

```bash
# In-session:
cronjob(action="run", job_id="...")
```

## Gateway Health Watchdog

Prevent silent failures by monitoring gateway health independently.

### Pattern: no_agent cron + direct Telegram API

A working reference script is bundled with this skill at
`scripts/gateway-watchdog.sh`. It handles both macOS (launchd) and Linux
(systemd) gateway detection.

Create a watchdog script at `~/.hermes/scripts/gateway-watchdog.sh`:

```bash
#!/bin/bash
set -euo pipefail

# Check if gateway process is running
# macOS launchd:
PID=$(launchctl list 2>/dev/null | grep "ai.hermes.gateway" | awk '{print $1}')
if [ -n "$PID" ] && [ "$PID" != "-" ] && kill -0 "$PID" 2>/dev/null; then
    exit 0  # alive, silent
fi

# Linux systemd:
# systemctl --user is-active --quiet hermes-gateway && exit 0

# Gateway is DOWN -- send alert via direct Telegram API
# (bypasses the dead gateway)
source ~/.hermes/.env 2>/dev/null || true
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="YOUR_CHAT_ID"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "text=🔴 Hermes Gateway is DOWN%0A%0A$(date)" \
    -o /dev/null
```

Then register as a no_agent cron job:

```
cronjob(
    action="create",
    name="Gateway Health Watchdog",
    schedule="every 15m",
    script="gateway-watchdog.sh",
    no_agent=true,
    deliver="telegram:CHAT_ID"
)
```

Key design points:
- **no_agent=true** -- no LLM cost, just runs the script
- **Direct Telegram API** -- bypasses the dead gateway entirely; can't fail
  because its target is down
- **Silent on success** -- empty stdout = no message delivered (the watchdog
  pattern). Only alerts when something is wrong
- **Every 15 minutes** -- frequent enough to catch outages quickly, infrequent
  enough to not spam

### Pitfalls

- **macOS `launchctl list <label>` vs `launchctl list | grep`**: On macOS,
  `launchctl list ai.hermes.gateway` returns the plist contents (JSON-like),
  not a table with PID. Use `launchctl list | grep <label> | awk '{print $1}'`
  to get the PID.
- **Watchdog depends on the cron scheduler**: if the scheduler itself goes
  down, the watchdog can't fire. This is rare but possible after updates.
  After `hermes update`, always verify the gateway restarted.
- **Token placement**: the watchdog reads `TELEGRAM_BOT_TOKEN` from `.env`.
  Ensure it's set there and not just in `config.yaml` under
  `platforms.telegram.token` (which shell scripts can't easily parse).

## Post-Update Verification

After `hermes update`, always verify:

```bash
# Check gateway is running
hermes gateway status

# Check cron scheduler is running
hermes cron list

# Verify recent cron deliveries
grep "deliver" ~/.hermes/logs/agent.log | tail -5
```

The update process stops the gateway. On macOS (launchd), the service restarts
automatically if OnDemand is set. On Linux (systemd), Restart=on-failure
handles it. But edge cases happen -- verify manually.
