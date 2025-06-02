"""
Script: parse_visual_toc.py
Version: 1.3.7
Purpose: Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF
"""

print("🛠 parse_visual_toc.py - v1.3.7")
print("📘 Purpose: Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF")
print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
print("")

import sys
import fitz
import argparse
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def extract_visual_toc(pdf_path: Path, verbose=False):
    output_path = OUTPUT_DIR / (pdf_path.stem + ".visual_toc.txt")
    print(f"📂 Processing {pdf_path.name}")
    doc = fitz.open(pdf_path)
    lines = []
    for i in range(min(5, len(doc))):
        page = doc[i]
        text = page.get_text().strip().splitlines()
        for line in text:
            if any(char.isdigit() for char in line) and "." in line:
                lines.append(line)
    if not lines:
        output_path.write_text("No visual TOC detected.\n")
    else:
        output_path.write_text("\n".join(lines))
    if verbose:
        print(f"📝 Output: {output_path}")
    print("✅ Visual TOC extraction complete.")

def prompt_pdf_selection():
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        print("⚠️ No PDFs found in input directory.")
        return None
    print("Select a PDF to process:")
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    choice = input("Enter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(pdfs)):
        print("❌ Invalid selection.")
        return None
    return pdfs[int(choice) - 1]

def main():
    parser = argparse.ArgumentParser(description="Extract visual TOC from a PDF.")
    parser.add_argument("file", nargs="?", help="PDF filename (searched in ../data/input_pdfs/ if not a full path)")
    parser.add_argument("--all", action="store_true", help="Process all PDFs in ../data/input_pdfs/")
    parser.add_argument("--version", "-v", action="version", version="parse_visual_toc.py v1.3.7")
    parser.add_argument("--verbose", action="store_true", help="Show verbose output")
    args = parser.parse_args()

    if args.all:
        for pdf_path in sorted(INPUT_DIR.glob("*.pdf")):
            extract_visual_toc(pdf_path, args.verbose)
        return

    if args.file:
        path = Path(args.file)
        if not path.exists():
            path = INPUT_DIR / args.file
        if not path.exists():
            print(f"❌ File not found: {args.file}")
            return
        extract_visual_toc(path, args.verbose)
        return

    selected = prompt_pdf_selection()
    if selected:
        extract_visual_toc(selected, args.verbose)

if __name__ == "__main__":
    main()
