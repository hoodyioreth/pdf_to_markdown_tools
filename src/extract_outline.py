
#!/usr/bin/env python3
"""
extract_outline.py - v1.0.0
Purpose: Extract the PDF's outline (bookmarks) and save as outline.json
"""

import os
import fitz  # PyMuPDF
import argparse
import json
from tqdm import tqdm

SCRIPT_NAME = "extract_outline.py"
VERSION = "v1.0.0"

INPUT_DIR = "../data/input_pdfs"
OUTPUT_DIR = "../data/extracted_text"

def extract_outline(pdf_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.outline.json")

    doc = fitz.open(pdf_path)
    outline = doc.get_toc(simple=True)  # [ [level, title, page], ... ]
    doc.close()

    json_ready = [
        {"level": item[0], "title": item[1], "page": item[2]}
        for item in outline
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_ready, f, indent=2)

    print(f"✅ Extracted outline: {os.path.basename(output_path)}")

def list_pdfs():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    return sorted(files)

def main():
    print(f"🛠 {SCRIPT_NAME} - {VERSION}")
    print("📘 Purpose: Extract PDF bookmarks (outline) to .outline.json")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="PDF filename to extract outline from")
    parser.add_argument("--all", action="store_true", help="Extract from all PDFs")
    parser.add_argument("--version", "-v", action="version", version=VERSION)

    args = parser.parse_args()

    pdfs = list_pdfs()

    if args.all:
        for f in tqdm(pdfs, desc="Extracting outlines"):
            extract_outline(os.path.join(INPUT_DIR, f))
    elif args.file:
        target = os.path.join(INPUT_DIR, args.file)
        if not os.path.exists(target):
            print("❌ File not found.")
            return
        extract_outline(target)
    else:
        if not pdfs:
            print("❌ No PDF files found.")
            return

        print("\n📄 Available PDFs:")
        for i, f in enumerate(pdfs):
            print(f"[{i}] {f}")
        choice = input("Enter number (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            return
        if not choice.isdigit() or int(choice) >= len(pdfs):
            print("❌ Invalid selection.")
            return
        selected = pdfs[int(choice)]
        extract_outline(os.path.join(INPUT_DIR, selected))

if __name__ == "__main__":
    main()
