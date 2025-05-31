import sys
import fitz
from pathlib import Path

SCRIPT_NAME = "extract_text.py"
SCRIPT_VERSION = "1.6.1"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def select_pdf():
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found.")
        sys.exit(1)
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, file in enumerate(pdf_files, 1):
        print(f"[{i}] {file.name}")
    try:
        return pdf_files[int(input("Enter number: ")) - 1]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        sys.exit(1)

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if "--help" in sys.argv or "-h" in sys.argv:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h] [filename]")
        sys.exit(0)
    if "--version" in sys.argv:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        sys.exit(0)

    try:
        filename = next(arg for arg in sys.argv[1:] if not arg.startswith("-"))
        input_pdf = INPUT_DIR / filename
    except StopIteration:
        input_pdf = select_pdf()

    if not input_pdf.exists():
        print(f"❌ Error: no such file: '{input_pdf.name}'")
        print("⚠️ No text extracted.")
        return

    output_txt = OUTPUT_DIR / (input_pdf.stem + ".txt")

    if verbose:
        print(f"📂 Input: {input_pdf}")
        print(f"📝 Output: {output_txt}")

    doc = fitz.open(str(input_pdf))
    with open(output_txt, "w", encoding="utf-8") as out:
        for page in doc:
            out.write(page.get_text())
    print("✅ Text extraction complete.")

if __name__ == "__main__":
    main()