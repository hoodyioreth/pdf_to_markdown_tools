#!/usr/bin/env python3
"""
Script: convert_to_md.py
Version: 1.0.4
Purpose: Convert extracted text and heading data into structured Markdown from PDF selection
"""

import sys
import json
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "convert_to_md.py"
SCRIPT_VERSION = "1.0.4"
SCRIPT_PURPOSE = "Convert extracted text + structure into Markdown, selected by PDF"

INPUT_PDF_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
TEXT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/converted_md"

def load_headings(stem: str):
    def is_valid_outline(data):
        return isinstance(data, list) and len(data) > 1

    paths = {
        "outline": TEXT_DIR / f"{stem}.outline.json",
        "headings": TEXT_DIR / f"{stem}.headings.json",
        "visual": TEXT_DIR / f"{stem}.visual_toc.txt"
    }

    if paths["outline"].exists():
        with open(paths["outline"], "r") as f:
            data = json.load(f)
        if is_valid_outline(data):
            return data, "outline"
    if paths["headings"].exists():
        with open(paths["headings"], "r") as f:
            data = json.load(f)
        if data:
            return data, "headings"
    if paths["visual"].exists():
        lines = paths["visual"].read_text().splitlines()
        visual = [line.strip() for line in lines if line.strip()]
        if visual:
            return visual, "visual"
    return [], None

def convert_to_markdown(stem: str, verbose=False):
    text_path = TEXT_DIR / f"{stem}.txt"
    if not text_path.exists():
        print(f"❌ Missing extracted text file: {text_path.name}")
        return

    raw_text = text_path.read_text(encoding="utf-8").splitlines()
    headings, source = load_headings(stem)

    if source:
        print(f"🧠 Using structure source: {source}")
    else:
        print(f"⚠️ No structure source found for {stem}. Output will be unstructured.")

    output_md = OUTPUT_DIR / f"{stem}.md"
    with open(output_md, "w", encoding="utf-8") as out:
        out.write(f"# Converted Markdown from {stem}\n\n")
        if not headings:
            for line in raw_text:
                out.write(line + "\n")
        else:
            current_idx = 0
            for h in headings:
                text = h["text"] if isinstance(h, dict) else h
                out.write(f"\n## {text}\n\n")
                for line in raw_text[current_idx:]:
                    out.write(line + "\n")
                current_idx = len(raw_text)
    print(f"✅ Markdown written: {output_md}")
    if verbose and source:
        print(f"📁 Used extracted text: {text_path}")
        print(f"📄 Structure file type: {source}")

def get_pdf_list():
    return sorted(INPUT_PDF_DIR.glob("*.pdf"))

def display_menu(pdfs):
    print("\nSelect a PDF to convert to Markdown:")
    print("[0] Exit")
    for i, f in enumerate(pdfs, 1):
        print(f"[{i}] {f.name}")
    idx = input("Enter number: ")
    if idx.strip() == "0":
        print("👋 Exiting.")
        sys.exit(0)
    return pdfs[int(idx) - 1]

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
    print(f"📥 Input PDFs:        {INPUT_PDF_DIR.resolve()}")
    print(f"📂 Extracted text:    {TEXT_DIR.resolve()}")
    print(f"📤 Output Markdown:   {OUTPUT_DIR.resolve()}")

    INPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = get_pdf_list()
    if run_all:
        for pdf in tqdm(pdfs, desc="📄 Converting all PDFs"):
            convert_to_markdown(pdf.stem, verbose)
        return

    if not pdfs:
        print("❌ No PDFs found in input_pdfs folder.")
        return

    selected = display_menu(pdfs)
    convert_to_markdown(selected.stem, verbose)

if __name__ == "__main__":
    main()
