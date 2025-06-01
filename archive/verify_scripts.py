
"""
Script: verify_scripts.py
Version: 1.0.0
Purpose: Audit all .py scripts in src/ for proper headers and verification match
"""

import os
import re
from pathlib import Path
import pandas as pd

src_dir = Path(__file__).resolve().parent
verif_path = src_dir.parent / "docs" / "VERIFICATION.md"

# Load verification entries for reference
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

# Script analysis output
results = []

for py_file in src_dir.glob("*.py"):
    with open(py_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    script = py_file.name
    head_block = lines[:10]

    # Check for proper triple-quoted header
    triple_match = re.findall(r'Script:\s*(.+)', ''.join(head_block))
    version_match = re.findall(r'Version:\s*(\d+\.\d+\.\d+)', ''.join(head_block))
    purpose_match = re.findall(r'Purpose:\s*(.+)', ''.join(head_block))

    has_header = len(triple_match) == 1 and len(version_match) == 1 and len(purpose_match) == 1

    # Build banner prints
    if has_header:
        banner = [
            f'print("🛠 {triple_match[0]} - v{version_match[0]}")',
            f'print("📘 Purpose: {purpose_match[0]}")',
            'print("📦 Requires: PyMuPDF (install via \'pip install pymupdf\')")',
            'print("")'
        ]
        detected_version = version_match[0]
    else:
        banner = ["⚠️ Header missing or malformed"]
        detected_version = "❌"

    # Check against VERIFICATION.md
    script_base = script.replace(".py", "")
    verif_data = verif_entries.get(script_base, ("❌ Not found", "❌"))
    if detected_version != "❌" and detected_version == verif_data[1]:
        verif_status = "✅"
    else:
        verif_status = "❌"

    results.append({
        "Script": script,
        "Header OK?": "✅" if has_header else "❌",
        "Detected Version": detected_version,
        "VERIFICATION.md Version": verif_data[1],
        "VERIFIED?": verif_status,
        "Banner Output": "\n".join(banner)
    })

# Print summary to console
df = pd.DataFrame(results)
print(df.to_string(index=False))
