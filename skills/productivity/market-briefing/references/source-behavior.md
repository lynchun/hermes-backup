# Source Behavior Reference

Behavioural notes from actual testing across multiple sessions (May 2026).

## Yahoo Finance
- **URL**: `https://finance.yahoo.com/`
- **Status**: Works. No CAPTCHA, no login wall.
- **Index data**: Visible in top bar on homepage refresh. Prices update ~15s delayed.
- **Individual tickers**: `/quote/SI=F/`, `/quote/CL=F/`, `/quote/SILJ/`, `/quote/GDX/`, `/quote/%5EGSPC/`
- **Data shape** (from accessibility snapshot):
  ```
  S&P 500    → "7,473.47"  "+27.75 +0.37%"
  Dow 30     → "50,579.70" "+294.00 +0.58%"
  Nasdaq     → "26,343.97" "+50.87 +0.19%"
  Gold       → "4,574.50"  "+51.30 +1.13%"
  Brent      → "93.92"     "-6.29 -6.28%"
  ```
- **News headlines**: Listed on homepage with source attribution (Bloomberg, Reuters, AFP, FT). Article links redirect to Yahoo 404 when clicked programmatically — read from homepage snapshot only, don't try to open individual articles.
- **Ticker data is delayed**: Shows "At close:" timestamp. For SILJ/GDX, can be several days stale if ETF markets close earlier than indices.

## DeepSeek Balance API
- **URL**: `https://api.deepseek.com/user/balance`
- **Auth**: `Authorization: Bearer <DEEPSEEK_API_KEY>`
- **Response shape**:
  ```json
  {
    "is_available": true,
    "balance_infos": [{
      "currency": "USD",
      "total_balance": "1.64",
      "granted_balance": "0.00",
      "topped_up_balance": "1.64"
    }]
  }
  ```
- **Parse**: `data["balance_infos"][0]["total_balance"]`
- **Key location**: `DEEPSEEK_API_KEY` in `~/.hermes/.env`

## OpenRouter Balance API
- **URL**: `https://openrouter.ai/api/v1/auth/key`
- **Auth**: `Authorization: Bearer <OPENROUTER_API_KEY>`
- **Response shape**:
  ```json
  {
    "data": {
      "label": "sk-or-v1-fd0...49b",
      "limit": 10,
      "limit_reset": "weekly",
      "limit_remaining": 9.98,
      "usage": 0.056,
      "usage_weekly": 0.018,
      "usage_monthly": 0.056
    }
  }
  ```
- **Parse**: `data["data"]["limit_remaining"]` for remaining credit, `data["data"]["usage_weekly"]` for usage
- **Key location**: `OPENROUTER_API_KEY` in `~/.hermes/.env`
- **WARNING**: This endpoint returns credit *limit* info, not a dollar balance. The `limit` field ($10/week) is the budget cap, `limit_remaining` is what's left of the cap.

## X/Twitter
- **URL**: `https://x.com/zerohedge`, `https://x.com/fundstrat`, `https://x.com/DaveHcontrarian`
- **Status**: Login wall. Shows "Don't miss what's happening" with sign-up prompt. No posts visible without authentication.
- **Recommended tool**: Load `xurl` skill and use `xurl search "from:fundstrat"` or `xurl search "from:zerohedge"`.
- **Do NOT waste browser rounds** trying to access x.com — it always shows login wall.

## Google Search
- **Status**: Blocked. Returns CAPTCHA page with "We've detected unusual activity."
- **URL after block**: `https://www.google.com/sorry/index?continue=...`

## Bing Search
- **Status**: Blocked. Returns Cloudflare challenge page.
- Shows "One last step — Please solve the challenge below to continue."

## DuckDuckGo (HTML mode)
- **URL**: `https://html.duckduckgo.com/html/?q=...`
- **Status**: Blocked. Returns CAPTCHA checkboxes.

## Bloomberg Markets
- **URL**: `https://www.bloomberg.com/markets`
- **Status**: Blocked. "Are you a robot?" page with CAPTCHA challenge.

## Reuters Markets
- **URL**: `https://www.reuters.com/markets/`
- **Status**: Blocked. DataDome CAPTCHA.

## CNBC Markets
- **URL**: `https://www.cnbc.com/markets/`
- **Status**: Works. No CAPTCHA or login. Shows index data, market movers, and news articles.
- Index table includes: S&P 500, NASDAQ, DJIA, FTSE, NIKKEI, HSI, SHANGHAI, VIX, DAX.
- Data shows timestamp: e.g. "FRI, MAY 22 2026 • 8:00 PM EDT"

## Market Holiday Awareness
- **Memorial Day**: Last Monday of May. In 2026: May 25.
  - If briefing runs on Tuesday May 26, reference data is from Thursday May 22.
  - Don't report "yesterday's close" — say "last close before the long weekend."
- **Good Friday**: Date varies. Markets closed.
- **Independence Day**: July 4.
- **Thanksgiving**: Fourth Thursday of November. Markets also close early on Black Friday.
