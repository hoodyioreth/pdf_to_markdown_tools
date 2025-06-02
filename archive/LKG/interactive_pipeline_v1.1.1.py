#!/usr/bin/env python3
""" 
interactive_pipeline.py - v1.1.1

Fix: Pass only filename (not full path) to extract_text.py to avoid duplicate path nesting

Dependencies:
- extract_text.py v1.6.4+
- detect_headings.py v1.0.2+
- convert_to_md.py v2.0.8+
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_NAME = "interactive_pipeline.py"
VERSION = "v1.1.1"

def run_subprocess(command):
    print(f"🔹 Running: {' '.join(command)}")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"❌ Error during step: {' '.join(command)}")
        sys.exit(1)

def prompt_continue(step_desc):
    proceed = input(f"✅ Completed: {step_desc}. Proceed to next step? [Y/n]: ").strip().lower()
    if proceed not in ['', 'y', 'yes']:
        print("🚪 Exiting.")
        sys.exit(0)

def main():
    print(f"🛠 {SCRIPT_NAME} - {VERSION}")
    print("📘 Purpose: Step-by-step interactive PDF → Markdown pipeline")

    input_dir = Path("../data/input_pdfs/")
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in ../data/input_pdfs/")
        return

    print("\n📄 Available PDFs:")
    for i, pdf in enumerate(pdf_files):
        print(f"[{i}] {pdf.name}")

    choice = input("\nEnter the number of the PDF to process: ").strip()
    try:
        pdf_path = pdf_files[int(choice)]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return

    print(f"👉 Selected: {pdf_path.name}")

    # Step 1: extract_text
    run_subprocess(["python3", "extract_text.py", pdf_path.name])
    prompt_continue("Text extraction")

    # Step 2: detect_headings
    run_subprocess(["python3", "detect_headings.py", pdf_path.name])
    prompt_continue("Heading detection")

    # Step 3: convert_to_md
    run_subprocess(["python3", "convert_to_md.py", pdf_path.name])
    prompt_continue("Markdown conversion")

    print("\n✅ Pipeline completed successfully for", pdf_path.name)

if __name__ == "__main__":
    main()
