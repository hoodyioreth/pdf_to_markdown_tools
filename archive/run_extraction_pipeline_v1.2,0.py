#!/usr/bin/env python3
"""
🔁 run_extraction_pipeline.py - v1.2.0

Purpose: Batch-run all core PDF-to-Markdown extraction steps:
- extract_text.py
- extract_outline.py
- parse_visual_toc.py

Features:
- Supports `--all` for batch mode
- Displays script versions and purposes
- Prints final stats summary
"""

import subprocess
import sys
import os

# Configuration
SCRIPT_NAME = "run_extraction_pipeline.py"
SCRIPT_VERSION = "1.2.0"

# List of subprocess scripts with descriptions
extraction_steps = [
    {
        "script": "extract_text.py",
        "description": "Extract raw text from the PDF pages into .txt"
    },
    {
        "script": "extract_outline.py",
        "description": "Extract internal PDF outline/bookmarks into .txt and .json"
    },
    {
        "script": "parse_visual_toc.py",
        "description": "Detect and extract TOC text blocks into .txt"
    }
]

# Helper to find version and purpose of each script
def get_script_info(script_name):
    try:
        with open(script_name, 'r') as f:
            lines = f.readlines()
            version = next((line.strip() for line in lines if "SCRIPT_VERSION" in line), "unknown")
            purpose = next((line.strip() for line in lines if "SCRIPT_PURPOSE" in line), "")
            return version, purpose
    except:
        return "?", "?"

def print_metadata():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print("📚 Core scripts used in this pipeline:")
    for step in extraction_steps:
        script = step["script"]
        version, purpose = get_script_info(script)
        print(f"  - {script} ({version}): {purpose or step['description']}")
    print("\n🚧 Steps this pipeline performs:")
    for step in extraction_steps:
        print(f"▶️ {step['script']}: {step['description']}")
    print("\n" + "-" * 60 + "\n")

def run_pipeline(args):
    total_scripts_run = 0
    for step in extraction_steps:
        script = step["script"]
        command = ["python3", script] + args
        print(f"▶️ Running {' '.join(command)}")
        result = subprocess.run(command)
        if result.returncode != 0:
            print(f"❌ Error running {script}, aborting pipeline.")
            exit(1)
        print(f"✅ Completed {script}.\n")
        total_scripts_run += 1

    print("-" * 60)
    print("📊 Pipeline complete.")
    print(f"📄 Scripts executed: {total_scripts_run}")
    print(f"🗂 Arguments used: {' '.join(args) if args else '[interactive]'}")
    print("🎉 All extraction steps completed successfully.\n")

if __name__ == "__main__":
    print_metadata()
    run_pipeline(sys.argv[1:])
