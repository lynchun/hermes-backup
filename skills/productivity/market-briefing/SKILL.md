---
name: market-briefing
description: Compile daily market briefings — collect US index data, commodities, financial news, API credit balances, and social commentary from X/Twitter using browser + terminal tools. Includes bot-detection workarounds for financial data sources.
---

# Market Briefing

Collect financial market data, news headlines, API balances, and social commentary into a structured daily briefing. Designed for cron-job execution (no user present, no clarifying questions).

## Sources That Work 

| Source | Method | Notes |
|--------|--------|-------|
| **Yahoo Finance** | `browser_navigate(url)` | Works reliably. Index data on homepage; individual tickers via `/quote/TICKER/`. No login needed. |
| **CNBC Markets** | `browser_navigate(url)` | Works. Index data + market movers. Accepts automated access. |
| **Bloomberg RSS** | `terminal(curl)` | `curl -s https://feeds.bloomberg.com/markets/news.rss` — **WORKS**. Full article titles, descriptions, dates. No captcha. Preferred over direct Bloomberg.com. |
| **Google News RSS** | `terminal(curl)` | Bypasses bot blocks for any source. `curl -s "https://news.google.com/rss/search?q=site:reuters.com"` or `site:zerohedge.com`. |
| **API Balances** | `terminal()` via curl | DeepSeek: `curl -s https://api.deepseek.com/user/balance -H "Authorization: Bearer $KEY"`. OpenRouter: `curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $KEY"`. |

## Sources That Block 

| Source | Issue | Workaround |
|--------|-------|------------|
| **X/Twitter** | Login wall requires auth | Use **xurl CLI** (load skill `xurl`): `xurl search "from:fundstrat"`, `xurl search "from:DaveHcontrarian"`. Or navigate browser without login — only cached posts show. |
| **Bloomberg.com** | CAPTCHA/Cloudflare | Use Bloomberg RSS feed instead (`feeds.bloomberg.com/markets/news.rss`) |
| **Reuters** | CAPTCHA/DataDome | Use Google News RSS for reuters.com |
| **Google Search** | CAPTCHA | Blocked |
| **Bing Search** | Cloudflare | Blocked |
| **DuckDuckGo** | CAPTCHA | Blocked |
| **Investing.com** | Cloudflare | Blocked |

## User Profile & Filtering (Lyndon's Investment Style)

This briefing is curated for Lyndon Arthurson, an investment adviser and portfolio manager. His approach:

- **High-level macro focus** — secular cycles, big picture. Not stock-picking.
- **Follows David Hunter** — cycle-based, long trends run very long (secular super-cycle view).
- **Follows Tom Lee / Fundstrat** — data-driven but accessible macro calls.
- **Behavioural finance lens** — mean reversion / probabilistic. "Buy when blood in streets, sell when euphoria." But respects momentum — trends can persist (secular cycle view).
- **Technical timing matters** — Fibonacci levels, support/resistance.
- **Core holdings** — precious metals (SILJ, GDX, GDXJ), TLT/TMF for late-cycle bond plays.

**Filter news for:** macro themes, commodities (especially gold/silver), precious metals miners, Fed/rates, Iran/oil geopolitics, secular cycle calls, late-cycle indicators. De-prioritise: single-company news, micro caps, sector rotation within tech.

## Newsletter Fallback

If the user wants Bloomberg newsletters (Markets Daily, Open, Close) ingested:
1. Use a mail-to-RSS service (kill-the-newsletter.com or similar)
2. Generate a unique address
3. User updates Bloomberg account to send newsletters there
4. Poll as an RSS feed like any other source
As of May 2026 this is not yet set up — RSS feed covers equivalent content.

## Companion Skills

Always load these if the briefing includes their content:
- **`xurl`** — X/Twitter API access. Required for Tom Lee (@fundstrat) and Dave Hunter (@DaveHcontrarian) commentary.
- **`hermes-agent`** — Only if configuring/modifying the cron job itself.

## Data Collection Workflow

### Core Rules (User Preference)

1. **NEVER fabricate reasons for market moves.** Only report sourced explanations. If no sourced reason is found — just report the number without commentary. This was a direct user correction.
2. **Always state the data date.** Distinguish "last close" from "overnight". US holidays (Memorial Day, July 4, Labor Day, Thanksgiving) mean data may be 3-4 days old.
3. **Only what was asked — nothing extra.** Indices: S&P 500, NASDAQ (no Dow, no Brent, no Russell unless asked). Commodities: gold, silver, WTI, SILJ, GDX. No extra indices or benchmarks.
4. **No editorializing.** Report the numbers and sourced moves. No commentary like "consider topping up," "maps to your thesis," "Your positioning aligns," or "action needed." Just the facts.
5. **No ticker annotations.** Don't append labels like "← Junior silver miners", "← Senior gold miners", or "← WATCHLIST" to data points. The ticker is self-explanatory.
6. **No Watchlist section.** The user opens articles manually when interested. Do not include an "Articles Worth Opening" or "Watchlist" section at the end.
7. **Deliver as concise, scannable plain text** suitable for terminal reading. Remove filler lines. One-line-per-item where possible.

