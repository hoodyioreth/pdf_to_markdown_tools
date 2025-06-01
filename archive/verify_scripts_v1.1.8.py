"""
Script: verify_scripts.py
Version: 1.1.8
Purpose: Audit all .py scripts in src/ for proper headers and verification match
"""

import os
import re
from pathlib import Path

def parse_verification_md(filepath):
    verif = {}
    if not filepath.exists():
        return verif
    for line in filepath.read_text().splitlines():
        if line.startswith("|") and not line.startswith("| Script"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 3:
                script, version, status = parts[:3]
                verif[script] = {"version": version, "status": status}
    return verif

def check_header(path):
    lines = path.read_text(errors='ignore').splitlines()
    header_data = {"Script": None, "Version": None, "Purpose": None}
    for line in lines[:10]:
        for key in header_data:
            if key in line:
                match = re.search(f"{key}:(.*)", line)
                if match:
                    header_data[key] = match.group(1).strip()
    return header_data

def suggest_banner(header_data, script_name):
    version = header_data.get("Version", "?.?.?")
    purpose = header_data.get("Purpose", "No purpose found.")
    print("Suggested banner:")
    print(f'    print("{script_name} - v{version}")')
    print(f'    print("Purpose: {purpose}")')
    print("    print(\"Requires: PyMuPDF (install via 'pip install pymupdf')\")")
    print("")

def main():
    src_dir = Path(__file__).resolve().parent
    verif_path = src_dir.parent / "docs" / "VERIFICATION.md"
    verif_data = parse_verification_md(verif_path)

    print("verify_scripts.py - v1.1.8")
    print("Purpose: Audit .py scripts in src/ for proper headers and verification match")
    print("Requires: PyMuPDF (install via 'pip install pymupdf')")
    print("")

    for pyfile in sorted(src_dir.glob("*.py")):
        base_name = pyfile.name
        script_stem = pyfile.stem.split("_v")[0]
        print(f"Analyzing: {base_name}")
        header = check_header(pyfile)
        if all(header.values()):
            print("Header OK")
            print(f"Version detected: {header['Version']}")
        else:
            print("Header missing or malformed")
            print("Version detected: Unknown")

        if script_stem in verif_data:
            entry = verif_data[script_stem]
            print(f"VERIFICATION.md says: {entry['version']} {entry['status']}")
        else:
            print("VERIFICATION.md entry: ❌ Not found")

        if all(header.values()):
            suggest_banner(header, script_stem)
        print("")

if __name__ == "__main__":
    main()
