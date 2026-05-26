# Health Data Audit — Verified Values & Corrections

## Directory Layout

```
HEALTH/1. Personal data/
├── 1. Test Results/            # Source PDFs, RTFs, DOCXs
│   ├── Bloods/                 # Blood test results by year
│   ├── Allergy testing/        # IgE panels (image PDFs — unreadable)
│   ├── Genetic testing/        # 23andMe, Genetic Genie, Genvue
│   ├── Gut/                    # GI Map (NutriPATH, Feb 2024)
│   ├── Heavy Metals/           # Hair mineral analysis, challenge tests
│   ├── Immune testing/         # IgG food panel (US BioTek, Nov 2025)
│   ├── Organic Acids Urine/    # OAT March 2024
│   └── Scans/                  # MRI, CT, DEXA reports
├── 2. Health marker tables/    # Compiled CSVs (master, timeline, etc.)
├── 3. Valuable medical correspondence/
│   └── 2. TO specialst or doctor from me/  # Patient-written summaries
└── Medical Reports and Correspondance/
```

## Source Extraction Commands

| File Type | Command |
|-----------|---------|
| Text PDF | `pdftotext -layout file.pdf -` |
| Scanned PDF | `sips -s format jpeg --resampleWidth 2000 file.pdf --out /tmp/x.jpg && cd /tmp && tesseract x.jpg stdout --psm 6 --oem 1` |
| RTF | `textutil -stdout -cat txt file.rtf` |
| DOCX | `textutil -stdout -cat txt file.docx` |

**Tesseract path bug:** Tesseract 5.5.2 cannot read files with absolute paths. Always `cd /tmp` and use relative filenames.

## Verified Values from Source

### Vitamin B6 (P5P) — All values confirmed from source documents
| Date | Value (nmol/L) | Source File | Verified? |
|------|---------------|-------------|-----------|
| 2021-06-25 | 7,910 | Compound RTF (B1 high) — line "Vitamin B6 (P5P) H 7910 nmol/L (20-190)" | ✓ |
| 2021-07-14 | 310 | Follow up B6 levels 14.7.21 RTF — "Vitamin B6 (P5P) H 310 nmol/L (20-190)" | ✓ |
| 2023-06-01 | 42.5* | Quest Diagnostics USA — original 10.5 ng/mL (ref 2.1-21.7) | ✓ |
| 2023-10-06 | 105 | Vitamin B6 October 2023.pdf | ✓ |
| 2024-01-18 | 73 | 1. Bloods Jan 18 2024.pdf | ✓ |
| 2024-01/02 | 196 | 2. Bloods Jan and Feb 2024 #2.pdf | ✓ |
| 2024-08-09 | 147 | 7. Blood 5 September 24 (Random) B6 and Homcystein.pdf | ✓ |

### Bilirubin (Gilbert's pattern)
| Date | Value | Ref Range | Verified? |
|------|-------|-----------|-----------|
| 2010-06-25 | 59 H | 4-20 | ✓ From biochemistry RTF table |
| 2011-08-04 | 32 H | 4-20 | ✓ |
| 2021-06-07 | 44 H | 4-20 | ✓ |
| 2021-06-25 | 31 H | 4-20 | ✓ |
| 2024-03-16 | 11 | 3-20 | ✓ First normal reading ever |
| 2024-12-04 | 28 H | 4-20 | ✓ RPAH (Urriola) |

### Iron Studies — Anomalous March 2024 reading
| Marker | Mar 2024 | Apr 2024 | Context |
|--------|----------|----------|---------|
| Ferritin | 18 (LOW) | 186 | Dramatic recovery in 1 month |
| Iron | 9.0 (LOW) | 14.7 | Recovered |
| Saturation | 13% (LOW) | 29% | Recovered |
Conclusion: transient deficiency, possibly acute/collection-related.

### Complement C3 Trend
| Date | Value | Ref |
|------|-------|-----|
| 2021-06-25 | 0.76 L | 0.78-1.82 |
| 2024-04-18 | 0.61 L | |
| 2024-12-04 | 0.68 L | |
Persistently low-borderline over 3 years. C4 borderline (0.12-0.14).

### ANA
- Patient records: detected 80-160 speckled (historical)
- Dec 2024 RPAH serology: **negative** — possible intermittent pattern

## Corrections Applied

1. **CRP unit** — Obsidian said g/L, source said mg/L. Fixed.
2. **Testosterone unit** — 2024-06-07 said mmol/L, should be nmol/L. Fixed.
3. **Homocysteine** — Added missing values 7.8 (Aug 2022) and 4.0 (Apr 2024) from source PDF.
4. **Active B12** — Created missing marker file with 113 (Oct 2023) and 143 (Jan 2024).
5. **ANA** — Created missing marker file from 2021 compound RTF.
6. **Iron/TIBC split** — Moved TIBC value (53, ref 45-80) out of Iron into TIBC.md.
7. **B6 CSV values** — Timeline CSV had 73→fixed to 105 (Oct 2023), 35→fixed to 73 (Jan 2024). Added missing 196 (Feb 2024) and 147 (Aug 2024).
8. **File rename** — "2. Bloods Jan 18 2024 #2.pdf" → "2. Bloods Jan and Feb 2024 #2.pdf" (user confirmed contains Jan+Feb data).
9. **US B6 (Jun 2023)** — Added 42.5 nmol/L from Quest Diagnostics (original 10.5 ng/mL). Applied conversion factor 1 ng/mL = 4.046 nmol/L. Added footnote in all CSVs and Obsidian.
10. **Dec 2024 RPAH bloods** — Added full panel from Urriola immunology consult. Created new markers: Vitamin E (11 umol/L), Vitamin C (46 umol/L), Chromogranin A (48.2 ug/L), Tryptase (4.2 ug/L). Updated C3 (0.68), C4 (0.13), B12 (587), Active B12 (174), Folate (25.7), B1 (122). Flagged Neutrophils 1.9 (borderline low) and Phosphate 4.21 (possible haemolysis artefact).
11. **"NEW" tags removed** — Removed all green "NEW", "HIST", "UPDATED" labels from HTML report per user preference. Specialist doesn't need change-marking.

## Key Interpretations from Correspondence

- **hEDS** diagnosed 2025 per AI health summary — explains joint deterioration, autonomic features, connective tissue fragility
- **Blood type O** noted in Medical Health Summary
- **Hair mineral analysis (2013)** — Phosphorus, Cobalt, Magnesium deficient. Manganese, Selenium, Boron, Molybdenum bottom of range.
- **ANA** varies — 80-160 on historical tests, negative on Dec 2024 RPAH serology (intermittent pattern)
- **Iron deficiency Mar 2024** was transient — ferritin 18, recovered to 186 by Apr 2024 (likely acute/collection artefact)
- **MCAS-type nocturnal symptoms** — sleep-triggered. Tryptase and Chromogranin A normal Dec 2024, excluding mastocytosis and NET.

## Conversion Factors (US → AU)

| Analyte | US Unit | × Factor | AU Unit | Notes |
|---------|---------|----------|---------|-------|
| Vitamin B6 (P5P) | ng/mL | 4.046 | nmol/L | Quest Diagnostics standard |
