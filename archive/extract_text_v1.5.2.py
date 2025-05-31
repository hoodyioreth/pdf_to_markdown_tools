"""
Script: extract_text.py

Purpose: Extract raw text from a PDF file using PyMuPDF

Version: 1.5.2
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.5.2"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def print_usage():
    print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--help]")
    sys.exit(0)

def print_version():
    print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
    sys.exit(0)

def list_pdfs(directory):
    return sorted([f for f in directory.glob("*.pdf")])

def select_pdf(verbose=False):
    pdf_files = list_pdfs(INPUT_DIR)
    if not pdf_files:
        print("❌ No PDF files found in input directory.")
        sys.exit(1)

    print("📥 No file provided.
Select a PDF to process:")
    for i, file in enumerate(pdf_files, start=1):
        print(f"[{i}] {file.name}")
    choice = int(input("Enter number: "))
    selected = pdf_files[choice - 1]
    if verbose:
        print(f"🔍 TRACE: Selected PDF = {selected}")
    return selected

def extract_text(pdf_path, output_path, verbose=False):
    doc = fitz.open(pdf_path)
    with open(output_path, "w", encoding="utf-8") as out_file:
        for page in tqdm(doc, desc="📄 Extracting pages", unit="page"):
            text = page.get_text()
            out_file.write(text + "\n")
    if verbose:
        print(f"💾 Saved extracted text to: {output_path}")

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
    if "--version" in sys.argv:
        print_version()

    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')
")

    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}
")

    pdf_path = select_pdf(verbose=verbose)
    output_file = OUTPUT_DIR / (pdf_path.stem + ".txt")

    extract_text(pdf_path, output_file, verbose=verbose)
    print("✅ Text extraction complete.")

if __name__ == "__main__":
    if "--verbose" in sys.argv or "-v" in sys.argv:
        print("🔍 TRACE: top-level execution begins")
    main()
