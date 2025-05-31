
#!/usr/bin/env python3
"""
Script: run_extraction_pipeline.py
Version: 0.1.0
Purpose: Sequentially runs all PDF extraction tools on a selected input file
Dependencies: 
  - extract_text_v1.5.3.py
  - extract_outline_v1.6.1.py
  - parse_visual_toc_v1.3.2.py
"""

import subprocess
import sys
import os
from pathlib import Path

SCRIPT_NAME = "run_extraction_pipeline.py"
SCRIPT_VERSION = "0.1.0"
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv

DATA_DIR = Path(__file__).resolve().parent / "../data"
INPUT_DIR = DATA_DIR / "input_pdfs"

def list_pdfs(input_dir):
    pdfs = sorted([f for f in input_dir.glob("*.pdf")])
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}] {pdf.name}")
    return pdfs

def select_pdf():
    print("📥 No file provided.")
    print("Select a PDF to process:")
    pdfs = list_pdfs(INPUT_DIR)
    choice = int(input("Enter number: ")) - 1
    return pdfs[choice]

def run_step(script, input_path):
    cmd = ["python3", script, str(input_path)]
    if VERBOSE:
        cmd.append("--verbose")
    print(f"▶️ Running: {' '.join(cmd)}")
    subprocess.run(cmd)

def main():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    if "--help" in sys.argv or "-h" in sys.argv:
        print(f"Usage: {SCRIPT_NAME} [--verbose|-v]")
        sys.exit(0)

    if "--version" in sys.argv:
        print(f"{SCRIPT_NAME} - v{SCRIPT_VERSION}")
        sys.exit(0)

    input_pdf = select_pdf()

    run_step("extract_text_v1.5.3.py", input_pdf)
    run_step("extract_outline_v1.6.1.py", input_pdf)
    run_step("parse_visual_toc_v1.3.2.py", input_pdf)

    print("✅ Extraction pipeline complete.")

if __name__ == "__main__":
    main()
