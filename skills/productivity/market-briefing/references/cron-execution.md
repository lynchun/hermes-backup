# Cron Execution Notes

Notes for running `market-briefing` as an unattended cron job (no user present).

## Before Starting

Always check if the cron prompt already exists before creating a duplicate:

```bash
cronjob action="list"
```

## The Cron Job

Created 25 May 2026, job ID `80a62658b3c1`.
Schedule: `0 8 * * 1-5` (weekdays at 8am).
Deliver: `origin` (back to the originating chat).

## Skill Loading

The cron prompt should load these skills in order:
```
skills=["market-briefing", "xurl"]
```

- `market-briefing` — playbook, source behavior, pitfalls
- `xurl` — X/Twitter API access for Tom Lee/Dave Hunter

## Prompt Structure

The cron prompt MUST be self-contained — no current-chat context. Include:
1. Full list of what to gather (indices, commodities, headlines, balances, commentary)
2. Where to check for each item
3. That the agent must make reasonable defaults (no user to ask)
4. That SILENT mode is available if there's nothing new to report

## Output Format

Final response is auto-delivered. Structure as:
- Section headers with emoji indicators
- Tables for numeric data
- ⚠ for notable moves (crashes, breakouts)
- ❌ for unavailable data (note WHY unavailable)
- ✅ for successfully checked items

## What This Session Proved

The cron approach works for:
- Yahoo Finance data extraction (browser tool)
- API balance retrieval (terminal + curl)
- Headline aggregation from Yahoo Finance's multi-source feed

The cron approach FAILS for:
- Direct X/Twitter feed access (needs xurl CLI)
- Bloomberg/Reuters article access (bot-detection)
- Search engine results (CAPTCHA)

Fix: ensure `xurl` skill is loaded in the cron prompt, and use it for `@fundstrat`, `@DaveHcontrarian`, `@zerohedge` queries.
