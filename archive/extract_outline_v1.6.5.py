
import fitz
import sys
import os
import json
from pathlib import Path
from rich.progress import track

SCRIPT_NAME = "extract_outline.py"
SCRIPT_VERSION = "v1.6.5"
SCRIPT_PURPOSE = "Extract the internal PDF outline (bookmarks) if available"

INPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "input_pdfs"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "extracted_text"

def extract_outline(pdf_path, verbose=False):
    doc = fitz.open(pdf_path)
    outline = doc.get_toc(simple=True)

    base_name = pdf_path.stem
    txt_path = OUTPUT_DIR / f"{base_name}.outline.txt"
    json_path = OUTPUT_DIR / f"{base_name}.outline.json"

    if outline:
        if verbose:
            print(f"📚 Found {len(outline)} outline entries.")

        with open(txt_path, "w", encoding="utf-8") as txt_out:
            for entry in track(outline, description="📝 Writing outline TXT"):
                txt_out.write(f"{'  ' * (entry[0] - 1)}- {entry[1]} (p. {entry[2]})\n")

        with open(json_path, "w", encoding="utf-8") as json_out:
            json.dump(outline, json_out, indent=2, ensure_ascii=False)

        print(f"💾 Saved outline TXT to: {txt_path}")
        print(f"💾 Saved outline JSON to: {json_path}")
        print("✅ Outline extraction complete.")
    else:
        if verbose:
            print("⚠️ No outline extracted.")
        with open(txt_path, "w", encoding="utf-8") as txt_out:
            txt_out.write("No outline found.\n")
        with open(json_path, "w", encoding="utf-8") as json_out:
            json.dump([], json_out)

def display_menu(pdf_files):
    print("📥 No file provided.")
    print("Select a PDF to process:")
    for i, file in enumerate(pdf_files, 1):
        print(f"[{i}] {file.name}")
    selection = int(input("Enter number: ")) - 1
    return pdf_files[selection]

def main():
    print(f"🛠 {SCRIPT_NAME} - {SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")
    print(f"📥 Expected input:   {INPUT_DIR.resolve()}")
    print(f"📤 Expected output:  {OUTPUT_DIR.resolve()}")

    args = sys.argv[1:]
    verbose = "--verbose" in args or "-v" in args
    show_version = "--version" in args
    show_help = "--help" in args or "-h" in args
    run_all = "--all" in args

    if show_version:
        print(f"{SCRIPT_NAME} - {SCRIPT_VERSION}")
        return
    if show_help:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v|--version|-h|--all]")
        return

    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if run_all:
        for file in pdf_files:
            print(f"📂 Processing {file.name}")
            extract_outline(file, verbose=verbose)
        return

    if not args:
        selected_pdf = display_menu(pdf_files)
        print(f"📂 Input: {selected_pdf}")
        extract_outline(selected_pdf, verbose=verbose)
    else:
        file_arg = args[0]
        file_path = INPUT_DIR / file_arg
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        extract_outline(file_path, verbose=verbose)

if __name__ == "__main__":
    main()
