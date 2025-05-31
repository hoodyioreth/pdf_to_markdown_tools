"""

Script: extract_outline.py

Purpose: Extract the internal PDF outline (bookmarks) if available

Version: 1.4.0

"""



import sys

import fitz  # PyMuPDF

import json

import sys

from pathlib import Path



SCRIPT_NAME = "extract_outline.py"

SCRIPT_VERSION = "1.4.5"

SCRIPT_PURPOSE = "Extract the internal PDF outline (bookmarks) if available"



INPUT_DIR = Path(__file__).resolve().parent / "../data/input_pdfs"

OUTPUT_DIR = Path(__file__).resolve().parent / "../data/extracted_text"



def print_banner():

    print(f"\n📥 Expected input:   {INPUT_DIR}")

    print(f"📤 Expected output:  {OUTPUT_DIR}\n")

    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")

    print(f"📘 Purpose: {SCRIPT_PURPOSE}")

    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")

    print("")



def extract_outline(pdf_path, verbose=False):

    try:

        doc = fitz.open(pdf_path)

        toc = doc.get_toc()

        if not toc:

            print("⚠️ No outline/bookmarks found in this PDF.")

            return []

        if verbose:

            print(f"📚 Found {len(toc)} outline entries.")

        return toc

    except Exception as e:

        print(f"❌ Error: {e}")

        return []



def save_outline_txt(output_path, outline, verbose=False):

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:

        for level, title, page in outline:

            indent = "  " * (level - 1)

            f.write(f"{indent}- {title} (Page {page})\n")

    if verbose:

        print(f"💾 Saved outline TXT to: {output_path}")



def save_outline_json(output_path, outline, verbose=False):

    structured = [{"level": lvl, "title": title, "page": page} for lvl, title, page in outline]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(structured, f, indent=2)

    if verbose:

        print(f"💾 Saved outline JSON to: {output_path}")





def select_pdf():

    pdf_files = sorted(INPUT_DIR.glob("*.pdf"))

    if "--verbose" in sys.argv:

        print("🔍 TRACE: select_pdf() called")

    if not pdf_files:

        print("❌ No PDF files found in input folder.")

        sys.exit(1)



    print("📥 No file provided.")

    print("Select a PDF to process:")

    for i, f in enumerate(pdf_files, start=1):

        print(f"[{i}] {f.name}")



    choice = input("Enter number: ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(pdf_files)):

        print("❌ Invalid selection.")

        sys.exit(1)



    return pdf_files[int(choice) - 1]



def main():

    print_banner()

    if "--verbose" in sys.argv:

        print("🔍 TRACE: main() entered")

    verbose = "--verbose" in sys.argv

    input_pdf = select_pdf() if len(sys.argv) < 2 or sys.argv[1].startswith("--") else Path(sys.argv[1])

    output_dir = Path(__file__).resolve().parent / "../data/extracted_text"

    txt_output = output_dir / (Path(input_pdf).stem + ".outline.txt")

    json_output = output_dir / (Path(input_pdf).stem + ".outline.json")

    print(f"📂 Input: {input_pdf}")

    print(f"📝 Output TXT: {txt_output}")

    print(f"📝 Output JSON: {json_output}")

    if verbose:

        print("🔊 Verbose mode enabled.")

    outline = extract_outline(input_pdf, verbose)

    if outline:

        save_outline_txt(txt_output, outline, verbose)

        save_outline_json(json_output, outline, verbose)

        print("✅ Outline extraction complete.")

    else:

        print("⚠️ No outline extracted.")

    input_pdf = select_pdf() if len(sys.argv) < 2 or sys.argv[1].startswith("--") else Path(sys.argv[1])

    verbose = "--verbose" in sys.argv



    output_dir = Path(__file__).resolve().parent / "../data/extracted_text"

    txt_output = output_dir / (Path(input_pdf).stem + ".outline.txt")

    json_output = output_dir / (Path(input_pdf).stem + ".outline.json")



    print(f"📂 Input: {input_pdf}")

    print(f"📝 Output TXT: {txt_output}")

    print(f"📝 Output JSON: {json_output}")

    if verbose:

        print("🔊 Verbose mode enabled.")



    outline = extract_outline(input_pdf, verbose)

    if outline:

        save_outline_txt(txt_output, outline, verbose)

        save_outline_json(json_output, outline, verbose)

        print("✅ Outline extraction complete.")

    else:

        print("⚠️ No outline extracted.")



if __name__ == "__main__":
    main()