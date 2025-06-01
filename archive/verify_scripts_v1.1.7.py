
# Script: verify_scripts.py
# Version: 1.1.7
# Purpose: Audit all .py scripts in src/ for proper headers and verification match

import os
import re
from pathlib import Path

VERIFICATION_PATH = Path(__file__).parent.parent / "docs" / "VERIFICATION.md"

def parse_verification_md():
    verified = {}
    if not VERIFICATION_PATH.exists():
        return verified
    for line in VERIFICATION_PATH.read_text(encoding="utf-8").splitlines():
        parts = [p.strip() for p in line.strip().split('|') if p.strip()]
        if len(parts) < 3 or parts[0].startswith('#'):
            continue
        script, version, status = parts[:3]
        verified[script] = (version, status)
    return verified

def extract_header_info(lines):
    script, version, purpose = None, None, None
    for line in lines[:10]:
        if line.startswith('# Script:'):
            script = line.split(':', 1)[1].strip()
        elif line.startswith('# Version:'):
            version = line.split(':', 1)[1].strip()
        elif line.startswith('# Purpose:'):
            purpose = line.split(':', 1)[1].strip()
    return script, version, purpose

def check_script(path, verified_dict):
    print(f"Analyzing: {path.name}")
    lines = path.read_text(encoding="utf-8").splitlines()
    script, version, purpose = extract_header_info(lines)
    banner_ok = all([script, version, purpose])

    if banner_ok:
        print("Header OK")
    else:
        print("Header missing or malformed")

    print(f"Version detected: {version or 'Unknown'}")

    base_script_name = path.name.replace(".py", "")
    if base_script_name in verified_dict:
        v, status = verified_dict[base_script_name]
        print(f"VERIFICATION.md says: {v} {status}")
    else:
        print("VERIFICATION.md entry: ❌ Not found")

    if banner_ok:
        print("Suggested banner:")
        print(f'    print("🛠 {script} - v{version}")')
        print(f'    print("📘 Purpose: {purpose}")')
        print(f'    print("📦 Requires: PyMuPDF (install via \'pip install pymupdf\')")')
    print("")

def main():
    print("🛠 verify_scripts.py - v1.1.7")
    print("📘 Purpose: Audit .py scripts in src/ for proper headers and verification match")
    print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')\n")

    src_dir = Path(__file__).parent
    verified = parse_verification_md()

    for pyfile in sorted(src_dir.glob("*.py")):
        if pyfile.name.startswith("test_"):
            continue
        check_script(pyfile, verified)

if __name__ == "__main__":
    main()
