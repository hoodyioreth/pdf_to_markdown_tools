# 🛠 interactive_pipeline.py - v1.3.4
# 📘 Purpose: Step-by-step interactive PDF → Markdown pipeline with optional progress emoji row

import os
import sys
import subprocess

def list_pdfs(input_dir):
    return [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

def display_pdf_choices(pdfs):
    print("\n📄 Available PDFs:")
    for i, name in enumerate(pdfs):
        print(f"[{i}] {name}")

def show_progress(step, enable_progress):
    if not enable_progress:
        return
    states = ["⬜", "⬜", "⬜"]
    for i in range(step):
        states[i] = "✅"
    if step < 3:
        states[step] = "🟩"
    progress_bar = f"➡️  [{''.join(states)}]"
    print(progress_bar, end=" ")
    if step == 0:
        print("Extracting text...")
    elif step == 1:
        print("Detecting headings...")
    elif step == 2:
        print("Converting to markdown...")

def run_step(description, command, step_num, show_progress_flag):
    show_progress(step_num, show_progress_flag)
    print(f"\n🔹 {description}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Error during step: {command}")
        sys.exit(1)
    else:
        print(f"✅ Completed: {description}. Proceed to next step? [Y/n]: ", end="")
        if input().lower().strip() == "n":
            sys.exit(0)

def main():
    input_dir = "../data/input_pdfs"
    output_dir = "../data/converted_md"
    show_progress_flag = "--progress" in sys.argv

    pdfs = list_pdfs(input_dir)
    display_pdf_choices(pdfs)

    selected = input("\nEnter the number of the PDF to process: ").strip()
    try:
        selected_pdf = pdfs[int(selected)]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        sys.exit(1)

    print(f"\n👉 Selected: {selected_pdf}")
    pdf_basename = selected_pdf.replace(".pdf", "")

    run_step("Step 1: Extracting raw text from PDF", f"python3 extract_text.py {selected_pdf}", 0, show_progress_flag)
    run_step("Step 2: Detecting headings using font size heuristics", f"python3 detect_headings.py {selected_pdf}", 1, show_progress_flag)
    run_step("Step 3: Converting extracted text into structured Markdown", f"python3 convert_to_md.py {selected_pdf}", 2, show_progress_flag)

    if show_progress_flag:
        print("➡️  [✅✅✅] Complete!")

    print("\n📦 Pipeline Complete!")
    print(f"📄 Source PDF:      {selected_pdf}")
    print(f"📝 Text Extracted:  {pdf_basename}.txt")
    print(f"🧠 Headings Saved:  {pdf_basename}.headings.json")
    print(f"📘 Markdown Output: {pdf_basename}.md")

if __name__ == "__main__":
    main()
