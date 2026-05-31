---
name: project-tracker
description: Master project list for Lyndon — what we're working on, what's pending, what's done.
category: productivity
---

# Active Projects

## 1. Assessment List Definitions (ACTIVE)
**Batch build in progress (May 2026):** 5 new lists — Animals (55), Trees (62), Colors (41), Transport (51), Instruments (60). ~295 items total. Data files at ~/Desktop/{name}_data.py. ComfyUI image generation overnight. Pipeline at `assessment-list-guide` skill.

**Completed:**
- Vegetables (48 items, 95MB PDF)
- Countries (68 countries across 6 continents). PDFs at ~/Desktop/Country_Reference/
- Fruit (58 fruits, 1.7MB PDF at ~/ORG BOARD/Div 6/.../fruit_guide.pdf)

**Next:** Dogs list after current batch.

## 2. Scientology Mission of Leichhardt (PENDING)
Two workstreams:
- **Social media:** 2-3 posts/day on hot-button items to build interest and following
- **Weekly newsletter:** Create → send for approval → edit if needed → send → monitor opens → tweak for future. Needs approval channel process.

## 3. Calendar Integration (PENDING — BLOCKED)
Gmail calendar ↔ work calendar sync. MS Graph app fb85268f registered on tenant stewardscapital.com. **Blocked:** waiting for Stewards Capital IT admin to grant admin consent.

## 4. Unchained Recordings Release Pipeline (PENDING)
Full automation for new artist releases:
- Artist sends tracks → mastering → back to artist for approval
- Convert to 16-bit → upload to Cygnus (needs Google auth setup)
- Cover art: template with artist name + EP name (same font), main image tile centered → send for approval → upload to Cygnus
- Enter all release details: release date, artist names, remixer names, English names (not monikers) → alert Lyndon for approval
- Parallel: upload to Bandcamp with same details
- Upload to Label Engine (promo mailout) with artwork, release date, press release (Lyndon will teach press release writing over time based on previous ones)
- Generate social media post images, banners from templates
- Note: Label Engine cost may be replaced later

## 5. CCHR Australia (ACTIVE — Research Phase)
**Daily research sweep** running: Mon-Sun 7am, delivers to Telegram. Monitors psychiatric abuse discourse across web, Reddit, Twitter/X, and 17 trusted sources. Output: top 5 trending items + suggested post angles.

**Skill:** `cchr-research` with keyword strategy, trusted sources, and narrative themes.
**Cron:** job `266a1079b622`,`deliver=telegram:1505823420`.
**Next:** Content calendar + social media posting workflow when research engine has enough source material.

## 6. Unchained Marketing (PENDING)
Monthly/weekly themed social media series to excite audiences.
Recent example: 3D logo gimmicks.
Assets: ~/Music/Unchained/Marketing Branding/Unchained Logo Assets/
- Animated Logo assets (rock break free spin.mp4)
- New Logo assets

## 7. Health Monitoring (PENDING)
Track supplements, medicines, health markers over time.

---

## 8. Multi-Agent Mission Control (NEW — pickup in a few days)
Based on Komputer Mechanic's Hermes Dashboard tutorial:
- 4 persistent Hermes agents + 1 Orchestrator
- Each agent on its own Discord channel, Orchestrator on Telegram
- Glassmorphism web dashboard (Overview, Agents, Task Board, Schedule, Content Library)
- Activity logging, cron calendar, Kanban board
- Tutorial: https://komputermechanic.com/tutorials/hermes-dashboard
- Video: https://www.youtube.com/watch?v=t6W_Zpohb7g

## 9. Voice Outreach Agent (NEW)
Set up an AI-assisted calling workflow to contact people and collect information that is slow/impractical over email.

**Goal:**
- Place structured outbound calls
- Ask approved question scripts
- Capture transcript/recording (where lawful)
- Summarize findings + next actions back to Lyndon

**Phase 1 scope (pilot):**
- One contact type
- 3–5 fixed questions
- Retry/no-answer policy
- Standard summary report format
- Compliance checklist (consent/disclosure by jurisdiction)

**Pending decisions:**
- Telephony stack (Twilio / Vapi / Retell / other)
- Caller identity + disclosure wording
- Escalation rules to human handoff

## User Directive
One project at a time — discipline over complexity. Record projects for future reference but do NOT start new ones without explicit direction.
