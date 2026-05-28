# Telegram Vision Crash — Root Cause & Fix

## Symptom

On Telegram (or any non-CLI platform), sending an image causes the agent to crash with:

```
Error code: 400 - unknown variant `image_url`, expected `text`
```

The session hits context overflow and the gateway skips transcript persistence.

## Root Cause

DeepSeek V4 Pro/Flash does NOT support native vision (multimodal `image_url` content blocks). When `vision_analyze` is called, Hermes falls back to an `auxiliary.vision` model. If `auxiliary.vision.provider` is set to `auto`, routing can fail — especially in gateway sessions where provider auto-detection resolves differently than in CLI.

In the Telegram gateway session, `auto` resolved to `openai-codex`, which tried to pass `deepseek-v4-pro` as the model. Codex doesn't support DeepSeek models, causing a 400 error that cascaded into context overflow.

## Fix

Pin the auxiliary vision provider explicitly to OpenRouter with a vision-capable model:

```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemini-2.5-flash
```

Then restart the gateway:

```bash
launchctl stop ai.hermes.gateway
sleep 2
launchctl start ai.hermes.gateway
```

## Why Gemini 2.5 Flash

- Cheap (~$0.10/M tokens)
- Fast
- Has native vision support
- Accessible via OpenRouter (already configured)

## Verification

After fix, send an image on Telegram. Gateway logs should show successful vision analysis, not a 400 error about `unknown variant image_url`.
