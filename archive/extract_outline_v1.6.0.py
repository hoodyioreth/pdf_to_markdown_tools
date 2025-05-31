"""
Script: extract_outline.py
Purpose: Extract the internal PDF outline (bookmarks) if available
Version: 1.5.1
"""

import sys
import fitz  # PyMuPDF

# CLI argument parsing
if "--help" in sys.argv or "-h" in sys.argv:
    print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h]")
    sys.exit(0)
if "--version" in sys.argv:
    print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
    sys.exit(0)
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv

import json
from pathlib import Path

if "--verbose" in sys.argv:
    print("🔍 TRACE: top-level execution begins")

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "1.5.1"
SCRIPT_PURPOSE = "Extract the internal PDF outline (bookmarks) if available"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

if "--verbose" in sys.argv:
    print("🔍 TRACE: defining select_pdf()")
def select_pdf():
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    if "--verbose" in sys.argv:
        print("🔍 TRACE: select_pdf() called")
    if not pdf_files:
        print("❌ No PDF files found in input directory.")
        sys.exit(1)

    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, file in enumerate(pdf_files, 1):
        print(f"[{i}] {file.name}")

    choice = int(input("Enter number: "))
    return pdf_files[choice - 1]

if "--verbose" in sys.argv:
    print("🔍 TRACE: defining main()")
def main():
    print(f"\n📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}\n")

    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')\n")

    verbose = "--verbose" in sys.argv
    if VERBOSE:
        print("🔍 TRACE: main() entered")

    input_pdf = select_pdf() if len(sys.argv) < 2 or sys.argv[1].startswith("--") else Path(sys.argv[1])

    txt_output = OUTPUT_DIR / f"{input_pdf.stem}.outline.txt"
    json_output = OUTPUT_DIR / f"{input_pdf.stem}.outline.json"

    print(f"📂 Input: {input_pdf}")
    print(f"📝 Output TXT: {txt_output}")
    print(f"📝 Output JSON: {json_output}")

    doc = fitz.open(input_pdf)
    outline = doc.get_toc(simple=True)

    if VERBOSE:
        print("🔊 Verbose mode enabled.")

    if outline:
        with open(txt_output, "w", encoding="utf-8") as f:
            for entry in outline:
                f.write(f"{entry}\n")

        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(outline, f, indent=2)

        print(f"📚 Found {len(outline)} outline entries.")
        print(f"💾 Saved outline TXT to: {txt_output}")
        print(f"💾 Saved outline JSON to: {json_output}")
        print("✅ Outline extraction complete.")
    else:
        with open(txt_output, "w", encoding="utf-8") as f:
            f.write("⚠️ No outline/bookmarks found in this PDF.\n")
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        print("⚠️ No outline extracted.")

    if VERBOSE:
        print("🔍 TRACE: main() exited")

if __name__ == "__main__":
    main()