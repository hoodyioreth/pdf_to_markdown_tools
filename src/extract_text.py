#!/usr/bin/env python3
""" 
extract_text.py - v1.6.4

Purpose:
Extract raw text from a PDF using PyMuPDF. Supports both single-file and --all batch mode.

Key Features:
- Accepts filename as positional argument
- Supports --all, --help, --version, -v
- Outputs to ../data/extracted_text/

Dependencies:
- PyMuPDF
- tqdm
"""

import argparse
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm
import sys

SCRIPT_NAME = "extract_text.py"
VERSION = "1.6.4"
INPUT_DIR = Path("../data/input_pdfs")
OUTPUT_DIR = Path("../data/extracted_text")

def extract_text_from_pdf(pdf_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (pdf_path.stem + ".txt")

    doc = fitz.open(pdf_path)
    with open(output_path, "w", encoding="utf-8") as out:
        for page in tqdm(doc, desc=f"📄 Extracting {pdf_path.name}", unit="page"):
            text = page.get_text()
            out.write(text)
            out.write("\n")
    doc.close()
    print(f"✅ Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Extract raw text from PDFs")
    parser.add_argument("filename", nargs="?", help="PDF file to process (from input_pdfs/)")
    parser.add_argument("--all", action="store_true", help="Process all PDFs in the input folder")
    parser.add_argument("--version", "-v", action="store_true", help="Show version info and exit")

    args = parser.parse_args()

    print(f"🛠 {SCRIPT_NAME} - v{VERSION}")
    print("📘 Purpose: Extract raw text from a PDF file using PyMuPDF")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
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
            extract_text_from_pdf(pdf_path, OUTPUT_DIR)
        return

    if args.filename:
        pdf_path = INPUT_DIR / args.filename
        if not pdf_path.exists():
            print(f"❌ File not found: {pdf_path}")
            sys.exit(1)
        extract_text_from_pdf(pdf_path, OUTPUT_DIR)
        return

    # Interactive fallback if no args
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
        extract_text_from_pdf(selected, OUTPUT_DIR)
    except (ValueError, IndexError):
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
