"""
Script: parse_visual_toc.py
Purpose: Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF
Version: 1.3.0
"""

import sys
import fitz  # PyMuPDF
from pathlib import Path

SCRIPT_NAME = "parse_visual_toc.py"
SCRIPT_VERSION = "1.3.0"
SCRIPT_PURPOSE = "Attempt to extract a visual Table of Contents (TOC) from the first few pages of a PDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

if "--verbose" in sys.argv:
    print("🔍 TRACE: top-level execution begins")


def select_pdf():
    if "--verbose" in sys.argv:
        print("🔍 TRACE: select_pdf() called")
    files = sorted(INPUT_DIR.glob("*.pdf"))
    if not files:
        print("❌ No PDF files found in input directory.")
        sys.exit(1)
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for idx, file in enumerate(files, start=1):
        print(f"[{idx}] {file.name}")
    choice = input("Enter number: ")
    try:
        idx = int(choice) - 1
        return files[idx]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        sys.exit(1)


def main():
    if "--verbose" in sys.argv:
        print("🔍 TRACE: main() entered")
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
        input_path = Path(sys.argv[1])
    else:
        input_path = select_pdf()

    output_txt = OUTPUT_DIR / (input_path.stem + ".visual_toc.txt")
    print(f"📂 Input: {input_path}")
    print(f"📝 Output: {output_txt}")

    doc = fitz.open(input_path)
    toc_text = ""
    for page in doc.pages(0, min(5, len(doc))):
        text = page.get_text()
        toc_text += text + "\n"

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(toc_text)

    print("✅ Visual TOC extraction complete.")
    if "--verbose" in sys.argv:
        print("🔍 TRACE: main() exited")

if __name__ == "__main__":
    main()
