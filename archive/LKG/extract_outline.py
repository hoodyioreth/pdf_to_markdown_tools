
import sys
import os
import fitz  # PyMuPDF
import json
from pathlib import Path

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "v1.6.6"
SCRIPT_PURPOSE = "Extract the internal PDF outline (bookmarks) if available"

INPUT_DIR = Path(__file__).parent / "../data/input_pdfs"
OUTPUT_DIR = Path(__file__).parent / "../data/extracted_text"

def display_menu(pdf_files):
    print("\nSelect a PDF to process:")
    for i, file in enumerate(pdf_files, start=1):
        print(f"[{i}] {file.name}")
    choice = input("Enter number: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(pdf_files):
            return pdf_files[index]
    except ValueError:
        pass
    print("❌ Invalid selection.")
    sys.exit(1)

def extract_outline(pdf_path, verbose=False):
    doc = fitz.open(pdf_path)
    outline = doc.get_toc(simple=True)
    name = pdf_path.stem
    txt_path = OUTPUT_DIR / f"{name}.outline.txt"
    json_path = OUTPUT_DIR / f"{name}.outline.json"

    if outline:
        with open(txt_path, "w", encoding="utf-8") as txt_out:
            for entry in outline:
                indent = "  " * (entry[0] - 1)
                txt_out.write(f"{indent}- {entry[1]} (p. {entry[2]})\n")
        with open(json_path, "w", encoding="utf-8") as json_out:
            json.dump(outline, json_out, indent=2)
        if verbose:
            print(f"💾 Saved outline TXT to: {txt_path}")
            print(f"💾 Saved outline JSON to: {json_path}")
    else:
        with open(txt_path, "w", encoding="utf-8") as txt_out:
            txt_out.write("⚠️ No outline extracted.\n")
        with open(json_path, "w", encoding="utf-8") as json_out:
            json.dump([], json_out)
        if verbose:
            print("⚠️ No outline extracted.")

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    show_version = "--version" in sys.argv
    show_help = "--help" in sys.argv or "-h" in sys.argv
    run_all = "--all" in sys.argv

    if show_version:
        print(f"{SCRIPT_NAME} - {SCRIPT_VERSION}")
        sys.exit(0)
    if show_help:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|--help|-h|--all]")
        sys.exit(0)

    print(f"🛠 {SCRIPT_NAME} - {SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if run_all:
        for file in pdf_files:
            print(f"📂 Processing {file.name}")
            extract_outline(file, verbose)
            print("✅ Outline extraction complete.")
        return

    print("\n📥 No file provided.")
    selected_pdf = display_menu(pdf_files)
    print(f"📂 Input: {selected_pdf.resolve()}")

    extract_outline(selected_pdf, verbose)
    print("✅ Outline extraction complete.")

if __name__ == "__main__":
    main()
