# parse_visual_toc_v1.3.6.py
import sys
import fitz
from pathlib import Path

SCRIPT_NAME = "parse_visual_toc.py"
SCRIPT_VERSION = "1.3.6"
SCRIPT_PURPOSE = "Attempt to extract a visual Table of Contents from the first few pages"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def extract_visual_toc(pdf_path: Path, verbose=False):
    output_path = OUTPUT_DIR / (pdf_path.stem + ".visual_toc.txt")
    print(f"📂 Processing {pdf_path.name}")
    doc = fitz.open(pdf_path)
    lines = []
    for i in range(min(5, len(doc))):
        page = doc[i]
        text = page.get_text().strip().splitlines()
        for line in text:
            if any(char.isdigit() for char in line) and "." in line:
                lines.append(line)
    if not lines:
        output_path.write_text("No visual TOC detected.\n")
    else:
        output_path.write_text("\n".join(lines))
    if verbose:
        print(f"📝 Output: {output_path}")
    print("✅ Visual TOC extraction complete.")

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if "--help" in sys.argv or "-h" in sys.argv:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--all]")
        return
    if "--version" in sys.argv:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return

    if "--all" in sys.argv:
        pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
        for pdf_path in pdf_files:
            extract_visual_toc(pdf_path, verbose)
        return

    print("📥 No file provided.\n")
    print("Select a PDF to process:")
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    choice = input("Enter number: ")
    try:
        selected = pdfs[int(choice) - 1]
        extract_visual_toc(selected, verbose)
    except Exception:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()