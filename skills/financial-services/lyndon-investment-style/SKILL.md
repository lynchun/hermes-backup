---
name: lyndon-investment-style
description: "Lyndon's investment philosophy and market interests. Used for curating news, filtering Bloomberg articles, and framing market commentary."
---

# Lyndon's Investment Profile

## Role
Investment adviser, portfolio manager (AFSL). Australia-based (Sydney/GMT+11).

## Investment Philosophy
- **High-level macro focus** — secular cycles, big picture themes over individual stocks
- **David Hunter style** — cycle-based, believes trends run much longer than大多数人 expect
- **Tom Lee / Fundstrat** — data-driven but accessible, detail-oriented
- **Mean reversion + behavioural finance** — contrarian: buy blood in the streets, sell euphoria
- **Respects momentum** — trends can persist for years (secular cycles)
- **Technical timing** — Fibonacci levels play a role in entry/exit timing

## Core Holdings / Watchlist
- Precious metals: SILJ, GDX, GDXJ
- Late-cycle bond plays: TLT, TMF
- Macro trends: gold, silver, oil, commodities broadly

## News Filtering Rules
When curating Bloomberg/Reuters/ZeroHedge content, prioritise:
1. Macro themes (secular cycles, late-cycle indicators)
2. Precious metals (gold, silver, miners)
3. Commodities broadly (oil, copper — macro signals)
4. Fed / central bank policy
5. Iran/oil — geopolitical macro impacts
6. Behavioural finance angles (sentiment extremes)
7. Technical analysis references (fibonacci, key levels)

Flag anything directly relevant to SILJ, GDX, gold, or silver as "WATCHLIST" priority.

## Daily Briefing Format

When compiling the daily market briefing for Lyndon, follow these rules:

### Must include
- Date and data timestamp clearly stated
- US Markets: S&P 500 (SPY/SPX), NASDAQ (NDX), VIX — level and % change only. Sourced driver in one sentence.
- Commodities: Gold, Silver, WTI Crude (NOT Brent), SILJ, GDX — price and % change only. No unsourced commentary.
- Top 3-4 headlines from Bloomberg RSS + ZeroHedge. One-sentence summaries.
- Tom Lee (Fundstrat) latest — one line.
- Dave Hunter (contrarian) latest — one line.
- Credit balances: OpenRouter and DeepSeek. Numbers only, no advice.
- Projects: brief status, one line each.

### Must NOT include
- Watchlist / "articles worth opening" sections
- Editorialising: no "Consider topping up", "Your positioning maps to...", "This is bullish for you", no investment advice
- Data Lyndon didn't ask for (Dow 30, Russell 2000 unless specifically relevant)
- Extra labels on tickers ("← Junior silver miners", "← Senior gold miners")
- Long-form explanations of market dynamics — one-sentence drivers only
- Fluff, filler, verbose framing
- **NO editorial nudges.** If DeepSeek balance is low, state the number. Do NOT add "consider topping up" or similar. If a holding aligns with a market theme, state the data. Do NOT add "your positioning maps to this thesis."

### Data sources
- Primary: TradingView watchlist #24551192 (see `references/tradingview-watchlist.md` for full symbol list). One browser hit covers SPY, NDX, VIX, GOLD, SILVER, SILJ, GDX, GDXJ, DXY, TLT, TMF.
- Commodities: WTI via USOIL or CL=F. Brent is NOT wanted.
- **PITFALL:** Yahoo Finance homepage ticker bar only shows Brent Crude, not WTI. Do NOT grab Brent from the homepage bar — navigate to CL=F specifically for WTI.
- Bloomberg: curl RSS feed at feeds.bloomberg.com/markets/news.rss
- ZeroHedge: Google News RSS for site:zerohedge.com
- Credit balances: OpenRouter /api/v1/auth/key and DeepSeek /user/balance endpoints via terminal

### Pitfalls

- **Credit balances: query the actual API, never estimate or guess.** The user expects live numbers. Use the terminal tool to curl the endpoints with the respective API key env var in the auth header:
  - OpenRouter: GET https://openrouter.ai/api/v1/auth/key (Bearer auth)
  - DeepSeek: GET https://api.deepseek.com/user/balance (Bearer auth)
  If a balance number wasn't retrieved from the live API, don't present it as a fact. Say "could not retrieve."
- **Cron delivery: always verify `deliver` is set to `origin`**, not `local`. A `local` delivery writes output to disk silently — the user never sees it. When creating or updating a briefing cron job, explicitly confirm the delivery target.
- **Yahoo Finance ticker bar shows Brent, not WTI.** Navigate to CL=F specifically.

### Tone
- Clean, scannable, minimal. The user will tell you if they want more detail.
