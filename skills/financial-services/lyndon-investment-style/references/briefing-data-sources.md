# Briefing Data Sources — Notes & Pitfalls

## TradingView Watchlist (PRIMARY)
- URL: https://www.tradingview.com/watchlists/24551192/
- Owner: lynchun (Lyndon)
- 28 symbols including all briefing-required tickers
- Load via browser_navigate, extract prices from snapshot
- Much faster than individual Yahoo Finance pages
- Free account — no API key needed

### Tickers relevant to daily briefing
| Data point | TradingView symbol | Notes |
|-----------|-------------------|-------|
| S&P 500 | SPY | ETF, tracks SPX |
| NASDAQ | NDX | NASDAQ 100 |
| VIX | VIX | Volatility index |
| Gold | GOLD | XAU/USD spot |
| Silver | SILVER | XAG/USD spot |
| WTI Crude | USOIL | Use this, NOT Brent |
| Gold Miners | GDX | VanEck Gold Miners ETF |
| Junior Silver | SILJ | Amplify Junior Silver Miners ETF |
| Dollar | DXY | US Dollar Index |
| Treasuries | TLT, TMF | Bond exposure |

## Yahoo Finance Pitfalls
- API endpoints (query1.finance.yahoo.com, query2.finance.yahoo.com) blocked by Cloudflare when using curl
- Browser scraping works but slow — one page per ticker
- Homepage ticker bar only shows BRENT, not WTI — navigating to CL=F required for WTI
- Individual quote pages sometimes show "We are experiencing temporary issues" with delayed data
- Prefer TradingView watchlist over Yahoo

## Bloomberg RSS
- URL: https://feeds.bloomberg.com/markets/news.rss
- Works via curl, returns full articles with titles and links
- No auth required for RSS feed access

## Credit Balance APIs
- OpenRouter: GET https://openrouter.ai/api/v1/auth/key (Bearer token from OPENROUTER_API_KEY)
  - Parse: data.limit_remaining, data.limit (weekly limit)
- DeepSeek: GET https://api.deepseek.com/user/balance (Bearer token from DEEPSEEK_API_KEY)
  - Parse: balance_infos[0].total_balance
- Cron prompt filter: do NOT include literal curl commands with auth headers in cron prompts — just say "use terminal to check balances"
