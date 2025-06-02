#!/usr/bin/env python3
"""
interactive_pipeline.py - v1.4.0
Purpose: Step-by-step interactive PDF → Markdown pipeline with emoji progress bar
"""

import os
import subprocess
import argparse

INPUT_DIR = "../data/input_pdfs"
OUTPUT_DIR = "../data/converted_md"

STEPS = [
    ("Extracting raw text from PDF", "extract_text.py"),
    ("Detecting headings using font size heuristics", "detect_headings.py"),
    ("Converting extracted text into structured Markdown", "convert_to_md.py")
]

def list_pdfs():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    files.sort()
    return files

def print_progress(index, total):
    icons = ["✅" if i < index else "🟩" if i == index else "⬜" for i in range(total)]
    labels = ["Extracting", "Detecting", "Converting"]
    print(f"➡️  [{' '.join(icons)}] {labels[index] if index < total else 'Complete!'}")

def run_step(step_index, script, pdf_filename, progress_enabled):
    if progress_enabled:
        print_progress(step_index, len(STEPS))

    print(f"
🔹 Step {step_index + 1}: {STEPS[step_index][0]}")
    try:
        subprocess.run(["python3", script, pdf_filename], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error during step: python3 {script} {pdf_filename}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Interactive PDF to Markdown pipeline")
    parser.add_argument("--progress", action="store_true", help="Show emoji progress indicators")
    args = parser.parse_args()

    print("📄 Available PDFs:")
    pdf_files = list_pdfs()
    for i, fname in enumerate(pdf_files):
        print(f"[{i}] {fname}")

    try:
        choice = int(input("
Enter the number of the PDF to process: "))
        selected_pdf = pdf_files[choice]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return

    print(f"
👉 Selected: {selected_pdf}
")
    basename = os.path.splitext(selected_pdf)[0]

    for i, (_, script) in enumerate(STEPS):
        if not run_step(i, script, selected_pdf, args.progress):
            return
        response = input(f"✅ Completed: Step {i+1}: {STEPS[i][0]}. Proceed to next step? [Y/n]: ")
        if response.lower().strip() == 'n':
            print("🛑 Pipeline aborted by user.")
            return

    print("
📦 Pipeline Complete!")
    print(f"📄 Source PDF:      {selected_pdf}")
    print(f"📝 Text Extracted:  {basename}.txt")
    print(f"🧠 Headings Saved:  {basename}.headings.json")
    print(f"📘 Markdown Output: {basename}.md")

if __name__ == "__main__":
    main()
