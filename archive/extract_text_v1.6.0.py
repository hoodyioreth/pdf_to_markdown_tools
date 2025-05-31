# Script: extract_text.py
# Version: 1.6.0
# Purpose: Extract raw text from a PDF file using PyMuPDF

import sys
import fitz  # PyMuPDF
from pathlib import Path
from rich.progress import track

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.6.0"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def select_pdf():
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, file in enumerate(pdf_files, 1):
        print(f"[{i}] {file.name}")
    selection = int(input("Enter number: ")) - 1
    return pdf_files[selection]

def extract_text(pdf_path, verbose=False):
    output_txt = OUTPUT_DIR / (pdf_path.stem + ".txt")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output: {output_txt}")
        print("📊 Progress bar active...")

    doc = fitz.open(pdf_path)
    with open(output_txt, "w", encoding="utf-8") as out:
        for page in track(doc, description="📄 Extracting pages"):
            text = page.get_text()
            out.write(text)
    print("✅ Text extraction complete.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(f"Usage: {SCRIPT_NAME} <input.pdf> [--verbose|-v|--version|-h]")
        sys.exit(0)
    if "--version" in args:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        sys.exit(0)

    verbose = "--verbose" in args or "-v" in args
    args = [arg for arg in args if not arg.startswith("-")]
    file_arg = args[0] if args else None
    pdf_path = Path(file_arg) if file_arg else select_pdf()
    extract_text(pdf_path, verbose)