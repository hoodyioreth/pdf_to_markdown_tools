"""
Script: run_testbench.py
Version: 1.0.0
Purpose: Run a full pipeline test on key structure variants in input_pdfs/
"""

import subprocess
from pathlib import Path

# Define test files by structure type
test_files = [
    "5e_2024_House_Rules_draft_v_0.2.pdf",  # headings
    "Classic_Guide_to_Greyhawk.pdf",        # outline
    "Greyhawk_Expanded_-_A_Players_Guide_to_Oerik.pdf",  # visual
    "VER1-03_Gift_of_Beauty_(3E).pdf",      # mixed
]

def run_script(script_name, args):
    print(f"🛠 Running {script_name} {' '.join(args)}")
    result = subprocess.run(["python3", script_name] + args)
    if result.returncode != 0:
        print(f"❌ {script_name} failed with code {result.returncode}")
    else:
        print(f"✅ {script_name} completed.")

def main():
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "../data/input_pdfs"
    testpaths = [input_dir / f for f in test_files]

    for pdf in testpaths:
        print(f"📄 Testing: {pdf.name}")
        run_script("extract_text.py", [str(pdf)])
        run_script("detect_headings.py", [str(pdf)])
        run_script("extract_outline.py", [str(pdf)])
        run_script("parse_visual_toc.py", [str(pdf)])
        run_script("convert_to_md.py", [str(pdf)])
        print("—" * 60)

    # Clean one file after conversion
    md_path = base_dir / "../data/converted_md/5e_2024_House_Rules_draft_v_0.2.md"
    if md_path.exists():
        run_script("clean_md_output.py", [md_path.name])
    else:
        print("⚠️ Markdown file not found for cleaning.")

if __name__ == "__main__":
    print("🚀 Running test bench on core PDFs...")
    main()
