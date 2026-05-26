#!/usr/bin/env python3
"""
Deterministic PDF de-identification.
Flattens to lossless PNG at 4000px/300DPI to strip ALL hidden text.
No Ollama needed. All local.

Usage:
    python3 deidentify_pdf.py document.pdf
    python3 deidentify_pdf.py document.pdf output.pdf
    python3 deidentify_pdf.py folder/              # batch process all PDFs
"""

import os, sys, subprocess, tempfile, shutil
from pathlib import Path


def flatten(source_path: Path, output_path: Path):
    """Flatten PDF to lossless PNG images, recombine. Strips all hidden text."""
    import pikepdf
    from PIL import Image

    print(f"\nProcessing: {source_path.name}")

    tmp_dir = tempfile.mkdtemp()
    try:
        # Split into individual page PDFs
        with pikepdf.open(str(source_path)) as pdf:
            num_pages = len(pdf.pages)
            print(f"  Pages: {num_pages}")
            page_pdfs = []
            for i, page in enumerate(pdf.pages):
                w = pikepdf.Pdf.new()
                w.pages.append(page)
                page_path = os.path.join(tmp_dir, f'p{i+1}.pdf')
                w.save(page_path)
                page_pdfs.append(page_path)

        # Convert each page to lossless PNG at 4000px / 300 DPI
        images = []
        for i, pp in enumerate(page_pdfs):
            png_path = os.path.join(tmp_dir, f'p{i+1}.png')
            r = subprocess.run([
                'sips', '-s', 'format', 'png',
                '--resampleWidth', '4000',
                '--setProperty', 'dpiHeight', '300',
                '--setProperty', 'dpiWidth', '300',
                pp, '--out', png_path
            ], capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and os.path.exists(png_path):
                images.append(png_path)
            else:
                print(f"    WARNING: page {i+1} failed: {r.stderr}")

        if not images:
            print("  ERROR: no pages converted!")
            return False

        # Combine into PDF
        imgs = [Image.open(img).convert('RGB') for img in images]
        imgs[0].save(output_path, save_all=True, append_images=imgs[1:],
                     dpi=(300, 300))
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  Saved: {output_path.name} ({size_mb:.1f} MB)")
        return True

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        output = Path(sys.argv[2]) if len(sys.argv) >= 3 else \
            target.parent / f"{target.stem} [DE-IDENTIFIED].pdf"
        flatten(target, output)

    elif target.is_dir():
        sources = sorted(target.glob("*.pdf"))
        sources = [s for s in sources
                   if "[DE-IDENTIFIED]" not in s.name
                   and "REDACTED" not in s.name]
        print(f"Found {len(sources)} PDFs in {target}")
        for s in sources:
            out = target / f"{s.stem} [DE-IDENTIFIED].pdf"
            if out.exists():
                print(f"  SKIP: {s.name} (output exists)")
                continue
            flatten(s, out)

    else:
        print(f"Not found: {target}")
        sys.exit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
