# Worner/Smith De-Identification Replacement Set

Full replacement set used in production for the BMM/Worner email de-identification.
Both the email script (`deidentify_eml.py`) and PDF script (`bmm_deidentify_pdf.py`)
use identical rules.

## Substitutions (Ordered — apply emails before names)

```python
SUBSTITUTIONS = [
    # Email addresses — replace BEFORE names to avoid partial matches
    ("khw2095@gmail.com", "k@gmail.com"),
    ("tgrworner@gmail.com", "t@gmail.com"),
    ("katrinaworner@bigpond.com", "k@bigpond.com"),
    
    # Names
    ("Katrina", "Karina"),
    ("Worner", "Smith"),
    ("Tim", "Jim"),
    
    # Misc words
    ("Leggings", "Meggings"),
    ("leggings", "meggings"),
]
```

## Regulatory Number Redaction (Regex)

```python
import re

ABN_RE = re.compile(r'\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b')
ACN_RE = re.compile(r'\b\d{3}\s?\d{3}\s?\d{3}\b')
```

## Address Redaction

```python
import re

ADDRESS_LINE_RE = re.compile(
    r'^.*\b(?:Manly|Umina)\b.*$', re.IGNORECASE | re.MULTILINE
)
```

## Script Locations

```
~/Desktop/deidentify_eml.py       # Email de-identification
~/Desktop/bmm_deidentify_pdf.py   # PDF de-identification (Cairo flatten)
~/.hermes/skills/.../scripts/     # Canonical copies in skill directory
```

## Ordering Rule

Email addresses first, then names. Reason: `katrinaworner@bigpond.com` contains
both `katrina` and `worner`. If you replace `Worner→Smith` first, the email becomes
`katrinasmith@bigpond.com` which won't match the email rule. Replace the full
email first, then the individual names.
