"""
Script: extract_text.py
Purpose: Extract raw text from a PDF file using PyMuPDF
Version: 1.2.0
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.2.0"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

def print_banner():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print("")

def extract_text(pdf_path, verbose=False):
    try:
        doc = fitz.open(pdf_path)
        if verbose:
            print(f"📄 PDF has {len(doc)} pages.")
        all_text = ""
        for i, page in enumerate(doc):
            if verbose:
                print(f"🔍 Extracting page {i + 1}...")
            all_text += page.get_text()
        if verbose:
            print(f"🧾 Extracted text length: {len(all_text)} characters")
        return all_text
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

def save_text(output_path, text, verbose=False):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    if verbose:
        print(f"💾 Saved output to: {output_path}")

def main():
    print_banner()
    if len(sys.argv) < 2:
        print("⚠️ Usage: python extract_text.py <input_pdf_path> [--verbose]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    verbose = "--verbose" in sys.argv

    output_dir = Path(__file__).resolve().parent / "../data/extracted_text"
    output_path = output_dir / (Path(input_pdf).stem + ".txt")

    print(f"📂 Input: {input_pdf}")
    print(f"📝 Output: {output_path}")
    if verbose:
        print("🔊 Verbose mode enabled.")

    text = extract_text(input_pdf, verbose)
    if text:
        save_text(output_path, text, verbose)
        print("✅ Text extraction complete.")
    else:
        print("⚠️ No text extracted.")

if __name__ == "__main__":
    main()
