import sys
import fitz
from pathlib import Path

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.6.2"
SCRIPT_PURPOSE = "Extract raw text from a PDF file using PyMuPDF"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def extract_text(pdf_path: Path, verbose=False):
    output_path = OUTPUT_DIR / (pdf_path.stem + ".txt")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output: {output_path}")
    doc = fitz.open(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for page in doc:
            f.write(page.get_text())
    if verbose:
        print("✅ Text extraction complete.")

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if "--help" in sys.argv or "-h" in sys.argv:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--all]")
        return
    if "--version" in sys.argv:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        return
    if "--all" in sys.argv:
        for pdf_path in sorted(INPUT_DIR.glob("*.pdf")):
            extract_text(pdf_path, verbose)
        return

    print("📥 No file provided.")
    print("Select a PDF to process:")
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    choice = input("Enter number: ")
    try:
        selected = pdfs[int(choice) - 1]
        extract_text(selected, verbose)
    except:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()