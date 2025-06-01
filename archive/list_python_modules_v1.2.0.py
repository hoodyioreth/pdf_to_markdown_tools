#!/usr/bin/env python3
"""
Script: list_python_modules.py
Version: 1.2.0
Purpose: List project Python modules with LKG version from VERIFICATION.md (or fallback to header), CLI flags, and run order
"""

import re
from pathlib import Path

# Suggested run order for primary tools
suggested_order = [
    "extract_text",
    "extract_outline",
    "parse_visual_toc",
    "detect_headings",
    "clean_headings_json",
    "diagnose_structure_sources",
    "convert_to_md",
]

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

def parse_lkg_versions(verification_path):
    versions = {}
    pattern = re.compile(r"✅\s+(\w+)_v(\d+(?:\.\d+)+)\.py")
    try:
        text = verification_path.read_text(errors="ignore")
        for match in pattern.finditer(text):
            base, version = match.groups()
            versions[base] = version
    except Exception:
        pass
    return versions

def extract_info(path: Path, lkg_versions: dict):
    name = path.name
    base = name.replace(".py", "").split("_v")[0]
    text = path.read_text(errors="ignore")

    # LKG from verification file or fallback to script docstring version
    lkg = lkg_versions.get(base)
    if not lkg:
        header = re.search(r'(?i)version[:=]\s*["\']?v?(\d+(?:\.\d+)+)', text)
        lkg = header.group(1) if header else "unknown"

    # Purpose from docstring or fallback
    docstring = re.search(r'"""(.*?)"""', text, re.DOTALL)
    purpose = docstring.group(1).strip().split("\n")[0] if docstring else fallback_descriptions.get(base, "No description found")

    # Detect CLI flags (excluding help/version)
    cli_flags = sorted(set(re.findall(r"--(\w+)", text)) - {"help", "version", "v"})

    return {
        "Module": base,
        "LKG Version": lkg,
        "Purpose": purpose,
        "CLI Flags": ", ".join(f"--{flag}" for flag in cli_flags) if cli_flags else "-",
        "Run Order": suggested_order.index(base) + 1 if base in suggested_order else "-"
    }

def main():
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir.parent / "src"
    docs_dir = base_dir.parent / "docs"
    verification_path = docs_dir / "VERIFICATION.md"

    print(f"🛠 list_python_modules.py - v1.2.0")
    print(f"📘 Purpose: List Python modules with metadata, LKG verification, and CLI flags")
    print(f"📂 Scanning: {src_dir.resolve()}\n")

    lkg_versions = parse_lkg_versions(verification_path)
    results = []

    for path in sorted(src_dir.glob("*.py")):
        results.append(extract_info(path, lkg_versions))

    if not results:
        print("❌ No .py files found.")
        return

    print(f"{'Module':<30} | {'LKG Version':<12} | {'Run Order':<10} | {'CLI Flags':<30} | Purpose")
    print("-" * 120)
    for r in results:
        print(f"{r['Module']:<30} | {r['LKG Version']:<12} | {r['Run Order']:<10} | {r['CLI Flags']:<30} | {r['Purpose']}")

if __name__ == "__main__":
    main()
