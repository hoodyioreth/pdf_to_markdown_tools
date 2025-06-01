#!/usr/bin/env python3
"""
Script: list_python_modules.py
Version: 1.0.0
Purpose: List all Python modules in the project with their purpose and suggested run order
"""

import re
from pathlib import Path

# Known descriptions for fallback use
fallback_descriptions = {
    "extract_text.py": "Extract raw text from PDF using PyMuPDF",
    "extract_outline.py": "Extract internal PDF outline (bookmarks)",
    "parse_visual_toc.py": "Extract visual TOC from first pages of PDF",
    "detect_headings.py": "Detect heading structure using font/position",
    "convert_to_md.py": "Convert extracted data into structured Markdown",
    "clean_headings_json.py": "Sanitize malformed headings in JSON files",
    "run_extraction_pipeline.py": "Batch run extraction scripts",
    "diagnose_structure_sources.py": "List fallback logic used per PDF",
}

# Suggested run order for core scripts
suggested_order = [
    "extract_text.py",
    "extract_outline.py",
    "parse_visual_toc.py",
    "detect_headings.py",
    "clean_headings_json.py",
    "diagnose_structure_sources.py",
    "convert_to_md.py",
]

def scan_scripts(directory: Path):
    results = []
    for path in sorted(directory.glob("*.py")):
        name = path.name
        try:
            text = path.read_text(errors="ignore")
            match = re.search(r'"""(.*?)"""', text, re.DOTALL)
            purpose = match.group(1).strip().split("\n")[0] if match else fallback_descriptions.get(name, "No description found")
        except Exception:
            purpose = "Unreadable or missing"

        results.append({
            "Filename": name,
            "Purpose": purpose,
            "Run Order": suggested_order.index(name) + 1 if name in suggested_order else "-"
        })
    return results

def main():
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir.parent / "src"
    print(f"🛠 list_python_modules.py - v1.0.0")
    print(f"📘 Purpose: List Python modules with purpose and order")
    print(f"📂 Scanning: {src_dir.resolve()}\n")

    modules = scan_scripts(src_dir)
    if not modules:
        print("❌ No .py files found.")
        return

    print(f"{'Filename':<50} | {'Run Order':<10} | Purpose")
    print("-" * 100)
    for m in modules:
        print(f"{m['Filename']:<50} | {m['Run Order']:<10} | {m['Purpose']}")

if __name__ == "__main__":
    main()
