# Script: list_python_modules.py
# Version: 1.2.4
# Purpose: List Python modules with version and verification match (simplified)

import os
import re
from pathlib import Path

print("🛠 list_python_modules.py - v1.2.4")
print("📘 Purpose: List Python modules with version and verification match (simplified)")
print("📦 Requires: None (uses only standard library)")
print("")

verif_path = Path(__file__).resolve().parent.parent / "docs" / "VERIFICATION.md"
src_path = Path(__file__).resolve().parent

def parse_verification():
    if not verif_path.exists():
        return {}
    with open(verif_path, "r") as f:
        lines = f.readlines()
    entries = {}
    for line in lines:
        if line.strip().startswith("|") and not line.strip().startswith("| Script"):
            parts = [p.strip() for p in line.strip().split("|") if p.strip()]
            if len(parts) >= 2:
                script, version = parts[:2]
                entries[script] = version
    return entries

def extract_version(file_path):
    with open(file_path, "r") as f:
        content = f.read(512)
    version_match = re.search(r"Version:\s*([0-9]+\.[0-9]+\.[0-9]+)", content)
    if version_match:
        return version_match.group(1)
    return "Unknown"

def list_modules():
    print("\n📘 list_python_modules.py - v1.2.4")
    print("📂 Scanning for Python modules in ./src")
    print("")

    verified = parse_verification()
    results = []

    for file in sorted(src_path.glob("*.py")):
        name = file.stem
        base = re.sub(r"_v\d+\.\d+\.\d+$", "", name)
        version = extract_version(file)
        ver_status = "❌"
        if base in verified:
            if verified[base] == version:
                ver_status = "✅"
        else:
            ver_status = "❌❌"
        print(f"{file.name:<35} | Version: {version:<8} | Verified: {ver_status}")
        results.append((file.name, version, ver_status))

list_modules()
