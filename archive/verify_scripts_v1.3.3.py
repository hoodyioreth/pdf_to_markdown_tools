""" 
Script: verify_scripts.py
Version: 1.3.3
Purpose: Audit .py scripts in src/ for proper headers, suggest or insert missing headers
""" 

print("🛠 verify_scripts.py - v1.3.3")
print("📘 Purpose: Audit .py scripts in src/ for proper headers, suggest or insert missing headers")
print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")

import os
import re
from pathlib import Path

src_dir = Path(__file__).resolve().parent
verification_path = src_dir.parent / "docs" / "VERIFICATION.md"

def parse_verification():
    ver_dict = {}
    if not verification_path.exists():
        return ver_dict
    with open(verification_path, "r") as f:
        for line in f:
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if len(parts) >= 3:
                    name, version, status = parts[:3]
                    ver_dict[name] = {"version": version, "status": status}
    return ver_dict

def get_header_info(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    script_name = None
    version = None
    purpose = None
    for line in lines[:10]:
        if "Script:" in line:
            script_name = line.split("Script:")[1].strip()
        if "Version:" in line:
            version = line.split("Version:")[1].strip()
        if "Purpose:" in line:
            purpose = line.split("Purpose:")[1].strip()
    return script_name, version, purpose

def suggest_header(script_path, script_name=None, version="0.0.1", purpose="No description provided."):
    header = []
    header.append(f'print("🛠 {script_path.stem} - v{version}")')
    header.append(f'print("📘 Purpose: {purpose}")')
    header.append('print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")')
    return header

def main():
    ver_dict = parse_verification()
    print("\n📋 Header Verification Results:\n")
    for script_path in sorted(src_dir.glob("*.py")):
        script_name, version, purpose = get_header_info(script_path)
        key = script_path.stem
        print(f"Analyzing: {script_path.name}")
        if script_name and version and purpose:
            print(f"✅ Header OK | Version detected: {version}")
        else:
            print("❌ Header missing or malformed")
        ver_entry = ver_dict.get(key)
        if ver_entry:
            print(f"🔎 VERIFICATION.md says: {ver_entry['version']} {ver_entry['status']}")
        else:
            print("📄 VERIFICATION.md entry: ❌ Not found")
        if not (script_name and version and purpose):
            print("📎 Suggested header:")
            for line in suggest_header(script_path, script_path.stem, version or "0.0.1", purpose or "No description provided."):
                print("    " + line)
        print("")

if __name__ == "__main__":
    main()