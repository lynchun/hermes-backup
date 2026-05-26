---
name: health-markers-report
description: |-
  Generate a comprehensive, professional HTML health markers report from
  Obsidian vault data and source pathology files. Color-coded tables
  organised by category (vitamins, inflammation, liver, lipids, minerals,
  kidney, endocrine, FBC, electrolytes, B6 toxicity timeline, gut/stool,
  genetics, allergies, DEXA).
version: 2.4.0
author: Epictetus
metadata:
  hermes:
    tags: [health, markers, report, HTML, visualization, obsidian]
    related_skills: [ocr-and-documents, dashboard-pdf-workflow]
---

# Health Markers Report Skill

Generate a professional, colour-coded HTML report of a patient's health
markers history, designed for specialist consultations.

## Trigger

Load this skill whenever the user asks to:
- Generate a health report for a doctor/specialist
- Create a comprehensive markers timeline
- Compile all out-of-range values
- Update an existing health markers report
- Summarise pathology history for a consultation

## Data Sources

The report pulls from:
1. Obsidian vault markers at Health/Markers/*.md
2. Compiled CSVs at 2. Health marker tables/*.csv
3. Source pathology documents (PDFs, RTFs, DOCXs)
4. Pathology correspondence folder
5. US Lab results (unit conversion needed)

## Report Sections (in order)

1. Clinical Summary -- Bulleted key facts, 8-10 items max. No NEW tags.
2. Vitamin Markers -- Full timeline with colour coding
3. B6 Toxicity Timeline
4. Glucose & Metabolic -- GTT with insulin
5. Inflammatory/Immune
6. Liver Function
7. Lipids
8. Iron Studies
9. Minerals & Metals
10. Kidney Function
11. Endocrine
12. Full Blood Count
13. Electrolytes & Chemistry
14. New Markers (Single-Observation)
15-19. Speciality sections (Gut, Food Sensitivity, Genetics, etc.)
20. Investigation Flags -- Latest panel flags only
21. Pathology Summary -- All conditions active/resolved
22. Complete Out-of-Range Summary

## CGM Sensor Data Sections (23+)

When continuous sensor data is available (ketone CGM, glucose CGM, or similar),
add as section 23+ after the out-of-range summary (section 22). One section per
sensor type, with side-by-side session comparison.

### Data Source Format

Sensors export Excel files (.xlsx) with:
- Columns: No. | Time | Sensor reading(mmol/L)
- Single sheet named after the sensor serial
- 5-minute interval readings
- ~288 readings/day x 14-15 days per sensor (~4000 rows per session)

### File Location (Ketone CGM)

Sensor exports live at:
`~/ORG BOARD/Div 5 (Personal Dev., Health, Correction) /HEALTH/1. Personal data/1. Test Results/Ketones/`

### Analysis Script Pattern

Use a dedicated .py script run via terminal (not execute_code sandbox, which lacks openpyxl).
Pattern:

1. Write extraction script to /tmp/ with openpyxl + json output
2. Run via `python3 /tmp/script.py`
3. Parse JSON output to build HTML section

### Analysis Checklist

1. Read both .xlsx files with openpyxl (data_only=True to get computed values)
2. Compute: total readings, date range, min/max/avg/median
3. Distribution buckets (<0.5, 0.5-1.0, 1.0-1.5, 1.5+ mmol/L)
4. Daily averages — sensor start shows elevated readings (Day 1 spike), then gentle drift down
5. Side-by-side daily average comparison when two sensor sessions exist
6. First 24h vs last 24h mean (artifact pattern detection)
7. Hourly pattern by period: Overnight (00:00-05:59), Morning (06:00-11:59), Afternoon (12:00-17:59), Evening (18:00-23:59)

### HTML Section Structure (inserted between section 22 </div> and the closing key-facts)

Use the `<div class="section">` pattern matching the existing dashboard style.

```
<!-- ==================== 23. CGM TYPE ==================== -->
<div class="section">
<h2>23. Continuous [Type] Monitoring <span class="badge">Sensor brand</span></h2>
<p><!-- intro sentence --></p>

<!-- Sensor summary cards (two-col) -->
<div class="two-col">
  <div class="result-box" style="border-left:4px solid #4a7dff;">
    <h3>Sensor [ID] <span style="font-size:12px;font-weight:400;color:#888;">&mdash; [Year]</span></h3>
    <div class="grid">
      <div>Duration: <strong>N days</strong> (date range)</div>
      <div>Readings: <strong>N</strong></div>
      <div>Mean: <strong>X.XX mmol/L</strong></div>
      <div>Median: <strong>X.XX mmol/L</strong></div>
      <div>Range: <strong>X.X &ndash; X.X</strong></div>
      <div>First 24h avg: <strong>X.XX</strong> &rarr; Last 24h avg: <strong>X.XX</strong></div>
    </div>
  </div>
  <!-- repeat for second sensor -->
</div>

<!-- Daily average comparison table -->
<div class="result-box">
<h3>Daily Average Comparison &mdash; Sensor Lifecycle</h3>
<div class="sticky-wrap">
<table>
<thead><tr><th>Sensor Day</th><th colspan="2">[Year A]</th><th colspan="2">[Year B]</th></tr>
<tr><th>Day</th><th>Date</th><th>Mean (mmol/L)</th><th>Date</th><th>Mean (mmol/L)</th></tr></thead>
<tbody>
<tr><td>1</td><td>date</td><td>value</td><td>date</td><td>value</td></tr>
<!-- ... day 2 through N ... -->
</tbody>
</table>
</div>
</div>

<!-- Time-in-Range Distribution -->
<div class="result-box">
<h3>Time-in-Range Distribution</h3>
<table>
<thead><tr><th>Range</th><th>Interpretation</th><th colspan="2">[Year A]</th><th colspan="2">[Year B]</th></tr></thead>
<tbody>
<tr><td>&lt; 0.5 mmol/L</td><td>Minimal ketosis</td><td>N</td><td>(XX.X%)</td><td>N</td><td>(XX.X%)</td></tr>
<!-- more ranges -->
</tbody>
</table>
</div>

<!-- Hourly Pattern -->
<div class="result-box">
<h3>Hourly Pattern (24h)</h3>
<table>
<thead><tr><th>Period</th><th>Hours</th><th>[Year A] Avg</th><th>[Year B] Avg</th><th>Pattern</th></tr></thead>
<tbody>
<tr><td>Overnight</td><td>00:00&ndash;05:59</td><td>X.XX</td><td>X.XX</td><td>description</td></tr>
<tr><td>Morning</td><td>06:00&ndash;11:59</td><td>X.XX</td><td>X.XX</td><td>description</td></tr>
<tr><td>Afternoon</td><td>12:00&ndash;17:59</td><td>X.XX</td><td>X.XX</td><td>description</td></tr>
<tr><td>Evening</td><td>18:00&ndash;23:59</td><td>X.XX</td><td>X.XX</td><td>description</td></tr>
</tbody>
</table>
</div>

<!-- Clinical Interpretation -->
<div class="callout">
<strong>Clinical Interpretation for [Doctor]:</strong><br>
&#8226; <strong>Both sensors show near-identical overall means</strong> &mdash; consistent with a well-adapted dietary pattern.<br>
&#8226; <strong>Sensor insertion spike:</strong> Day 1 elevation from tissue trauma, not true metabolic change. Note pattern across sessions.<br>
&#8226; <strong>Baseline drift:</strong> Daily averages decline over sensor lifetime (first week ~0.5-0.6 to final days ~0.2-0.3). Unclear if metabolic or sensor ageing.<br>
&#8226; <strong>&gt;95% below 1.0 mmol/L</strong> — consistent with expected range for adapted keto/carnivore.<br>
&#8226; <strong>Circadian pattern:</strong> Higher overnight/evening, lowest mid-day — matches fasting physiology.<br>
&#8226; <strong>&#9888; Caveat:</strong> Interstitial measurement; accuracy may decline in final days.
</div>
</div>
```

### Insertion Point

Insert between the closing `</div>` of section 22 (complete-out-of-range) and the 
opening `<div class="key-facts" style="margin-top:24px;">` at the bottom of the page.
Use patch() to insert — the old_string is the `key-facts` div open tag 
`<div class="key-facts" style="margin-top:24px;">` and the new_string is the full 
ketone HTML section + the same key-facts tag.

**Important:** After insertion, verify div balance between the section comment and 
the key-facts tag using a Python script. The count of `<div` and `</div>` in that 
range should be equal. Pre-existing mismatch (~ -1) in the original dashboard file 
is from a stray `</table>` in the FBC section — not caused by the new section.

### File Replace/Upload (Google Drive)

After editing the HTML in the ORG BOARD location:

1. **Update the existing PDF** using drive.files().update() with the existing file ID (preserves the share link)
2. Do NOT delete + recreate — existing bookmarks and shares break
3. Use Playwright's page.pdf() with format='A4', print_background=True, 
   margin={'top':'10mm','bottom':'10mm','left':'10mm','right':'10mm'}
4. Upload: `drive.files().update(fileId=PDF_FILE_ID, media_body=MediaFileUpload(...))`

File IDs are stable:
- Dashboard PDF: `1IujjKRyVZqPZorn3KphVlmxX4SPPaP42`
- Dashboard HTML: `10CE-Xd6GMZ9ezJdvjw2o9PaAdIJaKEVu`

### Clinical Interpretation Template (ketone-specific)

Key talking points for a keto-knowledgeable doctor:

- **Overall pattern:** Well-adapted carnivore shows mostly <0.5 mmol/L with excursions to 0.5-1.5. Don't expect high ketones — that's for unadapted.
- **Sensor start-up artifact:** Document both sessions' insertion spikes separately since they can differ (gradual ramp vs acute spike). Flag as not real ketosis.
- **Session-over-session reproducibility:** Same mean/median across years = stable metabolic baseline.
- **Circadian rhythm:** Higher overnight = fasting effect. Lowest mid-day = fed state. Matches expected physiology.
- **Low time in therapeutic ketosis (>1.0 mmol/L):** Only 2-4% of readings. This is expected for maintenance carnivore, not therapeutic keto. Worth noting for clinical context.

## Style & Design Rules (STRICT)

- No change-marking tags (NEW, UPDATED, HIST) -- rejected by user.
- Investigation Flags: strictly NEW findings only. No MTHFR/hEDS/Gilbert's.
- B6 status: "Resolved in Oct 2023, with one relapse despite no supplementation."
- Hypophosphatasia note: "ALP never low (52-68, ref 30-110) -- argues against hypophosphatasia." NOT "Likely exogenous B6."
- Tables with 4+ columns: sticky-wrap (scrollable), NOT two-col.
- Section 21 (Flags): full-width, not two-column.
- Patient header: "Clinical Summary" NOT "Clinical Summary for Dr [Name]".
- Diet field: "Carnivore-ish (with excursions)".
- Missing ref ranges: use standard published ranges for adult males.
- Pathology Summary: near end of report, not at the top.
- Colour coding: red=high, orange=low, green=normal.

## Collaborative Editing Discipline (CRITICAL)

When the user edits a document and removes specific content, that content
is DELETED from the working context entirely. Do NOT reintroduce it
anywhere. The user's removal is an editorial signal -- respect it.
"Based on the history" means based on the FINAL EDITED VERSION.

## Clinical History Narrative Workflow

1. Read ALL documents in the correspondence folder
2. Prioritise: Extended summaries over flash summaries
3. Structure chronologically
4. Write in plain language -- NEVER third person ("the patient" / "he").
   Use direct statements. This was explicitly enforced.
5. Let the user edit freely. Removals stay removed.
6. Save as TXT to the personal data folder
7. Incorporate salient points into HTML dashboard after user finalises

## Historical Data Extraction

New pathology reports often contain comparison tables. Always extract
these. Scan EVERY new report for "Latest Results" tables. Check ALL
individual test files, not just composites.

## Unit Conversions

- Vitamin B6 (P5P): 1 ng/mL = 4.046 nmol/L
- Show both converted value (with *) and original in footnote

## Reference Ranges Vary by Lab

Different labs use different ranges. Document these per source.

EXAMPLE: B6 reference ranges vary across labs. Laverty/DHM and Sullivan
Nicolaides use 20-190 nmol/L. Australian Clinical Labs uses 35-110 nmol/L.
A value of 147 is normal on one range but flagged high on the other. Always
note the LAB, not just the value.

Cross-check new pathology reports that include comparison tables
("Latest Results" / "Previous Result" columns). These often contain
historical values you haven't seen before -- extract them even if the
current result is the primary purpose of reading the file.

## Date Splitting

- Early YYYY (Jan-Mar), Mid YYYY (Apr-Jun), Late YYYY (Aug-Dec)

## PDF Generation & Drive Upload

After the HTML dashboard is finalised, generate a print-ready PDF and upload to Google Drive for external sharing.

### File Locations

- **Dashboard HTML (working copy):** `~/Downloads/health_markers_for_dr_mason.html`
- **Dashboard HTML (authoritative copy):** `~/ORG BOARD/Div 5 (Personal Dev., Health, Correction) /HEALTH/1. Personal data/For Dr Paul Mason/health_markers_for_dr_mason.html`
- **Clinical History HTML:** `~/ORG BOARD/.../For Dr Paul Mason/clinical_history_lyndon_arthurson_12may2026 RA.html`
- **GDrive Folder ID:** `1xqKTR7vrWfMIv1_iUyOeqMhDLPjMpRf3` (Current Health Dashboard)

### Add Print-Quality CSS to Both HTML Files

```css
@page { margin: 20mm 15mm; size: A4; }
@media print {
  body { background: white; padding: 0; margin: 0; }
  .section { page-break-inside: avoid; break-inside: avoid; }
  table { page-break-inside: auto; }
  tr { page-break-inside: avoid; }
  h2 { page-break-after: avoid; }
  h1 { page-break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
  .patient-card, .key-facts, .result-box,
  .callout, .callout-warn, .callout-red,
  .pathology-item, .highlight, .diag-item,
  .diag-list { page-break-inside: avoid; break-inside: avoid; }
  .subtitle { page-break-after: avoid; }
}
```

### Workflow Order (Strict)

1. **Edit the Downloads copy** of the dashboard HTML (the working copy)
2. **Edit the clinical history** in its ORG BOARD location (edit in place)
3. **Immediately sync** the dashboard HTML from Downloads → ORG BOARD:
   ```bash
   cp ~/Downloads/health_markers_for_dr_mason.html "~/ORG BOARD/Div 5 (Personal Dev., Health, Correction) /HEALTH/1. Personal data/For Dr Paul Mason/health_markers_for_dr_mason.html"
   ```
4. **Generate PDFs** using Playwright from the ORG BOARD copies
5. **Upload** to Drive (delete old PDFs first, upload new, re-apply public sharing)
6. **Tell user to Cmd+Shift+R** (hard refresh) before confirming changes took effect

### PDF Generation (Playwright)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file://' + html_path)
    page.pdf(
        path=pdf_path, format='A4',
        margin={'top': '20mm', 'bottom': '20mm', 'left': '15mm', 'right': '15mm'}
    )
    browser.close()
```

### Upload to Drive

Use `drive.files().update()` to preserve the existing file ID (keeps bookmarks/share links working):

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = Credentials.from_authorized_user_file(
    '/Users/lyndonarthurson/.hermes/google_token.json')
drive = build('drive', 'v3', credentials=creds)

# Get the existing file ID first (list the folder)
folder_id = '1xqKTR7vrWfMIv1_iUyOeqMhDLPjMpRf3'
items = drive.files().list(
    q=f"'{folder_id}' in parents",
    fields='files(id, name, mimeType)'
).execute()

# Find the PDF by name and get its ID
pdf_id = [f['id'] for f in items['files'] if f['name'] == 'Health Markers Dashboard - Dr Mason.pdf'][0]

# Update the file in-place (preserves link)
media = MediaFileUpload(pdf_path, mimetype='application/pdf')
updated = drive.files().update(
    fileId=pdf_id,
    media_body=media,
    fields='id, name, webViewLink, modifiedTime'
).execute()
```

Known stable file IDs (may change if DT deletes/recreates):
- Dashboard PDF: `1IujjKRyVZqPZorn3KphVlmxX4SPPaP42`

### Viewer Link (no login needed)

Format: `https://docs.google.com/viewer?url=https://drive.usercontent.google.com/download?id=FILE_ID&embedded=true`

### PDF Workflow Pitfalls

- **Two copies exist** — edits to Downloads are NOT reflected in ORG BOARD until `cp` is run. Always sync before user checks.
- **Hard refresh (Cmd+Shift+R)** is always the first diagnostic when user says "hasn't changed"
- **Different CSS** — dashboard uses `.patient-card`, `.callout-red`, `.result-box`; clinical history uses `.section`, `.highlight`, `.diag-item`. Both need print styles applied.
- Playwright's `page.pdf()` does NOT support `print_backgrounds` on older versions.
- **Google Drive requires sign-in for HTML files** even with public sharing — always convert to PDF for external recipients.

## Local Model for Client Work

For client data that cannot leave the machine:
- Use direct Ollama: `ollama run llama3.1:8b`
- Hermes local profile exists but Llama 3.1 8B is slow in Hermes (~60s+)
- Qwen 2.5 3B/7B (32K context) won't meet Hermes 64K minimum
- Peekaboo MCP screen data + cloud model = offshore too (same restriction)

## Web Research Limitations

See `travel-flight-research/references/web-research-limitations.md` (hosted under the travel research skill). Travel sites block headless
browsers. Google Flights and Momondo work. Peekaboo can bypass via real
browser. Otherwise user searches and shares results.

## Doctor Consult Protocol Summaries

When the user has a doctor consult (especially Dr Paul Mason) and asks you to create a practical patient-facing summary:

### Trigger

This workflow runs when the user asks for:
- A supplement/medication regime from doctor notes
- A fridge-ready protocol summary
- A table of what to take and when
- A plain-language synopsis of a doctor's findings

### Source Documents

Doctor notes are typically stored in the Obsidian vault under:
`Health/Health professionals/[Doctor Name]/Consult [Date]/`

Files may include:
- `Patientnotes.pdf` — the doctor's clinical notes
- `Paul Mason Summary and Qs.md` — the user's own notes and questions
- `Follow up script before next meeting.pdf` — pathology forms
- Other handouts (probiotic guides, etc.)

### Extraction

For PDFs from Dr Mason's clinic (TCPDF-generated):
1. Use `pymupdf` to extract text (already installed)
2. The PDFs have a header on every page (clinic address, patient info) — ignore duplicates
3. Extract: supplement names, doses, frequencies, special instructions, cautions
4. Also extract: medication names, sinus rinse recipes, eye care protocols, body wash protocols

### Output Format

The summary should be structured as a single-read markdown document optimised for A4 printing:

**Title:** `[Patient]'s Daily Protocol — Dr [Name] ([Date])`

Then sections in this order:

1. **Supplements — Daily** (table: #, Supplement, Dose, When, Notes)
2. **Medicines — Weekly / As Directed** (table: same columns)
3. **Sinus Rinse** (if applicable — step-by-step with quantities and technique)
4. **Body Wash** (product name + usage instructions)
5. **Eye Care** (products + frequency)
6. **Cautions** (drug interactions, practical warnings in a bulleted block)
7. **Blood Tests — Follow-up** (list of ordered tests)
8. **Quick Reference — Morning & Evening** (checkbox list for fridge printing)

### Table Format Rules

- Clear header rows with `|` pipes
- Include a `---` separator row
- Use bold for emphasis on critical items
- Add `⚠️` for drug interactions or safety notes
- Notes column for brand names, where to buy, practical tips

### Style Rules

- Plain language — the user has to follow this from memory
- Group supplements by timing (morning, evening, with food)
- Include quantities explicitly: "6-12ml of 10% betadine in 240ml bottle" not "dilute appropriately"
- Cautions section is mandatory — don't skip it
- The quick reference checklist at the bottom is the most-used part — invest effort here

### File Location

Save in the same Obsidian consult folder as the source PDFs, named:  
`Supplement & Medicine Regime.md`

### Update Pattern

When the user says "first draft and we'll tweak" — write the complete draft, present it, wait for feedback. Don't ask for approval on every subsection.

## Pitfalls

- Vision API wont work with DeepSeek V4 Flash
- Tesseract 5.5.2 path bug -- cd /tmp first
- 2024 has high variability -- always split into periods
- NEVER re-add content the user deliberately removed during editing
- Write clinical history in plain language; third-person was rejected
- Most travel booking sites block headless browser
- Doctor PDFs from TCPDF have repeated header on every page — dedupe mentally
- When building protocol tables, the user needs to PRINT this — format for physical paper, not screen-first
