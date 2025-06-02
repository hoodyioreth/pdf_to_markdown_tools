#!/usr/bin/env python3
""" 
detect_headings.py - v1.0.2

Purpose:
Detect and extract headings from a PDF file based on font size heuristics.

Key Features:
- Accepts single filename (positional)
- Supports --all batch processing
- Fallback to interactive selection
- Compatible with interactive_pipeline.py

Dependencies:
- PyMuPDF
- tqdm
"""

import argparse
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm
import json
import sys

SCRIPT_NAME = "detect_headings.py"
VERSION = "1.0.2"
INPUT_DIR = Path("../data/input_pdfs")
OUTPUT_DIR = Path("../data/extracted_text")

def detect_headings_from_pdf(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    headings = []

    for page in tqdm(doc, desc=f"🔎 Scanning {pdf_path.name}", unit="page"):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)
                    if text and len(text) < 100 and size >= 14:  # heuristic
                        headings.append(text)

    output_path = output_dir / (pdf_path.stem + ".headings.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(headings, f, indent=2)
    doc.close()
    print(f"✅ Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Detect headings from PDF by font size")
    parser.add_argument("filename", nargs="?", help="PDF file to process (from input_pdfs/)")
    parser.add_argument("--all", action="store_true", help="Process all PDFs in the input folder")
    parser.add_argument("--version", "-v", action="store_true", help="Show version info and exit")

    args = parser.parse_args()

    print(f"🛠 {SCRIPT_NAME} - v{VERSION}")
    print("📘 Purpose: Detect headings from PDFs using font size heuristics")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}")

    if args.version:
        sys.exit(0)

    if args.all:
        files = list(INPUT_DIR.glob("*.pdf"))
        if not files:
            print("❌ No PDF files found in input folder.")
            sys.exit(1)
        for pdf_path in files:
            detect_headings_from_pdf(pdf_path, OUTPUT_DIR)
        return

    if args.filename:
        pdf_path = INPUT_DIR / args.filename
        if not pdf_path.exists():
            print(f"❌ File not found: {pdf_path}")
            sys.exit(1)
        detect_headings_from_pdf(pdf_path, OUTPUT_DIR)
        return

    # Interactive fallback
    files = list(INPUT_DIR.glob("*.pdf"))
    if not files:
        print("❌ No PDF files found in input folder.")
        return

    print("\n📄 Available PDFs:")
    for i, file in enumerate(files):
        print(f"[{i}] {file.name}")
    choice = input("\nEnter number: ").strip()
    try:
        selected = files[int(choice)]
        detect_headings_from_pdf(selected, OUTPUT_DIR)
    except (ValueError, IndexError):
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
