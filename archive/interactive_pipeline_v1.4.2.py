#!/usr/bin/env python3
"""
interactive_pipeline.py - v1.4.1
Purpose: Step-by-step interactive PDF → Markdown pipeline with optional progress display.
"""

import os
import sys
import argparse
import subprocess
import shlex
from pathlib import Path

# === Configuration ===
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PDF_INPUT = DATA_DIR / "input_pdfs"
TEXT_OUTPUT = DATA_DIR / "extracted_text"
MD_OUTPUT = DATA_DIR / "converted_md"
SCRIPTS = {
    "extract": "extract_text.py",
    "headings": "detect_headings.py",
    "convert": "convert_to_md.py",
}

# === Functions ===
def list_pdfs():
    return sorted([f for f in PDF_INPUT.glob("*.pdf")])

def display_pdfs(pdfs):
    print("\n📄 Available PDFs:")
    for i, pdf in enumerate(pdfs):
        print(f"[{i}] {pdf.name}")

def run_step(script, filename, step_label, step_number, show_progress=False):
    stem = filename.stem
    emoji_states = ["⬜", "⬜", "⬜"]
    for i in range(step_number):
        emoji_states[i] = "✅"
    emoji_states[step_number] = "🟩"
    if show_progress:
        print(f"➡️  [{' '.join(emoji_states)}] {step_label}")

    print(f"\n🔹 Step {step_number + 1}: {step_label}")
    cmd = ["python3", SCRIPTS[script], filename.name]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Completed: {step_label}. Proceed to next step? [Y/n]: ", end="")
        resp = input().strip().lower()
        if resp == 'n':
            print("🛑 Aborted.")
            sys.exit(0)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error during step: {' '.join(cmd)}")
        sys.exit(1)

def summarize_output(pdf_name):
    stem = Path(pdf_name).stem
    print("\n📦 Pipeline Complete!")
    print(f"📄 Source PDF:      {pdf_name}")
    print(f"📝 Text Extracted:  {stem}.txt")
    print(f"🧠 Headings Saved:  {stem}.headings.json")
    print(f"📘 Markdown Output: {stem}.md")

# === Main ===
def main():
    parser = argparse.ArgumentParser(description="Interactive PDF → Markdown Pipeline")
    parser.add_argument("--progress", action="store_true", help="Show progress bar")
    parser.add_argument('--no-progress', action='store_true', help='Disable emoji progress display')
    args = parser.parse_args()
    use_progress = not args.no_progress

    pdfs = list_pdfs()
    if not pdfs:
        print("❌ No PDF files found.")
        return

    display_pdfs(pdfs)
    selection = input("\nEnter the number of the PDF to process: ").strip()
    if not selection.isdigit() or int(selection) >= len(pdfs):
        print("❌ Invalid selection.")
        return

    pdf_file = pdfs[int(selection)]
    print(f"\n👉 Selected: {pdf_file.name}")

    run_step("extract", pdf_file, "Extracting raw text from PDF", 0, args.progress)
    run_step("headings", pdf_file, "Detecting headings using font size heuristics", 1, args.progress)
    run_step("convert", pdf_file, "Converting extracted text into structured Markdown", 2, args.progress)

    summarize_output(pdf_file.name)

if __name__ == "__main__":
    main()
