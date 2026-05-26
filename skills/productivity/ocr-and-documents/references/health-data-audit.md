# Health Data Audit: Cross-Referencing Workflow

Used 2026-05-12 to validate Lyndon's Obsidian health markers against source medical PDFs/RTFs/DOCXs, then corrected all discrepancies.

## Directory Layout

```
ORG BOARD/Div 5 (Personal Dev., Health, Correction) /HEALTH/1. Personal data/
├── health_markers_master.csv          # Master compiled CSV (~500 lines)
├── health_markers_timeline.csv        # Timeline CSV (messy, has OCR garbage)
├── health_markers_timeline_clean.csv  # Cleaned subset of timeline
├── health_pdf_markers.csv             # PDF-extracted markers
├── health_markers_rtf_tables.csv      # RTF-table extracted
├── Medical Reports and Correspondance/   # PDFs by year
├── Health Professionals and Specialists/ # DOCX summaries
└── Test Results/
    ├── Bloods/2011-2012/ 2021/ 2023/ 2024/ 2025/
    ├── Genetic testing/   (23andMe, Promethease, Genvue, Genetic Genie)
    ├── Scans/             (MRIs, X-rays, CT, DEXA)
    ├── Gut/               (GI map)
    ├── Heavy Metals/      (hair, urine)
    └── Immune testing/
```

Obsidian vault markers: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Health/Markers/` (84 marker notes)

## Source Extraction Commands

```bash
# RTF → text (use textutil, NOT cat — RTF is binary-like)
textutil -stdout -cat txt report.rtf

# PDF → text (text-based PDFs)
pdftotext -raw report.pdf -
pdftotext -layout report.pdf -    # Preserve column alignment

# PDF → OCR (scanned/image PDFs)
tesseract report.pdf stdout --psm 6

# DOCX → text
textutil -stdout -cat txt summary.docx
```

## Values Verified from Source

| Marker | Date | Value | Source File |
|--------|------|-------|-------------|
| Vitamin B6 | 2021-06-25 | 7,910 nmol/L | Compound RTF (Lab ID 850316031) |
| Vitamin B6 | 2021-07-14 | 310 nmol/L | B6-FollowUp RTF |
| Vitamin B6 | 2023-10-06 | 105 nmol/L | Vitamin B6 October 2023.pdf |
| Vitamin B6 | 2024-01-18 | 73 nmol/L | 1. Bloods Jan 18 2024.pdf |
| Vitamin B6 | 2024-02-01 | 196 nmol/L | 2. Bloods Jan and Feb 2024 #2.pdf |
| Vitamin B6 | 2024-08-09 | 147 nmol/L | Sept 2024 Bloods PDF |
| Thiamine (B1) | 2021-06-25 | 290 nmol/L | Compound RTF |
| Mercury (blood) | 2021-06-26 | 69 nmol/L | Blood metals RTF |
| ANA | 2021-06-25 | Detected, 80 Speckled | Mercury RTF |
| Active B12 | 2023-10-06 | 113 pmol/L | 2025 Bloods PDF |
| Active B12 | 2024-01-18 | 143 pmol/L | 2025 Bloods PDF |
| Homocysteine | 2022-08-16 | 7.8 umol/L | Sept 2024 PDF (historical table) |
| Homocysteine | 2024-04-18 | 4.0 umol/L | Sept 2024 PDF (historical table) |
| Homocysteine | 2024-08-09 | 13.4 umol/L | Sept 2024 PDF |
| Homocysteine | 2025-03-03 | 11.0 umol/L | Mar 2025 PDF |
| Bilirubin | 2010-06-25 | 59 umol/L | Biochemistry table (RTF) |
| Bilirubin | 2011-08-04 | 32 umol/L | Biochemistry table |
| Bilirubin | 2021-06-07 | 44 umol/L | Biochemistry table |
| Bilirubin | 2021-06-25 | 31 umol/L | Biochemistry table |
| Copper | 2021-06-24 | 12 umol/L | Metals report |
| Zinc | 2021-06-24 | 10 umol/L | Metals report |
| ACE | 2021-06-24 | 30 U/L | Compound RTF |
| Complement C3 | 2021-06-25 | 0.76 g/L | Compound RTF |
| CRP (2009) | 2009-11-05 | 30.4 mg/L | Compound RTF (not g/L!) |
| CRP (2021) | 2021-06-25 | 0.4 mg/L | Compound RTF |
| Testosterone | 2011-06-28 | 27.44 nmol/L | PDF-OCR |
| Testosterone | 2024-06-07 | 15.4 nmol/L | PDF-OCR (Obsidian had mmol/L — WRONG) |

## Corrections Applied

### Obsidian Markers Fixed (8 files)

| File | Issue | Fix |
|------|-------|-----|
| CRP.md | Unit said g/L, source says mg/L | Changed g/L → mg/L |
| Testosterone.md | 2024-06-07 entry said mmol/L | Changed to nmol/L |
| Homocysteine.md | Missing 7.8 (Aug 2022), 4.0 (Apr 2024) | Added from source historical table |
| ANA.md | Did not exist | Created from source (Detected, 80 Speckled) |
| Active B12.md | Did not exist | Created with 113 (Oct 2023), 143 (Jan 2024) |
| Iron.md | Contained TIBC value mixed with serum iron | Removed TIBC; added to TIBC.md |
| TIBC.md | Had only 2024 reading | Added 2011 TIBC value (53) |
| Vitamin B6.md | Missing 73 (Jan 2024 draw), bad source ref | Added missing row, fixed sources |

### CSVs Updated (4 files, ~20 rows changed/added)

**health_markers_master.csv:** Added 5 missing B6 rows + 2 missing Homocysteine rows
**health_markers_timeline.csv:** Fixed 73→105, 35→73, removed OCR-noise 6, added 196+147
**health_markers_timeline_clean.csv:** Same fixes
**health_pdf_markers.csv:** Added 105, 73, 196 B6 rows

### File Renamed
- `2. Bloods Jan 18 2024 #2.pdf` → `2. Bloods Jan and Feb 2024 #2.pdf`

## Pitfalls & Lessons

1. **Compound RTF files contain multi-date tables** — always check ALL date columns, not just the newest
2. **"Tests Pending" ≠ "Tests Completed"** — don't confuse ordered-but-unreported with actual results
3. **Multiple B6 draws in same month** is normal — Jan 2024 had two: 73 and 196, from different lab reports
4. **Lab PDFs go image-based after ~2024** — pre-2024 had embedded text, 2024+ were scans (blank pdftotext)
5. **timeline CSVs accumulate OCR garbage** — lines like "shapeType,1,fFlipH" or "029819,6666,Fax" need manual removal after extraction
6. **Lab table dates default to patient DOB** (1973-04-12) when column parsing fails — don't trust default dates
7. **User domain knowledge beats automated extraction** — Lyndon correctly identified that the CSV had wrong B6 values for Oct 2023 and Jan 2024 because the extraction misread historical data columns
8. **g/L vs mg/L confusion** is a common unit error in lab data — CRP at 30.4 g/L is impossible, always mg/L. Testosterone at 15.4 mmol/L is impossible, always nmol/L.
