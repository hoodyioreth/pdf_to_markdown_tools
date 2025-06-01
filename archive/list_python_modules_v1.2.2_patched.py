
# Simplified VERIFICATION.md loader (Script | Version | Status)
verif_path = Path(__file__).resolve().parent.parent / "docs" / "VERIFICATION.md"
verif_data = {}
if verif_path.exists():
    with open(verif_path, "r", encoding="utf-8") as vf:
        for line in vf:
            if line.strip().startswith("|") and not line.lower().startswith("| script"):
                parts = [p.strip() for p in line.strip().split("|")[1:-1]]
                if len(parts) >= 3:
                    script, version, status = parts[:3]
                    verif_data[script] = {"version": version, "status": status}
    
# SCRIPT_VERSION = "1.2.2"
# SCRIPT_PURPOSE = "List Python modules with metadata, multiple versions, and LKG fallback"


import os
import re
from pathlib import Path

SCRIPT_VERSION = "1.2.2"
SCRIPT_PURPOSE = "List Python modules with LKG matching, CLI flags, and version status"

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
ARCHIVE_DIR = PROJECT_ROOT / "archive"
LKG_DIR = ARCHIVE_DIR / "LKG"
def extract_version_from_script(filepath):
    try:
        with open(filepath, "r") as f:
            for line in f:
                if "VERSION" in line and "=" in line:
                    match = re.search(r"['\"](\d+\.\d+\.\d+)['\"]", line)
                    if match:
                        return match.group(1)
    except:
        return "unknown"
    return "unknown"

def extract_cli_flags(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.read()
        flags = set(re.findall(r"(--[a-zA-Z0-9\-]+)", lines))
        flags.difference_update({"--help", "--version", "-v"})
        return sorted(flags)
    except:
        return []

def extract_purpose(filepath):
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.strip().startswith("SCRIPT_PURPOSE"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except:
        return "Unknown"
    return "Unknown"

def list_modules():
    module_dict = {}
    for pyfile in sorted(SRC_DIR.glob("*.py")):
        name_parts = pyfile.stem.split("_v")
        base = name_parts[0]
        version = extract_version_from_script(pyfile)
        flags = extract_cli_flags(pyfile)
        purpose = extract_purpose(pyfile)
        is_lkg = check_lkg_matches(pyfile.name)
        status = "LKG" if is_lkg else "-"
        if base not in module_dict:
            module_dict[base] = []
        module_dict[base].append({
            "file": pyfile.name,
            "version": version,
            "is_lkg": is_lkg,
            "status": status,
            "flags": flags,
            "purpose": purpose
        })

    return module_dict

def print_table(module_dict):
    print(f"🛠 list_python_modules.py - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print(f"📂 Scanning: {SRC_DIR}\n")

    print(f"{'Module':<25} | {'File':<40} | {'This Ver':<10} | {'LKG':<8} | {'Status':<8} | {'CLI Flags':<25} | Purpose")
    print("-" * 140)
    for module, entries in module_dict.items():
        for i, entry in enumerate(entries):
            print(f"{module if i==0 else '':<25} | {entry['file']:<40} | {entry['version']:<10} | {'yes' if entry['is_lkg'] else '-':<8} | {entry['status']:<8} | {', '.join(entry['flags']):<25} | {entry['purpose']}")

module_data = list_modules()
print_table(module_data)
