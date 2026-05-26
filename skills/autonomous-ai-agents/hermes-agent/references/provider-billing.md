# Checking Provider Billing

When the user asks about actual spend/costs, **don't estimate** — retrieve real data.

## DeepSeek

No public billing API. Options:

1. **Browser (if Chrome remote debugging active):** Navigate to `https://platform.deepseek.com/usage` using the user's logged-in session via `mcp_peekaboo_browser`
2. **Ask the user** to read numbers from their billing dashboard
3. **Hermes insights** (`hermes insights --days N`) gives token counts per model, but NOT dollar cost — multiply by DeepSeek's current published rates as a last resort, but flag it as an estimate and cite the rate you used

DeepSeek pricing as of May 2026 (check for updates):
- deepseek-chat: ~$0.27/M input, $1.10/M output
- deepseek-v4-flash: cheaper than chat
- deepseek-v4-pro: premium tier

## OpenAI / Anthropic / OpenRouter

These platforms typically have usage APIs. Check provider docs, or use the browser approach above.
