# Gateway Watchdog

No-agent cron job that monitors gateway health and alerts via direct Telegram API when the gateway is down. The alert bypasses the dead gateway entirely.

## Script

Saved at `~/.hermes/scripts/gateway-watchdog.sh`:

```bash
#!/bin/bash
# Gateway health watchdog — checks if the gateway is running and alerts if not.
# Designed to run as a no_agent cron job every 15 minutes.

set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"
ENVFILE="$HERMES_HOME/.env"

# --- Check if gateway is running ---
# launchctl on macOS — 'launchctl list' (no label) shows PID in first column
PID=$(launchctl list 2>/dev/null | grep "ai.hermes.gateway" | awk '{print $1}')
if [ -n "$PID" ] && [ "$PID" != "-" ] && kill -0 "$PID" 2>/dev/null; then
    exit 0  # Gateway alive — silent
fi

# --- Gateway is DOWN — send Telegram alert ---
if [ -f "$ENVFILE" ]; then
    set -a; source "$ENVFILE"; set +a
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="1505823420"

if [ -z "$BOT_TOKEN" ]; then
    BOT_TOKEN=$(grep -A2 'telegram:' "$CONFIG" 2>/dev/null | grep 'token:' | head -1 | sed 's/.*token:\s*"\(.*\)"/\1/' || echo "")
fi

if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "null" ]; then
    echo "⚠️  GATEWAY DOWN — could not read bot token to send alert"
    exit 1
fi

MESSAGE="🔴 Hermes Gateway is DOWN%0A%0ALast checked: $(date '+%Y-%m-%d %H:%M:%S')%0A%0ARestart with: hermes gateway restart"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "text=${MESSAGE}" \
    -d "parse_mode=HTML" \
    -o /dev/null -w "%{http_code}" 2>/dev/null

exit 0
```

## Cron Job Setup

```
cronjob create
  name: "Gateway Health Watchdog"
  schedule: "every 15m"
  no_agent: true
  script: "gateway-watchdog.sh"
  deliver: "telegram:1505823420"
```

## Design Rationale

- **no_agent=true** — no LLM needed. A shell script is faster, cheaper, and more reliable for this.
- **Direct Telegram API** — the watchdog cannot use `send_message` tool or gateway delivery because the gateway is what it's monitoring. It curl-posts directly to api.telegram.org.
- **Silent on success** — empty stdout = no delivery. Only the failure case produces output, which cron delivers as an alert.
- **Token resolution** — falls back: .env → config.yaml → error. Covers both gateway and tool contexts.
