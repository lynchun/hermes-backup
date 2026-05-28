# Telegram Vision + Model Configuration

## The Problem

When a user sends an image to Hermes on Telegram, the vision tool fails because:
1. DeepSeek V4 Pro/Flash do NOT support native vision (no `image_url` content type)
2. The auxiliary vision fallback (`auxiliary.vision.provider`) defaults to `auto`, which routes unreliably
3. On Telegram gateway sessions, the auto-detection may pick the wrong provider (e.g., `openai-codex` instead of `openrouter`), causing:
   - `HTTP 400: unknown variant 'image_url', expected 'text'`
   - `HTTP 400: The 'deepseek-v4-pro' model is not supported when using Codex`

## The Fix

Pin both the auxiliary vision provider and model explicitly:

```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemini-2.5-flash
```

Restart the gateway after:
```bash
launchctl stop ai.hermes.gateway
sleep 2
launchctl start ai.hermes.gateway
```

## Gateway Session Diagnostics

When Telegram sessions crash, check:
```bash
# Recent gateway logs
tail -30 ~/.hermes/logs/gateway.log | grep -i 'telegram\|error'

# Error log for crashes
tail -30 ~/.hermes/logs/gateway.error.log

# Check if gateway is running
launchctl list | grep hermes

# Full restart if needed
launchctl stop ai.hermes.gateway && sleep 2 && launchctl start ai.hermes.gateway
```

## Context Overflow

Telegram sessions can hit context overflow during long conversations. The gateway logs `Skipping transcript persistence for context-overflow failure`. Fix: user sends `/new` to reset the session. Voice messages with vision/Peekaboo calls accelerate context growth.

## Locking Down

After initial setup, lock Telegram to specific user IDs:
```bash
echo "TELEGRAM_ALLOWED_USERS=1505823420" >> ~/.hermes/.env
```
Replace with actual user ID from gateway logs (`user=Lyndon chat=#######`).
Remove `GATEWAY_ALLOW_ALL_USERS=true` if temporarily set during setup.

## Lyndon's Setup

- User ID: 1505823420
- Bot: @lyndonsgemma_bot (token in .env)
- Vision: auxiliary.vision → openrouter/google/gemini-2.5-flash
- Telegram locked to user only
- Gateway runs via launchd (ai.hermes.gateway.plist)