### Step 1: Market Data (TradingView Watchlist — PRIMARY)

Lyndon's TradingView watchlist contains all needed symbols in one page:
```
browser_navigate("https://www.tradingview.com/watchlists/24551192/")
```
The snapshot yields: SPY, NDX, VIX, GOLD, SILVER, SILJ, GDX, GDXJ, DXY, TLT, TMF — all with last price and % change. Extract what's needed from the snapshot. This replaces navigating to 6 separate Yahoo Finance pages.

**PITFALL — WTI vs Brent:** The TradingView watchlist does NOT include WTI crude. For WTI specifically, fall back to:
```
browser_navigate("https://finance.yahoo.com/quote/CL=F/")
```
Do NOT use Brent Crude. The Yahoo Finance homepage ticker bar also only shows Brent — do not grab it from there. WTI only, via CL=F.

**Fallback:** If TradingView fails or requires login, use Yahoo Finance homepage as backup:
```
browser_navigate("https://finance.yahoo.com/")
```
Read S&P 500, NASDAQ, VIX, Gold from the top bar. Then navigate to individual tickers for Silver (SI=F), SILJ, GDX. Same WTI rule applies.

### Step 3: API Balances
From terminal:
```bash
# OpenRouter
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(grep OPENROUTER_API_KEY ~/.hermes/.env | cut -d= -f2)"

# DeepSeek
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $(grep DEEPSEEK_API_KEY ~/.hermes/.env | cut -d= -f2)"
```

### Step 4: Market Headlines
Yahoo Finance homepage shows headlines from multiple sources (Bloomberg, Reuters, AFP, FT, Yahoo). Scroll down to read them. Key sections:
- Top banner story (latest big move driver)
- "Latest News" section with multi-source aggregation

### Step 5: X/Twitter Commentary (Tom Lee, Dave Hunter)
Load the `xurl` skill, then:
```
xurl search "from:fundstrat"
xurl search "from:DaveHcontrarian"
```

### Step 6: Check Market Calendar
Before reporting "yesterday's close", check if today is a US market holiday:
- Memorial Day (last Monday of May)
- Independence Day (July 4)
- Labor Day (first Monday of September)
- Thanksgiving (fourth Thursday of November)
- If holiday, the "most recent close" may be 3-4 days old.

## Market Driver Identification
The day's key driver is usually visible from:
1. The top headline on Yahoo Finance
2. The biggest % mover (often oil, VIX, or a sector ETF)
3. Check: Iran deal headlines (oil), Fed/rates stories (bonds), inflation data

## Primary Data Source: TradingView Watchlist

Lyndon's watchlist at https://www.tradingview.com/watchlists/24551192/ (28 symbols) is the primary one-hit data source. See `references/tradingview-watchlist.md` for full symbol list and notes. One `browser_navigate` call replaces 6+ Yahoo Finance page loads.

**What's missing from watchlist:** WTI Crude only. Fetch via `CL=F` on Yahoo Finance. Do NOT substitute Brent.

## Pitfalls
- **X/Twitter login wall**: Do NOT waste browser time trying to access x.com without auth. Load the `xurl` skill and use the CLI. **Fallback**: Google News RSS search works for finding recent articles quoting Tom Lee or Dave Hunter: `curl -s "https://news.google.com/rss/search?q=Tom+Lee+Fundstrat+market+outlook&hl=en-US&gl=US&ceid=US:en"`. Same pattern for Dave Hunter. Use this when xurl is unavailable.
- **Memorial Day**: US markets closed last Monday of May. If today is that Tuesday, reference is previous Thursday's close.
- **After-hours data**: Yahoo Finance shows "At close:" timestamp — check if it's the current day or stale.
- **SILJ/GDX stale dates**: These ETFs may show data from an earlier date if you access outside trading hours. Note the date in your briefing.
- **Balance parsing**: DeepSeek returns `{"balance_infos":[{"currency":"USD","total_balance":"1.64",...}]}`. OpenRouter returns `{"data":{"limit_remaining":9.98,...}}`. Parse accordingly.
- **WTI vs BRENT**: Yahoo Finance homepage ticker bar shows Brent Crude, NOT WTI. The user wants WTI only. Navigate to CL=F specifically. This was a direct correction — the agent reported Brent in a briefing and was corrected. Never grab oil data from the homepage bar. Fetch WTI from CL=F or the TradingView watchlist (which also lacks WTI — see references/tradingview-watchlist.md).
- **No user to ask**: This is a cron job. Make reasonable defaults. If data is unavailable, note it honestly rather than guessing or omitting.
- **VERBOSITY — user correction**: Keep it concise. No editorializing. No "consider topping up" or "maps to your thesis" commentary. No ticker annotations. No Watchlist. Just the numbers, sourced drivers, and headlines. One line per item where possible. The user will ask if they want more detail.
- **Only requested indices**: S&P 500 and NASDAQ only. No Dow, no Brent, no Russell unless explicitly asked. The skill says this — follow it.
