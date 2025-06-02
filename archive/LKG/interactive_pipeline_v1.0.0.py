# ✅ Script name: interactive_pipeline.py
# ✅ Version: v1.0.0
# ✅ Purpose: Guide user interactively through converting a single PDF to Markdown
# ✅ Dependencies: extract_text.py, detect_headings.py, convert_to_md.py

import os
import sys
import subprocess
import argparse
from pathlib import Path

SCRIPT_VERSION = "v1.0.0"

# Set base directory relative to this script's location
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR.parent / "data" / "input_pdfs"
TEXT_DIR = BASE_DIR.parent / "data" / "extracted_text"
MD_DIR = BASE_DIR.parent / "data" / "converted_md"

def list_pdfs():
    print("📄 Scanning for input PDFs...\n")
    pdfs = sorted([f.name for f in INPUT_DIR.glob("*.pdf")])
    if not pdfs:
        print("❌ No PDF files found in input folder.")
        sys.exit(1)
    for i, pdf in enumerate(pdfs):
        print(f"[{i}] {pdf}")
    print()
    return pdfs

def get_user_choice(pdfs):
    try:
        choice = int(input("Select a PDF by number: "))
        assert 0 <= choice < len(pdfs)
        return pdfs[choice]
    except (ValueError, AssertionError):
        print("❌ Invalid selection. Exiting.")
        sys.exit(1)

def ask_continue(prompt):
    response = input(f"{prompt} [Y/n]: ").strip().lower()
    return response in ["", "y", "yes"]

def run_step(step_num, step_total, label, command, progress_enabled):
    if progress_enabled:
        blocks = ["🟩" if i < step_num else "⬜" for i in range(step_total)]
        print(f"\n➡️  [{'✅' * (step_num - 1)}{''.join(blocks)}] {label}...\n")
    else:
        print(f"\n➡️  {label}...\n")

    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {label} failed. Exiting.\n")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Interactive PDF to Markdown pipeline")
    parser.add_argument("--no-progress", action="store_true", help="Disable emoji progress tracker")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s - {SCRIPT_VERSION}")
    args = parser.parse_args()

    print(f"\n📘 interactive_pipeline.py - {SCRIPT_VERSION}")
    print("🧠 Purpose: Convert a single PDF into clean Markdown via interactive steps.\n")

    pdfs = list_pdfs()
    filename = get_user_choice(pdfs)
    base = Path(filename).stem

    # Step 1: Extract Text
    if ask_continue("Step 1: Extract text from PDF?"):
        run_step(1, 3, "Extracting text", f"python3 extract_text.py \"{filename}\"", not args.no_progress)
    else:
        print("\n❌ Conversion canceled by user.\n")
        sys.exit(0)

    # Step 2: Detect Headings
    if ask_continue("Step 2: Detect headings from extracted text?"):
        run_step(2, 3, "Detecting headings", f"python3 detect_headings.py \"{filename}\"", not args.no_progress)
    else:
        print("\n❌ Conversion canceled by user.\n")
        sys.exit(0)

    # Step 3: Convert to Markdown
    if ask_continue("Step 3: Convert to Markdown?"):
        run_step(3, 3, "Converting to markdown", f"python3 convert_to_md.py \"{filename}\"", not args.no_progress)
    else:
        print("\n❌ Conversion canceled by user.\n")
        sys.exit(0)

    print("\n📦 All steps completed successfully!")
    print("\n🧾 Summary of output files:")
    print(f"   📄 Extracted text: {TEXT_DIR / (base + '.txt')}")
    print(f"   🧠 Headings JSON : {TEXT_DIR / (base + '.headings.json')}")
    print(f"   📘 Markdown file : {MD_DIR / (base + '.md')}\n")

if __name__ == "__main__":
    main()
