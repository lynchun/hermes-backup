#!/usr/bin/env python3
"""
Batch de-identify .eml files with specific find-and-replace rules.
Replaces targeted emails, names, ABNs/ACNs, and redacts Manly/Umina addresses.
Deterministic — no LLM needed. All local.

Usage:
    python3 deidentify_eml.py /path/to/folder/
"""

import os
import re
import sys
from pathlib import Path

# --- Replacement rules ---
SUBSTITUTIONS = {
    "khw2095@gmail.com": "k@gmail.com",
    "tgrworner@gmail.com": "t@gmail.com",
    "katrinaworner@bigpond.com": "k@bigpond.com",
    "Katrina": "Karina",
    "Worner": "Smith",
    # Words
    "Leggings": "Meggings",
    "leggings": "meggings",
}

# ABN: XX XXX XXX XXX  (11 digits)
# ACN: XXX XXX XXX     (9 digits)
ABN_RE = re.compile(r'\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b')
ACN_RE = re.compile(r'\b\d{3}\s?\d{3}\s?\d{3}\b')

ABN_RE = re.compile(r'\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b')
ACN_RE = re.compile(r'\b\d{3}\s?\d{3}\s?\d{3}\b')
ADDRESS_LINE_RE = re.compile(r'^.*\b(?:Manly|Umina)\b.*$', re.IGNORECASE | re.MULTILINE)


def apply_substitutions(text: str) -> str:
    for old, new in SUBSTITUTIONS.items():
        text = text.replace(old, new)
    return text


def redact_address_lines(text: str) -> str:
    return ADDRESS_LINE_RE.sub("[ADDRESS REDACTED]", text)


def process_eml(source_path: Path, output_dir: Path) -> bool:
    try:
        with open(source_path, 'rb') as f:
            raw_bytes = f.read()
    except Exception as e:
        print(f"  SKIP: {source_path.name} — {e}")
        return False

    raw_text = raw_bytes.decode('utf-8', errors='replace')

    orig_subject = ""
    for line in raw_text.split('\n'):
        if line.startswith('Subject:'):
            orig_subject = line[len('Subject:'):].strip()
            break

    result = apply_substitutions(raw_text)
    result = redact_address_lines(result)
    result = ABN_RE.sub("[ABN REDACTED]", result)
    result = ACN_RE.sub("[ACN REDACTED]", result)

    if orig_subject:
        result = result.replace(
            f"Subject: {orig_subject}",
            f"Subject: {orig_subject} [DE-IDENTIFIED]", 1)

    stem = source_path.stem
    out_name = f"{stem} [DE-IDENTIFIED].eml"
    out_path = output_dir / out_name

    counter = 1
    while out_path.exists():
        out_name = f"{stem} [DE-IDENTIFIED] ({counter}).eml"
        out_path = output_dir / out_name
        counter += 1

    with open(out_path, 'wb') as f:
        f.write(result.encode('utf-8'))
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 deidentify_eml.py /path/to/folder/ [output_folder]")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_file():
        sources = [target]
    elif target.is_dir():
        sources = sorted(target.glob("*.eml"))
        sources = [s for s in sources if "[DE-IDENTIFIED]" not in s.name]
    else:
        print(f"Not found: {target}")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) >= 3 else \
        target.parent / "Deidentified folder"

    if not sources:
        print("No .eml files to process.")
        return

    new_sources = []
    for s in sources:
        if not (output_dir / f"{s.stem} [DE-IDENTIFIED].eml").exists():
            new_sources.append(s)
    sources = new_sources
    if not sources:
        print("All emails already de-identified. Nothing to do.")
        return

    print(f"Processing {len(sources)} new emails...")
    output_dir.mkdir(parents=True, exist_ok=True)

    ok = fail = 0
    for i, f in enumerate(sources, 1):
        print(f"  [{i}/{len(sources)}] {f.name}", end="")
        if process_eml(f, output_dir):
            ok += 1
            print(" OK")
        else:
            fail += 1
            print(" FAIL")

    print(f"\nDone. {ok} de-identified, {fail} failed.")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
