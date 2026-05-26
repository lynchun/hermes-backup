#!/usr/bin/env python3
"""
BMM PDF De-identifier — Cairo Edition
=======================================
Renders PDF pages using Cairo (poppler) at 200 DPI, then recombines
into a lossless PDF. Removes ALL hidden text, preserves crisp quality.

Quality: 200 DPI (screen-sharp, ~1 MB per 5 pages)
Output:  Lossless DEFLATE PDF (via img2pdf)
Speed:   ~1 min per 20-page document

Requires: pdftocairo (from poppler), img2pdf, Python 3

Usage:
    python3 bmm_deidentify_pdf.py document.pdf
    python3 bmm_deidentify_pdf.py folder/
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def flatten_pdf(source_path: Path, output_path: Path):
    """Flatten a PDF using Cairo renderer at 200 DPI."""
    print(f"\nProcessing: {source_path.name}")

    tmp_dir = tempfile.mkdtemp()
    png_dir = os.path.join(tmp_dir, 'pngs')
    os.makedirs(png_dir)

    try:
        prefix = os.path.join(png_dir, 'page')
        r = subprocess.run([
            'pdftocairo', '-png', '-r', '200',
            str(source_path), prefix
        ], capture_output=True, text=True, timeout=300)

        if r.returncode != 0:
            print(f"  ERROR: pdftocairo failed — {r.stderr}")
            return False

        pages = sorted(
            [os.path.join(png_dir, f) for f in os.listdir(png_dir) if f.endswith('.png')]
        )
        if not pages:
            print("  ERROR: no pages rendered")
            return False

        print(f"  Pages: {len(pages)}")

        import img2pdf
        with open(output_path, 'wb') as f:
            f.write(img2pdf.convert(pages, dpi=200))

        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  Saved: {output_path.name} ({size_mb:.1f} MB)")
        return True

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


def verify_clean(pdf_path: Path) -> bool:
    """Verify the output has no extractable text."""
    r = subprocess.run(
        ['pdftotext', str(pdf_path), '-'],
        capture_output=True, text=True, timeout=15
    )
    char_count = len(r.stdout.strip())
    if char_count > 50:
        print(f"  WARNING: {char_count} chars of hidden text remain")
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        output = Path(sys.argv[2]) if len(sys.argv) >= 3 else \
            target.parent / f"{target.stem} [DE-IDENTIFIED].pdf"
        flatten_pdf(target, output)
        if verify_clean(output):
            print("  Verification: DE-IDENTIFIED (no hidden text)")
        else:
            print("  Verification: FAILED — inspect output manually")

    elif target.is_dir():
        sources = sorted(target.glob("*.pdf"))
        sources = [s for s in sources
                   if "[DE-IDENTIFIED]" not in s.name
                   and "REDACTED" not in s.name]
        print(f"Found {len(sources)} PDFs in {target}")
        clean_count = 0
        for s in sources:
            out = target / f"{s.stem} [DE-IDENTIFIED].pdf"
            if out.exists():
                print(f"  SKIP: {s.name}")
                continue
            flatten_pdf(s, out)
            if verify_clean(out):
                clean_count += 1
                print(f"  Verification: CLEAN")
            else:
                print(f"  Verification: FAILED")
        print(f"\nDone. {clean_count}/{len(sources)} clean")

    else:
        print(f"Not found: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
