#!/bin/bash
# Gateway health watchdog — checks if the gateway is running and alerts if not.
# Designed to run as a no_agent cron job every 15 minutes.
#
# Reads Telegram credentials from .env and sends a direct
# API call if the gateway is down (bypasses the gateway itself).

set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
ENVFILE="$HERMES_HOME/.env"

# --- Check if gateway is running ---
# macOS: launchctl list (no label) shows PID in first column
PID=$(launchctl list 2>/dev/null | grep "ai.hermes.gateway" | awk '{print $1}')
if [ -n "$PID" ] && [ "$PID" != "-" ] && kill -0 "$PID" 2>/dev/null; then
    # Gateway is alive — silent exit (nothing to report)
    exit 0
fi

# Linux: systemd user service
if command -v systemctl &>/dev/null; then
    if systemctl --user is-active --quiet hermes-gateway 2>/dev/null; then
        exit 0
    fi
fi

# --- Gateway is DOWN — send Telegram alert ---

# Load .env if it exists
if [ -f "$ENVFILE" ]; then
    set -a
    source "$ENVFILE"
    set +a
fi

# Try to get bot token and chat ID
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="1505823420"  # @lyndonsgemma_bot

if [ -z "$BOT_TOKEN" ]; then
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
