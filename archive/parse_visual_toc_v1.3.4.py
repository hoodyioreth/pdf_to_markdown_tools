# Script: parse_visual_toc.py
# Version: 1.3.3
# Purpose: Extract a visual TOC from the first few pages

import sys
import fitz
from pathlib import Path
from rich.progress import track

SCRIPT_NAME = "parse_visual_toc.py"
SCRIPT_VERSION = "1.3.3"
SCRIPT_PURPOSE = "Extract a visual TOC from the first few pages"

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

def extract_visual_toc(pdf_path, verbose=False, max_pages=5):
    output_txt = OUTPUT_DIR / (pdf_path.stem + ".visual_toc.txt")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output: {output_txt}")
        print("🔊 Verbose mode enabled.")

    doc = fitz.open(pdf_path)
    lines = []
    for i in track(range(min(max_pages, len(doc))), description="📄 Extracting pages"):
        page = doc[i]
        text = page.get_text()
        page_lines = text.splitlines()
        for line in page_lines:
            if any(char.isdigit() for char in line[-5:]) and len(line.strip()) > 8:
                lines.append(line.strip())
        if verbose:
            print(f"🔍 Scanned page {i + 1}, found {len(lines)} TOC lines so far.")

    output_txt.write_text("No visual TOC found.")  # fixed

".join(lines) if lines else "No visual TOC found.")
    print("✅ Visual TOC extraction complete.")

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
    extract_visual_toc(pdf_path, verbose)