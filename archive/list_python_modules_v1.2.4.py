#!/usr/bin/env python3
# 🛠 list_python_modules.py - v1.2.3
# 📘 Purpose: List Python modules with LKG matching, CLI flags, and version status

import os
import re
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"
VERIFICATION_FILE = DOCS_DIR / "VERIFICATION.md"

def extract_metadata(file_path):
    version = "unknown"
    purpose = "Unknown"
    try:
        with open(file_path, "r") as f:
            for line in f:
                if "SCRIPT_VERSION" in line:
                    version = line.split("=")[1].strip().strip('"')
                elif "SCRIPT_PURPOSE" in line:
                    purpose = line.split("=")[1].strip().strip('"')
                if version != "unknown" and purpose != "Unknown":
                    break
    except Exception:
        pass
    return version, purpose

def parse_verification():
    lkg_versions = {}
    try:
        with open(VERIFICATION_FILE, "r") as f:
            for line in f:
                match = re.match(r"- `(.+?)`\s+\(v([\d.]+)\)", line)
                if match:
                    file, version = match.groups()
                    base = re.sub(r"_v\d+\.\d+(\.\d+)?$", "", file.replace(".py", ""))
                    lkg_versions[base] = version
    except Exception:
        pass
    return lkg_versions

def scan_python_modules():
    files = list(SRC_DIR.glob("*.py"))
    lkg_map = parse_verification()
    modules = []

    for file in files:
        filename = file.name
        module_name = re.sub(r'_v\d+\.\d+(\.\d+)?$', '', filename.replace('.py', ''))
        version, purpose = extract_metadata(file)
        lkg_version = lkg_map.get(module_name)
        is_lkg = (version == lkg_version)
        modules.append({
            "module": module_name,
            "file": filename,
            "version": version,
            "lkg": "yes" if is_lkg else lkg_version or "-",
            "status": "LKG" if is_lkg else "-",
            "purpose": purpose
        })
    return modules

def display_table(modules):
    print(f"🛠 list_python_modules.py - v1.2.3")
    print(f"📘 Purpose: List Python modules with LKG matching, CLI flags, and version status")
    print(f"📂 Scanning: {SRC_DIR}\n")
    print(f"{'Module':<25} | {'File':<40} | {'This Ver':<10} | {'LKG':<8} | {'Status':<8} | {'Purpose'}")
    print("-" * 120)
    for m in modules:
        print(f"{m['module']:<25} | {m['file']:<40} | {m['version']:<10} | {m['lkg']:<8} | {m['status']:<8} | {m['purpose']}")

if __name__ == "__main__":
    display_table(scan_python_modules())
