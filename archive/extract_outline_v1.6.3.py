import sys
import fitz
import json
from pathlib import Path

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "1.6.3"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def select_pdf(verbose=False):
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
        input_pdf = select_pdf(verbose)

    output_txt = OUTPUT_DIR / (input_pdf.stem + ".outline.txt")
    output_json = OUTPUT_DIR / (input_pdf.stem + ".outline.json")

    doc = fitz.open(str(input_pdf))
    outline = doc.get_toc(simple=True)

    if not outline:
        output_txt.write_text("⚠️ No outline extracted.\n")
        print("⚠️ No outline extracted.")
        return

    with open(output_txt, "w", encoding="utf-8") as txt_out:
        for entry in outline:
            txt_out.write(f"{'  ' * (entry[0] - 1)}- {entry[1]} (p. {entry[2]})\n")

    with open(output_json, "w", encoding="utf-8") as json_out:
        json.dump(outline, json_out, indent=2)

    print(f"💾 Saved outline TXT to: {output_txt}")
    print(f"💾 Saved outline JSON to: {output_json}")
    print("✅ Outline extraction complete.")

if __name__ == "__main__":
    main()