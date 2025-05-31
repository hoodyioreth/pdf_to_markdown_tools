
"""
Script: extract_text.py

Purpose: Extract raw text from a PDF file using PyMuPDF

Version: 1.6.2
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.6.2"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text(pdf_path: Path, verbose=False):
    output_path = OUTPUT_DIR / (pdf_path.stem + ".txt")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output: {output_path}")
    else:
        print(f"📘 Processing: {pdf_path.name}")
    with fitz.open(pdf_path) as doc, open(output_path, "w", encoding="utf-8") as out_file:
        for page in tqdm(doc, desc="📄 Extracting pages", unit="page", disable=not verbose):
            text = page.get_text()
            out_file.write(text + "\n")
    print("✅ Text extraction complete.")

def select_pdf():
    files = sorted(INPUT_DIR.glob("*.pdf"))
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, f in enumerate(files, 1):
        print(f"[{i}] {f.name}")
    choice = input("Enter number: ")
    return files[int(choice) - 1]

def main():
    args = sys.argv
    verbose = "--verbose" in args or "-v" in args
    show_help = "--help" in args or "-h" in args
    show_version = "--version" in args
    run_all = "--all" in args

    if show_help:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--all]")
        return

    if show_version:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return

    if run_all:
        files = sorted(INPUT_DIR.glob("*.pdf"))
        for f in files:
            extract_text(f, verbose)
        return

    # Manual selection
    pdf_file = select_pdf()
    extract_text(pdf_file, verbose)

if __name__ == "__main__":
    main()
