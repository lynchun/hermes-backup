#!/bin/bash
# OCR Ingest - drop any image/PDF and get text back
# Usage: ocr_ingest.sh <file_path>

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "ERROR: File not found: $FILE"
    exit 1
fi

# Determine file type
EXT="${FILE##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')

case "$EXT_LOWER" in
    pdf)
        # PDF - convert to images first
        pdftoppm -png -r 72 "$FILE" /tmp/ocr_ingest 2>/dev/null
        for pg in /tmp/ocr_ingest-*.png; do
            [ -f "$pg" ] || continue
            cd /tmp && tesseract "$(basename "$pg")" stdout --psm 6 --oem 1 2>/dev/null
            echo "---"
        done
        rm -f /tmp/ocr_ingest-*.png
        ;;
    png|jpg|jpeg|tiff|tif|bmp|gif)
        # Image - OCR directly
        cp "$FILE" /tmp/ocr_ingest_img.png
        cd /tmp && tesseract ocr_ingest_img.png stdout --psm 6 --oem 1 2>/dev/null
        rm -f /tmp/ocr_ingest_img.png
        ;;
    *)
        echo "ERROR: Unsupported file type: .$EXT"
        exit 1
        ;;
esac
