import sys
import fitz
import json
from pathlib import Path

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "1.6.4"
SCRIPT_PURPOSE = "Extract the internal PDF outline (bookmarks) if available"

INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"

def extract_outline(pdf_path: Path, verbose=False):
    doc = fitz.open(pdf_path)
    outline = doc.get_toc(simple=True)
    txt_path = OUTPUT_DIR / (pdf_path.stem + ".outline.txt")
    json_path = OUTPUT_DIR / (pdf_path.stem + ".outline.json")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output TXT: {txt_path}")
        print(f"📝 Output JSON: {json_path}")
    with open(txt_path, "w", encoding="utf-8") as txt_out:
        for entry in outline:
            txt_out.write(f"{'  ' * (entry[0] - 1)}- {entry[1]} (p. {entry[2]})
")
    with open(json_path, "w", encoding="utf-8") as json_out:
        json.dump(outline, json_out, indent=2)
    if verbose:
        print("✅ Outline extraction complete.")

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
            extract_outline(pdf_path, verbose)
        return

    print("📥 No file provided.")
    print("Select a PDF to process:")
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    choice = input("Enter number: ")
    try:
        selected = pdfs[int(choice) - 1]
        extract_outline(selected, verbose)
    except:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()