# Web / Travel Research Limitations (May 2026)

Most major travel booking sites block headless browsers used by AI agents.
Verified blocked sites (12 May 2026):

| Site | Blocks? | Notes |
|------|---------|-------|
| **Google Flights** | No | Works — aggregated results across airlines |
| **Momondo** | No | Homepage accessible; search forms complex to navigate programmatically |
| **Expedia** | Yes | Captcha / "Bot or Not?" page |
| **Skyscanner** | Yes | Captcha |
| **Kayak** | Yes | Bot detection page |
| **Webjet** | Yes | JS-rendered content blocks curl |

## Workarounds

1. **Peekaboo MCP** (if installed) — controls the user's actual Mac desktop
   browser, bypassing headless detection entirely. Requires Screen Recording
   + Accessibility permissions. Connected via `hermes mcp add peekaboo`.
2. **User shares results** — user searches on their own browser and shares
   screenshots/PDFs/receipts; agent analyses rather than searches.
3. **Direct airline sites** — some airline sites (Cathay Pacific, Qantas) are
   less aggressive than aggregators. Try those first when possible.

## Google Flights Known Limitations

- Shows excellent aggregated price data but may miss bulk deals
- The user found a deal $280 cheaper on Expedia (A$1,141 vs A$1,421 estimate)
- Google's prices include their aggregated taxes/fees; actual booking site
  totals can differ significantly
- Always present as estimates, not guarantees
