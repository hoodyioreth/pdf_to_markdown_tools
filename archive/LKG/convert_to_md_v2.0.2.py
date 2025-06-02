#!/usr/bin/env python3
"""
Script: convert_to_md.py
Version: 2.0.2
Purpose: Convert extracted text and structure metadata into well-formatted Markdown.
Author: Sean Hood + ChatGPT
"""
print("convert_to_md - v2.0.2")
print("Purpose: Convert extracted text and structure metadata into well-formatted Markdown.")
print("Requires: PyMuPDF (install via 'pip install pymupdf')")

import sys
import json
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "convert_to_md.py"
SCRIPT_VERSION = "2.0.0"
SCRIPT_PURPOSE = "Convert extracted text + structure (headings/TOC) into clean Markdown output."

# Directory layout (relative to src/)
BASE_DIR = Path(__file__).resolve().parent
INPUT_PDF_DIR = BASE_DIR / "../data/input_pdfs"
TEXT_DIR = BASE_DIR / "../data/extracted_text"
OUTPUT_DIR = BASE_DIR / "../data/converted_md"

def print_header():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print(f"📥 Text input:       {TEXT_DIR.resolve()}")
    print(f"📤 Markdown output:  {OUTPUT_DIR.resolve()}")

def parse_cli_args():
    return {
        "verbose": "--verbose" in sys.argv,
        "show_help": "--help" in sys.argv or "-h" in sys.argv,
        "show_version": "--version" in sys.argv or "-v" in sys.argv,
        "run_all": "--all" in sys.argv
    }

def load_text_file(stem):
    txt_path = TEXT_DIR / f"{stem}.txt"
    if not txt_path.exists():
        return None, f"Missing: {txt_path.name}"
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    return lines, None

def load_heading_structure(stem):
    """Try outline -> headings -> visual TOC, in fallback order."""
    candidates = [
        (TEXT_DIR / f"{stem}.outline.json", "outline"),
        (TEXT_DIR / f"{stem}.headings.json", "headings"),
        (TEXT_DIR / f"{stem}.visual_toc.txt", "visual")
    ]
    for path, label in candidates:
        if path.exists():
            if path.suffix == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return data, label
            elif path.suffix == ".txt":
                lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
                return lines, label
    return [], None

def segment_paragraphs(lines):
    """Simple paragraph joiner: collapse single line breaks into paras."""
    paragraphs = []
    para = []
    for line in lines:
        if line.strip() == "":
            if para:
                paragraphs.append(" ".join(para).strip())
                para = []
        else:
            para.append(line.strip())
    if para:
        paragraphs.append(" ".join(para).strip())
    return paragraphs

def write_markdown(stem, lines, headings, source, verbose=False):
    md_path = OUTPUT_DIR / f"{stem}.md"
    with open(md_path, "w", encoding="utf-8") as out:
        out.write(f"# {stem}\n\n")
        if not headings:
            for p in segment_paragraphs(lines):
                out.write(p + "\n\n")
        else:
            out.write(f"<!-- Structure source: {source} -->\n\n")
            for heading in headings:
                text = heading["text"] if isinstance(heading, dict) else heading
                out.write(f"## {text}\n\n")
            for p in segment_paragraphs(lines):
                out.write(p + "\n\n")

    print(f"✅ Converted {stem} → {md_path.name} (Structure: {source or 'None'})")


def convert_file(stem, verbose=False):
    print(f"🔍 Attempting to convert: {stem}")

    lines, err = load_text_file(stem)
    if err:
        print(f"❌ Skipped {stem}: {err}")
        return
    headings, source = load_heading_structure(stem)
    write_markdown(stem, lines, headings, source, verbose)

def list_pdf_stems():
    return sorted([f.stem for f in INPUT_PDF_DIR.glob("*.pdf")])

def interactive_menu(stems):
    print("\nChoose a PDF to convert to Markdown:")
    for i, s in enumerate(stems, 1):
        print(f"[{i}] {s}")
    choice = input("Enter number (0 to exit): ").strip()
    if choice == "0":
        sys.exit(0)
    return stems[int(choice) - 1]

def main():
    args = parse_cli_args()
    if args["show_help"]:
        print(f"Usage: {SCRIPT_NAME} [--all|--verbose|-v|--version|--help|-h]")
        return
    if args["show_version"]:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return

    print_header()
    INPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stems = list_pdf_stems()
    if args["run_all"]:
        for stem in tqdm(stems, desc="📄 Converting all PDFs"):
            convert_file(stem, verbose=args["verbose"])
        return

    if not stems:
        print("❌ No PDFs found.")
        return

    chosen = interactive_menu(stems)
    convert_file(chosen, verbose=True)

if __name__ == "__main__":
    main()