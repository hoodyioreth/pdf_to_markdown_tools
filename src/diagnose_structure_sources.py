#!/usr/bin/env python3
"""
Script: diagnose_structure_sources.py
Version: 1.0.0
Purpose: List which structure source (outline, headings, visual) would be used for each PDF
"""
print("diagnose_structure_sources - v1.0.0")
print("Purpose: List which structure source (outline, headings, visual) would be used for each PDF")
print("Requires: PyMuPDF (install via 'pip install pymupdf')")

from pathlib import Path
import json

SCRIPT_NAME = "diagnose_structure_sources.py"
SCRIPT_VERSION = "1.0.0"
SCRIPT_PURPOSE = "List structure source fallback logic per PDF"

BASE = Path(__file__).resolve().parent
PDF_DIR = BASE / "../data/input_pdfs"
TEXT_DIR = BASE / "../data/extracted_text"

def is_valid_outline(data):
    return isinstance(data, list) and len(data) > 1

def diagnose_structure(stem: str):
    paths = {
        "outline": TEXT_DIR / f"{stem}.outline.json",
        "headings": TEXT_DIR / f"{stem}.headings.json",
        "visual": TEXT_DIR / f"{stem}.visual_toc.txt"
    }

    if paths["outline"].exists():
        try:
            with open(paths["outline"], "r") as f:
                outline = json.load(f)
            if is_valid_outline(outline):
                return "outline"
        except:
            return "outline (invalid JSON)"

    if paths["headings"].exists():
        try:
            with open(paths["headings"], "r") as f:
                headings = json.load(f)
            if isinstance(headings, list) and headings:
                return "headings"
        except:
            return "headings (invalid JSON)"

    if paths["visual"].exists():
        lines = paths["visual"].read_text().splitlines()
        if any(line.strip() for line in lines):
            return "visual"

    return "none"

def main():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print(f"📂 PDF folder:  {PDF_DIR.resolve()}")
    print(f"📂 Extracted:   {TEXT_DIR.resolve()}")
    print("")

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print("❌ No PDFs found in input_pdfs folder.")
        return

    print(f"{'PDF File':60} | Structure Source Used")
    print("-" * 90)
    for pdf in pdfs:
        stem = pdf.stem
        result = diagnose_structure(stem)
        print(f"{pdf.name:60} | {result}")

if __name__ == "__main__":
    main()
    