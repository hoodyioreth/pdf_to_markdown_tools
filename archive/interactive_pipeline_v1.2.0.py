#!/usr/bin/env python3
"""
🛠 interactive_pipeline.py - v1.2.0
📘 Purpose: Step-by-step interactive PDF → Markdown pipeline with enhanced user feedback
"""

import os
import sys
import subprocess
import argparse

PIPELINE_STEPS = [
    ("Extract Text", "extract_text.py"),
    ("Detect Headings", "detect_headings.py"),
    ("Convert to Markdown", "convert_to_md.py"),
]

def list_pdfs(input_dir):
    return [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

def run_step(step_number, label, script, filename, show_progress):
    print(f"🟩 Step {step_number} of 3: {label}...")
    print(f"▶️ Command: python3 {script} {filename}")
    print("--------------------------------------------------")
    result = subprocess.run(["python3", script, filename])
    if result.returncode != 0:
        print(f"❌ Error during step: python3 {script} {filename}")
        sys.exit(1)
    print(f"✅ Step {step_number} Complete.
")
    if show_progress:
        print_progress(step_number)

def print_progress(current_step):
    print("🧭 Progress:")
    for i, (label, _) in enumerate(PIPELINE_STEPS, 1):
        status = "✔" if i <= current_step else " "
        print(f"   [{'✔' if i <= current_step else ' '}] {label}")
    print("--------------------------------------------------")

def main():
    parser = argparse.ArgumentParser(description="Run the interactive PDF → Markdown pipeline.")
    parser.add_argument("--progress", action="store_true", help="Show flowchart-style progress during steps")
    args = parser.parse_args()

    input_dir = "../data/input_pdfs"
    text_dir = "../data/extracted_text"
    output_dir = "../data/converted_md"
    os.makedirs(output_dir, exist_ok=True)

    print("🛠 interactive_pipeline.py - v1.2.0")
    print("📘 Purpose: Step-by-step interactive PDF → Markdown pipeline
")
    print("📚 Pipeline Overview:")
    for i, (label, script) in enumerate(PIPELINE_STEPS, 1):
        print(f"  [{i}] {label:<22} → {script}")
    print("
--------------------------------------------------")

    pdfs = list_pdfs(input_dir)
    if not pdfs:
        print("❌ No PDF files found in input directory.")
        return

    print("📄 Available PDFs:")
    for i, pdf in enumerate(pdfs):
        print(f"[{i}] {pdf}")
    try:
        selected_index = int(input("
Enter the number of the PDF to process: "))
        filename = pdfs[selected_index]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return

    base = filename[:-4] if filename.endswith(".pdf") else filename
    print(f"
👉 Selected: {filename}")
    print("--------------------------------------------------")

    for i, (label, script) in enumerate(PIPELINE_STEPS, 1):
        run_step(i, label, script, filename, args.progress)
        if i < len(PIPELINE_STEPS):
            cont = input(f"✅ Completed: {label}. Proceed to next step? [Y/n]: ").strip().lower()
            if cont not in ("", "y", "yes"):
                print("🛑 Pipeline halted by user.")
                return

    # Summary
    print("🎉 Pipeline Complete:", filename)
    print("
📤 Outputs Generated:")
    print(f"  - ✅ {text_dir}/{base}.txt")
    print(f"  - ✅ {text_dir}/{base}.headings.json")
    print(f"  - ✅ {output_dir}/{base}.md")
    print("
📘 Conversion used: headings or fallback structure")
    print("🕒 Done.
--------------------------------------------------")

if __name__ == "__main__":
    main()
