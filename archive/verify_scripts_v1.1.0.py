"""
Script: verify_scripts.py
Version: 1.1.0
Purpose: Audit .py files in src/ for proper headers, banners, and version verification
"""

import os
import re
from pathlib import Path

print("🛠 verify_scripts.py - v1.1.0")
print("📘 Purpose: Audit .py files in src/ for proper headers, banners, and version verification")
print("📦 Requires: None (uses only standard library)")
print("")

# Path to VERIFICATION.md
verif_path = Path(__file__).resolve().parent.parent / "docs" / "VERIFICATION.md"

# Load simplified VERIFICATION.md data
def load_verification_table():
    if not verif_path.exists():
        print(f"❌ VERIFICATION.md not found at {verif_path}")
        return {}
    with open(verif_path, "r") as f:
        lines = f.readlines()
    verif = {}
    for line in lines:
        if line.strip().startswith("|") and "Script" not in line:
            parts = [part.strip() for part in line.strip().split("|")[1:-1]]
            if len(parts) >= 3:
                script, version, status = parts[:3]
                verif[script.replace(".py", "").strip()] = {
                    "version": version.strip(),
                    "status": status.strip()
                }
    return verif

# Analyze scripts in src/
def analyze_scripts():
    src_dir = Path(__file__).resolve().parent
    verif_data = load_verification_table()
    for script_path in sorted(src_dir.glob("*.py")):
        name = script_path.name
        base_name = script_path.stem.split("_v")[0] if "_v" in script_path.stem else script_path.stem
        print(f"🔍 Analyzing: {name}")

        with open(script_path, "r") as f:
            lines = f.readlines()

        header_match = any("Script:" in l for l in lines[:5]) and any("Version:" in l for l in lines[:5])
        if not header_match:
            print("❌ Header missing or malformed")
        else:
            header_block = "".join(lines[:5])
            script = re.search(r"Script:\s*(\S+)", header_block)
            version = re.search(r"Version:\s*([\d.]+)", header_block)
            purpose = re.search(r"Purpose:\s*(.+)", header_block)
            script_name = script.group(1).replace(".py", "") if script else "Unknown"
            version_str = version.group(1) if version else "Unknown"
            print(f"✅ Header OK")
            print(f"📌 Version detected: {version_str}")

            # Check against VERIFICATION.md
            ref = verif_data.get(script_name, {})
            ref_version = ref.get("version", "❌ Not listed")
            status = "✅" if version_str == ref_version else "❌ MISMATCH"
            print(f"📄 VERIFICATION.md says: {ref_version} {status}")
            if purpose:
                print("📢 Suggested banner:")
                print(f'    print("🛠 {script_name}.py - v{version_str}")')
                print(f'    print("📘 Purpose: {purpose.group(1)}")')
                print('    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')")')
                print('    print("")')
        print("")

if __name__ == "__main__":
    analyze_scripts()
