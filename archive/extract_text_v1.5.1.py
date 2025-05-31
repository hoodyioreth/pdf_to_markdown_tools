"""
Script: extract_text.py
Version: 1.5.1
Purpose: Extract raw text from a PDF file using PyMuPDF
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.5.1"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

# Check CLI flags before anything else
if "--help" in sys.argv or "-h" in sys.argv:
    print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h]")
    sys.exit(0)

if "--version" in sys.argv:
    print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
    sys.exit(0)

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv

if VERBOSE:
    print("🔍 TRACE: top-level execution begins")

def select_pdf(verbose=False):
    if verbose:
        print("🔍 TRACE: select_pdf() called")
    print("📥 No file provided.")
    print("Select a PDF to process:")
    files = sorted(INPUT_DIR.glob("*.pdf"))
    for idx, file in enumerate(files, 1):
        print(f"[{idx}] {file.name}")
    try:
        selection = int(input("Enter number: "))
        return files[selection - 1]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        sys.exit(1)

def extract_text(pdf_path, verbose=False):
    if verbose:
        print(f"🔍 TRACE: extract_text({pdf_path.name})")
    output_path = OUTPUT_DIR / (pdf_path.stem + ".txt")
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    with open(output_path, "w", encoding="utf-8") as out_file:
        print("📊 Progress bar active...")
        for page in tqdm(doc, desc="📄 Extracting pages", unit="page"):
            text = page.get_text()
            out_file.write(text)
    print(f"✅ Text extraction complete.")

def main():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')
")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}
")

    pdf_path = select_pdf(verbose=VERBOSE)
    print(f"📂 Input: {pdf_path}")
    print(f"📝 Output: {OUTPUT_DIR / (pdf_path.stem + '.txt')}")
    if VERBOSE:
        print("🔊 Verbose mode enabled.")
    extract_text(pdf_path, verbose=VERBOSE)

if __name__ == "__main__":
    if VERBOSE:
        print("🔍 TRACE: defining main()")
    main()
