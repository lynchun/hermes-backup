---
name: project-tracker
description: Master project list for Lyndon — what we're working on, what's pending, what's done.
category: productivity
---

# Active Projects

## 1. Assessment List Definitions (ACTIVE)
Helping Scientology students understand assessment list items used for auditor training. Each item gets a multilanguage reference sheet (EN/繁體中文/日本語) with definitions.

**Deliverables:** Typst-generated PDFs with GeoPandas continent maps, numbered circles, 3-language definitions.

**Completed:**
- Vegetables (48 items, 95MB PDF)
- Countries (68 countries across 6 continents — Africa, Europe, Asia, North America, South America, Oceania). PDFs at ~/Desktop/Country_Reference/
- **Fruit** (58 fruits, 1.7MB PDF at ~/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship/fruit_guide.pdf)
- Pipeline saved as `assessment-list-guide` skill with template at templates/build_guide.py

**Next:** Dogs list. docx already in Assessment listing defintions folder.

**Location:** ~/Desktop/Country_Reference/ (countries), ~/ORG BOARD/Div 6/ (vegetables, fruits, dogs)
**Pipeline for non-map lists:** Docx extract → translate → PIL illustrations → HTML → Chrome PDF (see `assessment-list-guide` skill)
**Pipeline for country maps:** Docx extract → translate → GeoPandas 50m maps → Typst → PDF

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

## 5. CCHR Australia (PENDING)
Social media posting and management.

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

## User Directive
One project at a time — discipline over complexity. Record projects for future reference but do NOT start new ones without explicit direction.
