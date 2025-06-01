#!/usr/bin/env python3
"""
Script: list_python_modules.py
Version: 1.1.0
Purpose: List Python modules in the project with base name, LKG version, CLI parameters, and run order
"""

import re
from pathlib import Path

# Known fallback descriptions
fallback_descriptions = {
    "extract_text": "Extract raw text from PDF using PyMuPDF",
    "extract_outline": "Extract internal PDF outline (bookmarks)",
    "parse_visual_toc": "Extract visual TOC from first pages of PDF",
    "detect_headings": "Detect heading structure using font/position",
    "convert_to_md": "Convert extracted data into structured Markdown",
    "clean_headings_json": "Sanitize malformed headings in JSON files",
    "run_extraction_pipeline": "Batch run extraction scripts",
    "diagnose_structure_sources": "List fallback logic used per PDF",
    "list_python_modules": "List Python modules with metadata",
}

suggested_order = [
    "extract_text",
    "extract_outline",
    "parse_visual_toc",
    "detect_headings",
    "clean_headings_json",
    "diagnose_structure_sources",
    "convert_to_md",
]

def extract_info(path: Path):
    name = path.name
    base = re.sub(r'_v[\d.]+(?=\.py)', '', name)
    version_match = re.search(r'_v(\d+(?:\.\d+)+)', name)
    version = version_match.group(1) if version_match else "unknown"
    text = path.read_text(errors="ignore")
    docstring = re.search(r'"""(.*?)"""', text, re.DOTALL)
    purpose = docstring.group(1).strip().split("\n")[0] if docstring else fallback_descriptions.get(base, "No description found")
    cli_flags = sorted(set(re.findall(r"--(\w+)", text)) - {"help", "version", "v"})

    return {
        "Module": base,
        "LKG Version": version,
        "Purpose": purpose,
        "CLI Flags": ", ".join(f"--{flag}" for flag in cli_flags) if cli_flags else "-",
        "Run Order": suggested_order.index(base) + 1 if base in suggested_order else "-"
    }

def main():
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir.parent / "src"
    print(f"🛠 list_python_modules.py - v1.1.0")
    print(f"📘 Purpose: List Python modules with base name, LKG version, CLI flags, and run order")
    print(f"📂 Scanning: {src_dir.resolve()}\n")

    results = []
    for path in sorted(src_dir.glob("*.py")):
        info = extract_info(path)
        results.append(info)

    if not results:
        print("❌ No .py files found.")
        return

    print(f"{'Module':<30} | {'LKG Version':<12} | {'Run Order':<10} | {'CLI Flags':<30} | Purpose")
    print("-" * 120)
    for r in results:
        print(f"{r['Module']:<30} | {r['LKG Version']:<12} | {r['Run Order']:<10} | {r['CLI Flags']:<30} | {r['Purpose']}")

if __name__ == "__main__":
    main()
