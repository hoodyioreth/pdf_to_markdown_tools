"""
Script: verify_scripts.py
Version: 1.3.1
Purpose: Audit .py scripts in src/ for proper headers, and optionally insert missing headers
"""

print("🛠 verify_scripts.py - v1.3.1")
print("📘 Purpose: Audit .py scripts in src/ for proper headers, and optionally insert missing headers")
print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')\n")

import os
import re
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
VER_PATH = SRC_DIR.parent / "docs" / "VERIFICATION.md"

HEADER_PATTERN = re.compile(r'^"""\nScript: (.*?)\nVersion: (.*?)\nPurpose: (.*?)\n"""', re.DOTALL)

def extract_header(file_path):
    with open(file_path, 'r') as f:
        content = f.read(300)
        match = HEADER_PATTERN.search(content)
        if match:
            return {
                "Script": match.group(1).strip(),
                "Version": match.group(2).strip(),
                "Purpose": match.group(3).strip()
            }
    return None

def suggest_header(filename, purpose, version):
    script_line = f'Script: {filename}'
    version_line = f'Version: {version}'
    purpose_line = f'Purpose: {purpose}'
    return f'"""\n{script_line}\n{version_line}\n{purpose_line}\n"""\n'

def interactive_insert(script_path, header_text):
    with open(script_path, 'r') as f:
        lines = f.readlines()
    print(f"📎 Suggested header for {script_path.name}:
{header_text}")
    response = input("Insert this header? (y/n): ").strip().lower()
    if response == 'y':
        with open(script_path, 'w') as f:
            f.write(header_text + '\n' + ''.join(lines))
        print("✅ Header inserted.")
    else:
        print("⏭ Skipped.")

def main():
    for script_file in SRC_DIR.glob("*.py"):
        header = extract_header(script_file)
        base_name = script_file.stem
        if not header:
            print(f"❌ No header found in {script_file.name}")
            purpose = input(f"Enter purpose for {script_file.name}: ").strip()
            version = input(f"Enter version for {script_file.name} (e.g., 1.0.0): ").strip()
            header_text = suggest_header(script_file.name, purpose, version)
            interactive_insert(script_file, header_text)
        else:
            print(f"✅ {script_file.name} has header: v{header['Version']} — {header['Purpose']}")

if __name__ == "__main__":
    main()
