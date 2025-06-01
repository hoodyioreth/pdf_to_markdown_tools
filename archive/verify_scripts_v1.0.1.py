
"""
Script: verify_scripts.py
Version: 1.0.1
Purpose: Audit .py files in src/ for proper headers, banners, and version verification
"""

import os
import re
from pathlib import Path

src_dir = Path(__file__).resolve().parent
verif_path = src_dir.parent / "docs" / "VERIFICATION.md"

# Load verification entries
verif_entries = {}
if verif_path.exists():
    with open(verif_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"\|\s*(\w+)\s*\|\s*([^\|]+)\|\s*(\d+\.\d+\.\d+)\s*\|", line)
            if match:
                script_name = match.group(1).strip()
                filename = match.group(2).strip()
                version = match.group(3).strip()
                verif_entries[script_name] = (filename, version)

# Scan src directory
for py_file in sorted(src_dir.glob("*.py")):
    print(f"\n🔍 Analyzing: {py_file.name}")
    with open(py_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    head_block = lines[:10]
    script = py_file.name

    triple_match = re.findall(r"Script:\s*(.+)", ''.join(head_block))
    version_match = re.findall(r"Version:\s*(\d+\.\d+\.\d+)", ''.join(head_block))
    purpose_match = re.findall(r"Purpose:\s*(.+)", ''.join(head_block))

    has_header = len(triple_match) == 1 and len(version_match) == 1 and len(purpose_match) == 1

    if has_header:
        script_name = triple_match[0]
        version = version_match[0]
        purpose = purpose_match[0]
        print("✅ Header OK")
        print(f"📌 Version detected: {version}")
    else:
        script_name = script.replace(".py", "")
        version = "❌"
        purpose = None
        print("❌ Header missing or malformed")

    # Compare to VERIFICATION.md
    verif_data = verif_entries.get(script_name, ("❌ Not found", "❌"))
    print(f"📄 VERIFICATION.md says: {verif_data[1]}", end=" ")
    if version != "❌" and version == verif_data[1]:
        print("✅ MATCH")
    else:
        print("❌ MISMATCH")

    if has_header:
        print("📢 Suggested banner:")
        print(f'    print("🛠 {script_name} - v{version}")')
        print(f'    print("📘 Purpose: {purpose}")')
        print('    print("📦 Requires: PyMuPDF (install via \'pip install pymupdf\')")')
        print('    print("")')
