#!/usr/bin/env python3
"""OCR pipeline for phone-screenshot pathology PDFs.
Usage: python3 ocr_pathology.py <path-to-pdf>

Steps:
  1. sips converts PDF page 1 to JPEG (2000px wide)
  2. OpenCV preprocessing: grayscale, CLAHE contrast enhancement, denoise, Otsu threshold
  3. tesseract with LSTM neural net model (PSM 6 for uniform text block)

Pitfall: tesseract 5.5.2 on this machine fails with absolute paths.
This script works around it by copying to /tmp and running from there.
"""
import cv2
import numpy as np
import subprocess
import sys
import os
import shutil

pdf_path = sys.argv[1]
base = '/tmp'
jpg_path = os.path.join(base, 'ocr_input.jpg')
out_path = os.path.join(base, 'ocr_preprocessed.png')

# Step 1: Convert page 1 to JPEG
subprocess.run(
    ['sips', '-s', 'format', 'jpeg', '--resampleWidth', '2000', pdf_path, '--out', jpg_path],
    capture_output=True, timeout=30
)

# Step 2: Read and preprocess
img_bgr = cv2.imread(jpg_path, cv2.IMREAD_COLOR)
if img_bgr is None:
    print("ERROR: could not read image")
    sys.exit(1)

gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)
denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
_, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite(out_path, thresh)

# Step 3: OCR (run from /tmp to avoid tesseract path bug)
orig_dir = os.getcwd()
os.chdir('/tmp')
result = subprocess.run(
    ['tesseract', 'ocr_preprocessed.png', 'stdout', '--psm', '6', '--oem', '1'],
    capture_output=True, timeout=30
)
os.chdir(orig_dir)
print(result.stdout.decode('utf-8', errors='replace').strip())
