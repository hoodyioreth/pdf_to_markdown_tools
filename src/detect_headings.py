#!/usr/bin/env python3
"""
Script: detect_headings.py
Version: 1.0.1
Purpose: Detect section headings in a PDF by analyzing font sizes and positions
"""
print("detect_headings - v1.0.1")
print("Purpose: Detect section headings in a PDF by analyzing font sizes and positions")
print("Requires: PyMuPDF (install via 'pip install pymupdf')")

import sys
import fitz  # PyMuPDF
from pathlib import Path
import json
from tqdm import tqdm

SCRIPT_NAME = "detect_headings.py"
SCRIPT_VERSION = "1.0.1"
SCRIPT_PURPOSE = "Detect likely section headings based on font size and position"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def detect_headings(pdf_path: Path, verbose=False):
    output_json = OUTPUT_DIR / (pdf_path.stem + ".headings.json")
    output_txt = OUTPUT_DIR / (pdf_path.stem + ".headings.txt")

    doc = fitz.open(pdf_path)
    headings = []

    for page_num in tqdm(range(len(doc)), desc="🔎 Scanning for headings"):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    font_size = s["size"]
                    text = s["text"].strip()
                    if len(text) > 0 and font_size >= 12 and not text.isupper():
                        headings.append({
                            "text": text,
                            "size": font_size,
                            "page": page_num + 1
                        })

    if not headings:
        output_txt.write_text("⚠️ No headings detected.\n")
        output_json.write_text("[]")
    else:
        # Sort by page number and descending font size
        headings.sort(key=lambda h: (-h["size"], h["page"]))
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(headings, f, indent=2)
        with open(output_txt, "w", encoding="utf-8") as f:
            for h in headings:
                f.write(f"{h['text']} (p. {h['page']}, size {h['size']})\n")
    if verbose:
        print(f"💾 Saved: {output_txt} and {output_json}")
    print("✅ Heading detection complete.")

def get_pdf_list():
    return sorted(INPUT_DIR.glob("*.pdf"))

def display_menu(pdfs):
    print("\n📥 No file provided.")
    print("Select a PDF to process:")
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    choice = input("Enter number: ")
    return pdfs[int(choice) - 1]

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    show_help = "--help" in sys.argv or "-h" in sys.argv
    show_version = "--version" in sys.argv
    run_all = "--all" in sys.argv

    if show_help:
        print(f"Usage: {SCRIPT_NAME} [--all|--verbose|-v|--version|--help|-h]")
        return
    if show_version:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return

    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = get_pdf_list()
    if run_all:
        if not pdfs:
            print("⚠️ No PDF files found in input directory.")
            return
        for pdf in pdfs:
            print(f"📂 Processing {pdf.name}")
            detect_headings(pdf, verbose)
        return

    if not pdfs:
        print("❌ No PDFs found in input directory.")
        return

    selected = display_menu(pdfs)
    detect_headings(selected, verbose)

if __name__ == "__main__":
    main()
    