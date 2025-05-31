"""
Script: parse_visual_toc.py
Purpose: Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF
Version: 1.2.1
"""

import sys
from tqdm import tqdm
import fitz  # PyMuPDF
import sys
from pathlib import Path
import re

SCRIPT_NAME = "parse_visual_toc.py"
SCRIPT_VERSION = "1.2.1"
SCRIPT_PURPOSE = "Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def print_banner():
    print(f"\n📥 Expected input:   {INPUT_DIR}")
    print(f"📤 Expected output:  {OUTPUT_DIR}\n")
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print("")

def is_likely_toc_line(line):
    # Heuristic: contains title-like text and ends in a number (page ref)
    return bool(re.search(r'\.{2,}\s*\d+$', line.strip()))

def extract_visual_toc(pdf_path, max_pages=5, verbose=False):
    try:
        doc = fitz.open(pdf_path)
        toc_lines = []
        for i in tqdm(range(min(max_pages, len(doc))), desc='🔍 Scanning pages', unit='page'):
            page = doc[i]
            text = page.get_text()
            lines = text.splitlines()
            for line in lines:
                if is_likely_toc_line(line):
                    toc_lines.append(line.strip())
            if verbose:
                print(f"🔍 Scanned page {i+1}, found {len(toc_lines)} TOC lines so far.")
        return toc_lines
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def save_visual_toc(output_path, toc_lines, verbose=False):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for line in toc_lines:
            f.write(line + "\n")
    if verbose:
        print(f"💾 Saved TOC lines to: {output_path}")


def select_pdf():
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in input folder.")
        sys.exit(1)

    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, f in enumerate(pdf_files, start=1):
        print(f"[{i}] {f.name}")

    choice = input("Enter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(pdf_files)):
        print("❌ Invalid selection.")
        sys.exit(1)

    return pdf_files[int(choice) - 1]

def main():
    print_banner()
    if len(sys.argv) < 2:
        print("⚠️ Usage: python parse_visual_toc.py <input_pdf_path> [--verbose]")
        sys.exit(1)

    input_pdf = select_pdf() if len(sys.argv) < 2 or sys.argv[1].startswith("--") else Path(sys.argv[1])
    verbose = "--verbose" in sys.argv

    output_dir = Path(__file__).resolve().parent / "../data/extracted_text"
    output_path = output_dir / (Path(input_pdf).stem + ".visual_toc.txt")

    print(f"📂 Input: {input_pdf}")
    print(f"📝 Output: {output_path}")
    if verbose:
        print("🔊 Verbose mode enabled.")

    toc_lines = extract_visual_toc(input_pdf, verbose=verbose)
    if toc_lines:
        save_visual_toc(output_path, toc_lines, verbose)
        print("✅ Visual TOC extraction complete.")
    else:
        print("⚠️ No visual TOC lines detected.")

if __name__ == "__main__":
    main()
