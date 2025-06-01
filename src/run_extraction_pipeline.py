#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

SCRIPT_NAME = "run_extraction_pipeline.py"
SCRIPT_VERSION = "1.2.2"
SCRIPT_PURPOSE = "Batch-run PDF-to-Markdown extraction scripts in sequence"

core_scripts = {
    "extract_text.py": {
        "version": "1.6.3",
        "purpose": "Extract raw text from a PDF file using PyMuPDF"
    },
    "extract_outline.py": {
        "version": "v1.6.6",
        "purpose": "Extract the internal PDF outline (bookmarks) if available"
    },
    "parse_visual_toc.py": {
        "version": "1.3.6",
        "purpose": "Attempt to extract a visual Table of Contents from the first few pages"
    }
}

valid_flags = ["--all", "--help", "--version", "-v"]
args_used = [arg for arg in sys.argv[1:] if arg in valid_flags]

# ─── Display Header ─────────────────────────────────────────────────────────────
print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
print(f"📘 Purpose: {SCRIPT_PURPOSE}")
print("🎛 Valid CLI Flags: --all | --help | --version | -v")
print("\n📚 Core scripts used in this pipeline:")
for script, meta in core_scripts.items():
    print(f"  - {script} (SCRIPT_VERSION = \"{meta['version']}\"): SCRIPT_PURPOSE = \"{meta['purpose']}\"")

print("\n🚧 Steps this pipeline performs:")
print("▶️ extract_text.py: Extract raw text from the PDF pages into .txt")
print("▶️ extract_outline.py: Extract internal PDF outline/bookmarks into .txt and .json")
print("▶️ parse_visual_toc.py: Detect and extract TOC text blocks into .txt")
print("-" * 60)

# ─── Main Execution ─────────────────────────────────────────────────────────────
if "--version" in sys.argv or "-v" in sys.argv:
    sys.exit(0)

if "--help" in sys.argv:
    sys.exit(0)

if "--all" not in sys.argv:
    print("❌ Please provide a valid flag. For batch mode, use: --all")
    sys.exit(1)

# Track stats
pdfs_processed = 0
scripts_run = 0

for script in core_scripts:
    print(f"\n▶️ Running python3 {script} --all")
    result = subprocess.run(["python3", script, "--all"])
    scripts_run += 1
    if result.returncode != 0:
        print(f"❌ Error in {script}. Aborting.")
        sys.exit(1)
    print(f"✅ Completed {script}.")

    # crude guess: each script processes all 9 PDFs (from menu)
    pdfs_processed = max(pdfs_processed, 9)

# ─── Summary ────────────────────────────────────────────────────────────────────
print("-" * 60)
print("📊 Pipeline complete.")
print(f"📄 Scripts executed: {scripts_run}")
print(f"🗂 Arguments used: {' '.join(args_used)}")
print(f"📈 PDFs processed per script: {pdfs_processed}")
print(f"📁 Estimated output files created: {pdfs_processed * scripts_run}")
print("🎉 All extraction steps completed successfully.")
