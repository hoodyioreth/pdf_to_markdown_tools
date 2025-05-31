"""
Script: extract_text.py
Purpose: Extract raw text from a PDF file using PyMuPDF
Version: 1.4.0
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.4.0"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def print_banner():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')\n")
    print(f"📥 Expected input:   {INPUT_DIR}")
    print(f"📤 Expected output:  {OUTPUT_DIR}\n")

def select_pdf():
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in input folder.")
        sys.exit(1)

    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, f in enumerate(pdf_files, start=1):
        print(f"[{i}] {f.name}")

    choice = input("Enter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(pdf_files)):
        print("❌ Invalid selection.")
        sys.exit(1)

    return pdf_files[int(choice) - 1]

def extract_text(pdf_path, verbose=False):
    try:
        doc = fitz.open(pdf_path)
        if verbose:
            print(f"📄 PDF has {len(doc)} pages.")
        all_text = ""
        for page in (doc if verbose else tqdm(doc, desc="📄 Extracting pages", unit="page")):
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
    verbose = "--verbose" in sys.argv

    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        input_pdf = select_pdf()
    else:
        input_pdf = Path(sys.argv[1])

    output_path = OUTPUT_DIR / (input_pdf.stem + ".txt")

    print(f"📂 Input: {input_pdf}")
    print(f"📝 Output: {output_path}")
    if verbose:
        print("🔊 Verbose mode enabled.")
    else:
        print("📊 Progress bar active...")

    text = extract_text(input_pdf, verbose)
    if text:
        save_text(output_path, text, verbose)
        print("✅ Text extraction complete.")
    else:
        print("⚠️ No text extracted.")

if __name__ == "__main__":
    main()
