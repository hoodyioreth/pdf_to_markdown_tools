# Script: extract_outline.py
# Version: 1.6.2
# Purpose: Extract PDF bookmarks (outline) if available

import sys
import fitz
import json
from pathlib import Path

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "1.6.2"
SCRIPT_PURPOSE = "Extract PDF bookmarks (outline) if available"

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

def extract_outline(pdf_path, verbose=False):
    output_txt = OUTPUT_DIR / (pdf_path.stem + ".outline.txt")
    output_json = OUTPUT_DIR / (pdf_path.stem + ".outline.json")
    if verbose:
        print(f"📂 Input: {pdf_path}")
        print(f"📝 Output TXT: {output_txt}")
        print(f"📝 Output JSON: {output_json}")
        print("🔊 Verbose mode enabled.")

    doc = fitz.open(pdf_path)
    outline = doc.get_toc()
    if not outline:
        if verbose:
            print("⚠️ No outline extracted.")
        output_txt.write_text("No outline found.")
        output_json.write_text(json.dumps([], indent=2))
        return

    with open(output_txt, "w", encoding="utf-8") as txt_out:
        for entry in outline:
            txt_out.write(f"{'  ' * (entry[0] - 1)}- {entry[1]} (p. {entry[2]})
")
    with open(output_json, "w", encoding="utf-8") as json_out:
        json.dump(outline, json_out, indent=2)

    print("✅ Outline extraction complete.")

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
    extract_outline(pdf_path, verbose)