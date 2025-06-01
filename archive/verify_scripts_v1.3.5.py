"""
Script: verify_scripts.py
Version: 1.3.5
Purpose: Audit .py scripts in src/ for proper headers, compare with VERIFICATION.md, and offer header insertion
"""

import os
import re
from pathlib import Path
from tabulate import tabulate

SCRIPT_NAME = "verify_scripts.py"
SCRIPT_VERSION = "1.3.5"

print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
print("📘 Purpose: Audit .py scripts in src/ for proper headers, compare with VERIFICATION.md, and offer header insertion")
print("📦 Requires: PyMuPDF (install via 'pip install pymupdf')\n")

SRC_DIR = Path(__file__).resolve().parent
DOCS_DIR = SRC_DIR.parent / "docs"
VER_PATH = DOCS_DIR / "VERIFICATION.md"

HEADER_RE = re.compile(r'^["\']{3}\s*\nScript: (.+?)\nVersion: (.+?)\nPurpose: (.+?)\n["\']{3}', re.DOTALL)
VERSION_RE = re.compile(r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)')

def parse_verification_file():
    ver_data = {}
    if VER_PATH.exists():
        for line in VER_PATH.read_text().splitlines():
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip().strip('|').split('|')]
                if len(parts) >= 4:
                    script, version, status = parts[0], parts[1], parts[2]
                    ver_data[script] = {"version": version, "status": status}
    return ver_data

def detect_header_info(path):
    content = path.read_text(encoding='utf-8', errors='ignore')
    header_match = HEADER_RE.search(content)
    version_match = VERSION_RE.search(content)
    return {
        "has_header": bool(header_match),
        "version": header_match.group(2) if header_match else (version_match.group(1) if version_match else "Unknown")
    }

def audit_scripts():
    ver_data = parse_verification_file()
    results = []

    for py_file in sorted(SRC_DIR.glob("*.py")):
        base = py_file.stem
        info = detect_header_info(py_file)
        ver_info = ver_data.get(base, {"version": "❌", "status": "❌"})
        results.append([
            base,
            "✅" if info["has_header"] else "❌",
            info["version"],
            ver_info["version"],
            ver_info["status"]
        ])

    headers = ["Script", "Header", "Detected", "VER.md", "Status"]
    print(tabulate(results, headers=headers, tablefmt="github"))

if __name__ == "__main__":
    audit_scripts()
