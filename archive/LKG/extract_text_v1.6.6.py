#!/usr/bin/env python3
"""
Script: extract_text.py
Version: 1.6.3
Purpose: Extract raw text from PDFs using PyMuPDF
Supports: --all, --verbose/-v, --help/-h, --version
"""

import fitz  # PyMuPDF
import sys
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.6.3"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def extract_text_from_pdf(pdf_path, verbose=False):
    filename = pdf_path.name
    if verbose:
        print(f"🔍 TRACE: Extracting from {filename}")
    else:
        print(f"📂 Processing {filename}")

    output_path = OUTPUT_DIR / f"{filename.replace('.pdf', '.txt')}"
    doc = fitz.open(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for page in tqdm(doc, desc="📄 Extracting pages"):
            text = page.get_text()
            f.write(text)
    print("✅ Text extraction complete.")

def get_pdf_list():
    return sorted([f for f in INPUT_DIR.glob("*.pdf")])

def display_menu(pdf_files):
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for idx, pdf in enumerate(pdf_files, 1):
        print(f"[{idx}] {pdf.name}")
    choice = int(input("Enter number: "))
    return pdf_files[choice - 1]

def main():
    args = sys.argv
    verbose = "--verbose" in args or "-v" in args
    all_mode = "--all" in args

    if "--help" in args or "-h" in args:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--all]")
        return

    if "--version" in args:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return

    pdf_files = get_pdf_list()

    if all_mode:
        for pdf_path in pdf_files:
            extract_text_from_pdf(pdf_path, verbose)
        return

    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}")

    selected_pdf = display_menu(pdf_files)
    extract_text_from_pdf(selected_pdf, verbose)

if __name__ == "__main__":
    main()
