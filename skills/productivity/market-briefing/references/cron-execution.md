# Cron Execution Notes (Updated May 2026)

## The Cron Job

Job ID: `80a62658b3c1`
Schedule: `0 8 * * 1-5` (weekdays at 8am Sydney)
Delivery: `local` (saves to session)
Skills loaded: `lyndon-investment-style`

The `lyndon-investment-style` skill provides the investment philosophy lens. The cron prompt itself contains the full data-collection workflow (TradingView watchlist, Bloomberg RSS, credit balances, Tom Lee/Dave Hunter via Google News RSS).

## Delivery

Delivery is `local` — the briefing is saved to the session store and visible when the user opens Hermes. Telegram delivery was attempted but not yet working reliably via cron (the cron `run` command's `deliver` parameter does not override the job's stored delivery setting — you must `update` the job to change delivery, then `run`).

To test Telegram delivery: update the job to `deliver=telegram:1505823420`, run it, then switch back to `deliver=local`.

## Data Sources (What Works)

| Source | Method |
|--------|--------|
| TradingView watchlist #24551192 | `browser_navigate` — one call gets SPY, NDX, VIX, GOLD, SILVER, SILJ, GDX, GDXJ, DXY, TLT, TMF |
| WTI Crude (CL=F) | `browser_navigate` to Yahoo Finance CL=F — NOT in TradingView watchlist |
| Bloomberg headlines | `curl -s https://feeds.bloomberg.com/markets/news.rss` |
| ZeroHedge | `curl` Google News RSS for site:zerohedge.com |
| Tom Lee / Dave Hunter | Google News RSS search (fallback when xurl unavailable) |
| Credit balances | `terminal()` with curl to OpenRouter + DeepSeek API endpoints |

## What Changed (from earlier versions)

- **TradingView watchlist** replaced Yahoo Finance homepage + 6 individual ticker pages. One browser call instead of 7.
- **Bloomberg RSS** replaced Bloomberg.com direct access (was CAPTCHA-blocked).
- **Google News RSS fallback** for Tom Lee/Dave Hunter when xurl is unavailable.
- **Credit balances** added — OpenRouter `limit_remaining` and DeepSeek `balance_infos[0].total_balance`.
- **Briefing format simplified** — concise, no watchlist section, no editorializing, WTI only.
