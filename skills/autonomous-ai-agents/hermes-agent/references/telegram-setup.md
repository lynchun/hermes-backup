# Telegram Gateway Setup

## Quick Setup

1. Create bot with @BotFather on Telegram: `/newbot`
2. Add token to `.env`: `TELEGRAM_BOT_TOKEN=<token>`
3. Enable in `config.yaml`:
   ```yaml
   platforms:
     telegram:
       enabled: true
   ```
4. Lock to specific users: `TELEGRAM_ALLOWED_USERS=<user_id>` in `.env`
5. Restart gateway

## Activation Check

Look for `✓ telegram connected` in gateway logs. If missing:
- Verify token is correct
- Check `platforms.telegram.enabled: true` in config.yaml
- Restart gateway completely (`launchctl stop/start` on macOS)

## Vision/Image Support

Telegram uses the same model as CLI. If the main model lacks vision (e.g. DeepSeek):
```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemini-2.5-flash
```

## Common Issues

### Bot silent / no response
- Check `TELEGRAM_ALLOWED_USERS` — must include your user ID
- Or set `GATEWAY_ALLOW_ALL_USERS=true` temporarily (remove after getting user ID)
- User ID found in gateway logs: `[Telegram] Sending response (N chars) to <user_id>`

### Platform auto-paused
After 10 consecutive connection failures, Telegram auto-pauses. Gateway log shows:
`telegram paused after 10 consecutive failures`
Fix: restart gateway or `/platform resume telegram`

### Context overflow on Telegram
Long voice/image sessions can overflow context. User should send `/new` on Telegram to reset.
