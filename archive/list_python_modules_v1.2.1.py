#!/usr/bin/env python3
"""
Script: list_python_modules.py
Version: 1.2.1
Purpose: List project Python modules with LKG version from VERIFICATION.md (or fallback), CLI parameters, and version insights
"""

import re
from pathlib import Path
from packaging import version as v

# Run order
suggested_order = [
    "extract_text",
    "extract_outline",
    "parse_visual_toc",
    "detect_headings",
    "clean_headings_json",
    "diagnose_structure_sources",
    "convert_to_md",
]

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
    stem = path.stem
    if "_v" in stem and re.search(r'_v\d', stem):
        base = stem.split("_v")[0]
        version_str = stem.split("_v")[1]
    else:
        base = stem
        version_str = None

    text = path.read_text(errors="ignore")
    header = re.search(r'(?i)version[:=]\s*["\']?v?(\d+(?:\.\d+)+)', text)
    fallback_version = header.group(1) if header else "unknown"

    declared_lkg = lkg_versions.get(base)
    version_used = version_str or fallback_version or "unknown"

    # Status based on LKG comparison
    try:
        status = "LKG ✅" if version_used == declared_lkg else (
            "newer 🔼" if v.parse(version_used) > v.parse(declared_lkg) else "older 🔽"
        )
    except Exception:
        status = "-"

    docstring = re.search(r'"""(.*?)"""', text, re.DOTALL)
    purpose = docstring.group(1).strip().split("\n")[0] if docstring else fallback_descriptions.get(base, "No description found")

    cli_flags = sorted(set(re.findall(r"--(\w+)", text)) - {"help", "version", "v"})

    return {
        "Module": base,
        "File": name,
        "LKG": declared_lkg or "-",
        "This Ver": version_used,
        "Status": status,
        "Run Order": suggested_order.index(base) + 1 if base in suggested_order else "-",
        "CLI Flags": ", ".join(f"--{flag}" for flag in cli_flags) if cli_flags else "-",
        "Purpose": purpose
    }

def main():
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir.parent / "src"
    docs_dir = base_dir.parent / "docs"
    verification_path = docs_dir / "VERIFICATION.md"

    print(f"🛠 list_python_modules.py - v1.2.1")
    print(f"📘 Purpose: List Python modules with LKG matching, CLI flags, and version status")
    print(f"📂 Scanning: {src_dir.resolve()}\n")

    lkg_versions = parse_lkg_versions(verification_path)
    results = []

    for path in sorted(src_dir.glob("*.py")):
        results.append(extract_info(path, lkg_versions))

    if not results:
        print("❌ No .py files found.")
        return

    print(f"{'Module':<25} | {'File':<40} | {'This Ver':<10} | {'LKG':<8} | {'Status':<8} | {'Run Order':<10} | {'CLI Flags':<25} | Purpose")
    print("-" * 160)
    for r in results:
        print(f"{r['Module']:<25} | {r['File']:<40} | {r['This Ver']:<10} | {r['LKG']:<8} | {r['Status']:<8} | {r['Run Order']:<10} | {r['CLI Flags']:<25} | {r['Purpose']}")

if __name__ == "__main__":
    main()
