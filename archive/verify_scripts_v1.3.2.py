"""
Script: verify_scripts.py
Version: 1.3.2
Purpose: Audit .py scripts in src/ for proper headers, and optionally insert missing headers
"""

print("🛠 verify_scripts.py - v1.3.2")
print("📘 Purpose: Audit .py scripts in src/ for proper headers, and optionally insert missing headers")
print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")

import os
import re
from pathlib import Path

src_dir = Path(__file__).parent
docs_path = src_dir.parent / "docs" / "VERIFICATION.md"

def check_header_and_version(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_info = {"has_header": False, "version": None}
    for line in lines[:10]:
        if line.strip().startswith("Script:"):
            header_info["has_header"] = True
        if line.strip().startswith("Version:"):
            match = re.search(r"(\d+\.\d+\.\d+)", line)
            if match:
                header_info["version"] = match.group(1)
    return header_info

def generate_header(script_name, version, purpose):
    return f'''"""\nScript: {script_name}\nVersion: {version}\nPurpose: {purpose}\n"""\n'''

def prompt_insert(script_path, header_text):
    print(f"📎 Suggested header for {script_path.name}:
")
    print(header_text)
    response = input(f"Insert into {script_path.name}? (y/n/skip all): ").strip().lower()
    return response

def process_scripts():
    for py_file in sorted(src_dir.glob("*.py")):
        info = check_header_and_version(py_file)
        if not info["has_header"]:
            print(f"🔍 Missing header: {py_file.name}")
            suggested_header = generate_header(py_file.name, "1.0.0", "FIXME: Describe purpose here.")
            choice = prompt_insert(py_file, suggested_header)
            if choice == "y":
                with open(py_file, "r", encoding="utf-8") as f:
                    contents = f.read()
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(suggested_header + "\n" + contents)
                print(f"✅ Header inserted into {py_file.name}")
            elif choice == "skip all":
                print("⏭ Skipping all remaining.")
                break

if __name__ == "__main__":
    process_scripts()
