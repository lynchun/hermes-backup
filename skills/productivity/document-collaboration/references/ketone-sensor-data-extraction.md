# Extracting and Structuring Sensor Data from Excel

Workflow for extracting continuous monitoring data (ketone sensors, glucose monitors, etc.) from exported Excel files and structuring it for reporting.

## Source Data Shape

KetoCheck and similar sensors export as `.xlsx` files with:
- 1 sheet, named by sensor ID
- 3 columns: `No. | Time | Sensor reading(mmol/L)`
- 5-minute interval readings (~288 per day, ~3,000-4,000 per 12-15 day sensor)
- Session 1 and Session 2 come as separate files

## Extraction Pipeline

### 1. Read Excel Files

```python
import openpyxl
from datetime import datetime
from collections import defaultdict

base = '/path/to/ketones/folder'
files = ['sensor1.xlsx', 'sensor2.xlsx']

for f in files:
    fp = f'{base}/{f}'
    wb = openpyxl.load_workbook(fp, data_only=True)
    ws = wb[wb.sheetnames[0]]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is not None:
            try:
                val = float(row[2])  # value may come as string
                rows.append({'no': row[0], 'time': str(row[1]), 'value': val})
            except (ValueError, TypeError):
                pass
```

### 2. Daily Statistics

```python
daily = defaultdict(list)
for r in rows:
    day = r['time'][:10]
    daily[day].append(r['value'])

daily_stats = []
for d in sorted(daily.keys()):
    vals = daily[d]
    daily_stats.append({
        'date': d,
        'count': len(vals),
        'mean': round(sum(vals)/len(vals), 3),
        'min': round(min(vals), 2),
        'max': round(max(vals), 2)
    })
```

### 3. Key Metrics to Extract

| Metric | How | Why |
|--------|-----|-----|
| Overall mean/median | `sum(vals)/len(vals)`, sorted median | Compare sensors year-over-year |
| Time in range | Bucket into <0.5, 0.5-1.0, 1.0-1.5, 1.5+ | Shows % time in ketosis |
| First 24h vs last 24h | `rows[:288]` vs `rows[-288:]` | Detects sensor insertion spike vs end-of-life drift |
| Daily trend | Day-by-day means | Shows lifecycle drift pattern |
| Hourly pattern | Group by hour of day (0-23) | Circadian rhythm — overnight vs midday |

### 4. Clinically Relevant Observations

For a keto doctor (Dr Mason): 
- **Well-adapted carnivore pattern**: >95% of readings below 1.0 mmol/L, with most below 0.5
- **Sensor insertion spike**: elevated readings in first 24-48h (local tissue reaction, not true systemic elevation)
- **Baseline drift**: gentle decline over sensor lifetime (~0.5-0.6 in first week → ~0.2-0.3 in final days)
- **Circadian pattern**: higher overnight/evening, lowest midday (consistent with fasting physiology)

### 5. HTML Section Output

Build as a self-contained dashboard section matching the existing `health_markers_for_dr_mason.html` style:

- Sensor summary cards (two-column layout)
- Daily average comparison table (side-by-side sensor lifecycle)
- Time-in-range distribution table
- Hourly pattern (24h breakdown)
- Clinical interpretation callout

## Pitfalls

- **Value type**: openpyxl may return numeric values as strings when the sensor records them as text. Always cast with `float()`.
- **Partial days**: Day 1 and last day of each sensor have fewer readings (partial start/end). Don't compare by raw count.
- **Newline in f-strings**: Python 3.9 doesn't allow `\n` inside f-string expressions. Write multi-line scripts to files instead of inline.
- **execute_code sandbox**: Uses a different Python env than terminal. For library-dependent tasks (openpyxl, playwright, google-api), always use `terminal()` directly.
