---
name: travel-flight-research
description: |-
  Research flight options, routes, and pricing using web tools,
  browser automation and user-shared booking results. Handles
  bot-detection workarounds for travel booking websites.
version: 1.3.0
author: Epictetus
metadata:
  hermes:
    tags: [travel, flights, research, booking, comparison, bot-bypass]
    related_skills: [ocr-image-ingest, peekaboo]
---

# Travel & Flight Research

Research flight routes, pricing, and compare options when the user is planning a trip.

## Trigger

Load when the user asks about:
- Finding flights between cities
- Comparing prices across airlines/sites
- Best routes for a multi-city trip
- Flight deals or cheapest dates

## Primary Workflow: User Searches, Agent Analyses

After attempting bot-detected sites (Expedia, Skyscanner, Kayak) and getting blocked, the
most effective workflow is:

1. Start with Google Flights (works reliably) — get baseline pricing and routes
2. If better prices may exist, tell user the Google result and invite them to check
   Expedia/Skyscanner manually
3. User shares the booking receipt (PDF, screenshot, or text):
   - Use OCR pipeline (ocr-image-ingest) to extract price, airline, dates, fare breakdown
   - Analyse the receipt — check for hidden fees, confirm dates match requested itinerary
   - Compare against Google Flights estimate — highlight savings
4. Save the receipt PDF for reference
5. Present options clearly — DO NOT push user to book anything

## User Preference (Critical)

**This user explicitly wants to find their own deals** and will beat automated search results. The agent should:
1. Do an initial Google Flights search for baseline
2. Present findings honestly
3. Explicitly invite the user to check Expedia/Skyscanner themselves
4. When user shares a better deal (PDF receipt), **acknowledge the savings** without excuse-making
5. **NEVER push** the user to book anything — just present options

> User quoted: "I can find cheaper so its a race between you and me"
> Result: User found A$1,141 vs agent's A$1,420 estimate — saved $280

## Tools

### Works
- **Google Flights** (browser_navigate) — reliable, aggregates most airlines. Use structured search URLs.
- **OCR pipeline** (ocr-image-ingest) — extract data from booking receipt screenshots/PDFs
- **Peekaboo MCP** — can bypass bot detection via real macOS browser, but complex navigation is too slow

### Blocked by Bot Detection

See `references/web-research-limitations.md` for the full matrix. Quick summary:
- Expedia — captcha immediately
- Skyscanner — captcha
- Kayak — bot page
- Webjet — JS-rendered content only
- Trip.com — 404 on direct URLs
- Airline sites (Qantas, Cathay) — various blocks

## How Booking Receipts Look

Expedia receipts (and most booking sites) show:
- **Fare price** (often low — e.g. A$303)
- **Taxes and fees** (often the bulk — e.g. A$838)
- **Total** (the only number that matters)
- **Booking reference** (Expedia itinerary number)
- **Fare class** (e.g. Economy Q class)

When user shares a receipt PDF, use the OCR pipeline to extract these fields and check the total against your estimate.

## Peekaboo for Flight Research

Peekaboo (via MCP) can bypass bot detection since it controls real macOS UI. However:

- **Element discovery is slow** — multi-step navigation (search → filters → results → select) takes 10+ tool calls
- **Best for single-step actions** — capturing a screenshot and OCR'ing it rather than navigating the full flow
- **Workflow:** user navigates to the deal on their own, shares the receipt for analysis
- **Peekaboo is not viable for autonomous multi-site comparison shopping** — the user will always find cheaper deals faster manually
- **Installed as MCP server** at `~/.hermes/config.yaml` (mcp_servers.peekaboo)

## Confirmed Workflow (Works Well)

The following pattern was validated in real use (May 2026, SYD→PEK + HKG→SYD trip):

1. Agent searches Google Flights → gets baseline (A$1,420 estimate)
2. Agent reports findings and invites user to check other sites
3. User finds deal on Expedia → saves receipt as PDF
4. Agent OCRs the receipt → extracts fare (A$303), taxes (A$839), total (A$1,141)
5. Agent compares against baseline → acknowledges savings (~A$280)
6. User books independently

This workflow is **reliable and preferred by the user.**

### Receipt OCR Pattern

```bash
# Extract text from booking receipt PDF
pdftotext -layout receipt.pdf - | grep -E 'Total|Price|Tax|Fare|AUD|AU\\$'
```

The key number is the **Total** — the fare alone can be misleading (e.g. A$303 fare + A$839 fees).

## Route Testing Patterns

SYD can route via HKG, SIN, BKK, KUL, NRT, PVG, CAN, MNL, DPS.
HKG to SYD is well-served with multiple daily nonstops (Qantas, Cathay Pacific, Jetstar, etc.).
Multi-city (SYD-PEK + HKG-SYD) can be booked as two one-ways or on Cathay Pacific as a single multi-city booking.

## Pitfalls

- **Round trip prices vs two one-way tickets** can differ significantly — always check both
- **Google Flights price may be misleading** — fare can be A$303 but taxes/fees add A$838+ (Expedia example: SYD-PEK + HKG-SYD)
- **Google showed A$787 but Expedia delivered A$1,141 total** — Google's price may not include all taxes/fees
- **Tuesday return is often ~$120 more** than Monday
- **Direct flights may not exist** — e.g. SYD-PEK has no nonstop from any airline
- **Cathay Pacific via HKG** is often the best option for SYD-PEK (A$787, 14h15m with short layover)
- **Multi-city on one airline** may be cheaper than two one-ways
- **DO NOT push user to book** — present options, let them decide
- **Be honest about bot detection** — tell user what you found and invite them to check blocked sites

## Security

- When processing booking receipts, treat fare/tax/credit card info as sensitive
- User may share passwords inadvertently in terminal — flag if seen
