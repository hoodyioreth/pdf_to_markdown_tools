#!/usr/bin/env python3
"""
Script: run_extraction_pipeline.py

Purpose: Sequentially run the 3 core PDF-to-Markdown extraction utilities:
- extract_text.py
- extract_outline.py
- parse_visual_toc.py

Assumes these scripts exist in the same directory and are the LKG (Last Known Good) versions.

Version: 1.0.0
"""

import subprocess
import os

scripts = [
    "extract_text.py",
    "extract_outline.py",
    "parse_visual_toc.py"
]

print("🔁 Starting PDF-to-Markdown extraction pipeline...
")

for script in scripts:
    print(f"▶️ Running {script}...
")
    result = subprocess.run(["python3", script])
    if result.returncode != 0:
        print(f"❌ Error running {script}, aborting pipeline.")
        exit(1)
    print(f"✅ Completed {script}.
")

print("🎉 All extraction steps completed successfully.")
