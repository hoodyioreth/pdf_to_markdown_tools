#!/usr/bin/env python3
"""
Script: convert_to_md.py
Version: 1.0.0
Purpose: Convert raw text and heading data into structured Markdown
"""

import sys
import json
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "convert_to_md.py"
SCRIPT_VERSION = "1.0.0"
SCRIPT_PURPOSE = "Convert extracted text + structure into Markdown"

INPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/converted_md"

def load_headings(base: Path):
    paths = {
        "outline": base.with_suffix(".outline.json"),
        "headings": base.with_suffix(".headings.json"),
        "visual": base.with_suffix(".visual_toc.txt")
    }
    if paths["outline"].exists():
        with open(paths["outline"], "r") as f:
            return json.load(f), "outline"
    elif paths["headings"].exists():
        with open(paths["headings"], "r") as f:
            return json.load(f), "headings"
    elif paths["visual"].exists():
        with open(paths["visual"], "r") as f:
            lines = paths["visual"].read_text().splitlines()
            return [{"text": line.strip(), "page": -1} for line in lines if line.strip()], "visual"
    else:
        return [], None

def convert_to_markdown(txt_path: Path, verbose=False):
    raw_text = txt_path.read_text(encoding="utf-8").splitlines()
    stem = txt_path.stem
    base = INPUT_DIR / stem
    headings, source = load_headings(base)

    output_md = OUTPUT_DIR / f"{stem}.md"
    with open(output_md, "w", encoding="utf-8") as out:
        out.write(f"# Converted Markdown from {stem}\n\n")
        if not headings:
            for line in raw_text:
                out.write(line + "\n")
            if verbose:
                print(f"⚠️ No heading data found for {stem}.")
        else:
            current_idx = 0
            for h in headings:
                out.write(f"\n## {h['text']}\n\n")
                for line in raw_text[current_idx:]:
                    out.write(line + "\n")
                current_idx = len(raw_text)
    print(f"✅ Markdown written: {output_md}")
    if verbose and source:
        print(f"🧠 Structure source: {source}")

def get_txt_files():
    return sorted(INPUT_DIR.glob("*.txt"))

def display_menu(files):
    print("\nSelect a text file to convert:")
    for i, f in enumerate(files, 1):
        print(f"[{i}] {f.name}")
    idx = input("Enter number: ")
    return files[int(idx) - 1]

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
    print(f"📥 Input folder: {INPUT_DIR.resolve()}")
    print(f"📤 Output folder: {OUTPUT_DIR.resolve()}")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = get_txt_files()
    if run_all:
        for f in tqdm(files, desc="📄 Converting all text files"):
            convert_to_markdown(f, verbose)
        return

    if not files:
        print("❌ No .txt files found in extracted_text folder.")
        return

    selected = display_menu(files)
    convert_to_markdown(selected, verbose)

if __name__ == "__main__":
    main()
