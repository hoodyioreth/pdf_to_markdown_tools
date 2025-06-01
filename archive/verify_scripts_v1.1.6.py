"""
Script: verify_scripts.py
Version: 1.1.6
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
            if line.startswith(f"# {key}:") or line.startswith('"""') or key in line:
                match = re.search(f"{key}:(.*)", line)
                if match:
                    header_data[key] = match.group(1).strip()
    return header_data

def main():
    src_dir = Path(__file__).resolve().parent
    verif_path = src_dir.parent / "docs" / "VERIFICATION.md"
    verif_data = parse_verification_md(verif_path)

    print("== verify_scripts.py - v1.1.6 ==")
    print("Purpose: Audit .py files in src/ for proper headers and verification match")
    print("Requires: PyMuPDF (install via 'pip install pymupdf')")
    print("")

    for pyfile in sorted(src_dir.glob("*.py")):
        base_name = pyfile.name
        print(f"Analyzing: {base_name}")
        header = check_header(pyfile)
        if all(header.values()):
            print("Header OK")
        else:
            print("Header missing or malformed")
        detected_version = header['Version'] or "Unknown"
        print(f"Version detected: {detected_version}")
        verif_record = verif_data.get(base_name.replace(".py", ""), {})
        verif_version = verif_record.get("version", "❌")
        verif_status = verif_record.get("status", "❌")
        print(f"VERIFICATION.md says: {verif_version} {verif_status}")

        if all(header.values()):
            print("Suggested banner:")
            print(f'    print("== {base_name} - v{header["Version"]} ==")')
            print(f'    print("Purpose: {header["Purpose"]}")')
            print('    print("Requires: PyMuPDF (install via \'pip install pymupdf\')")')
            print("")

if __name__ == "__main__":
    main()
