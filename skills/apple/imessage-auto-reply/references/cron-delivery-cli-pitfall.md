# Cron Delivery: CLI Gotcha

## The Problem

When a cron job uses `deliver=origin`, the scheduler resolves "origin" to the platform/chat where the user is currently active. This works for gateway platforms (Telegram, Discord, etc.) where there's a persistent chat session. But CLI sessions are ephemeral -- there's no persistent "origin" for the scheduler to route to.

Result: "no delivery target resolved for deliver=origin" warning on every tick. The cron script runs but output goes nowhere.

## The Fix

Use `deliver=local` for CLI-facing cron jobs. The script still runs and produces output, but delivery is suppressed. Instead, have the script write results to a known file that the agent can check during active sessions.

Pattern:
```bash
# Cron setup
deliver: local          # not 'origin'
no_agent: true

# Script writes to a known location
INBOX_FILE="$HERMES_HOME/.my_inbox"
```

The agent then periodically checks the inbox file during CLI sessions.

## When 'origin' DOES work

- Telegram: cron delivers to the Telegram chat
- Discord: cron delivers to the Discord channel
- Any platform with a persistent gateway session

## When 'origin' does NOT work

- CLI sessions (ephemeral, no persistent routing)
- API server contexts
- Any context without a gateway platform session
