
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
    
#!/usr/bin/env python3
# SCRIPT_VERSION = "1.2.4"
import os
import re
from pathlib import Path

SCRIPT_VERSION = "1.2.4"
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

def check_lkg_version(base_name):
    matches = sorted(LKG_DIR.glob(f"{base_name}_v*.py"))
    if matches:
        return extract_version_from_script(matches[-1])
    return "-"

def read_verification_lkg_versions():
    lookup = {}
    if VERIF_PATH.exists():
        with open(VERIF_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("|") and "Script Name" not in line:
                    parts = [p.strip() for p in line.strip().strip("|").split("|")]
                    if len(parts) >= 6:
                        script_base = parts[0]
                        file_name = parts[1]
                        version = parts[2]
                        lookup[script_base] = version
    return lookup

def list_modules():
    module_dict = {}
    verif_lkg = read_verification_lkg_versions()
    for pyfile in sorted(SRC_DIR.glob("*.py")):
        base = full_base_name(pyfile.name)
        version = extract_version_from_script(pyfile)
        flags = extract_cli_flags(pyfile)
        purpose = extract_purpose(pyfile)
        lkg_ver = verif_lkg.get(base, check_lkg_version(base))

        if base not in module_dict:
            module_dict[base] = []
        module_dict[base].append({
            "file": pyfile.name,
            "version": version,
            "lkg_version": lkg_ver,
            "flags": flags,
            "purpose": purpose
        })

    return module_dict

def print_table(module_dict):
    print(f"🛠 list_python_modules.py - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print(f"📂 Scanning: {SRC_DIR}\n")

    print(f"{'Module':<25} | {'File':<40} | {'This Ver':<10} | {'LKG Ver':<8} | {'CLI Flags':<25} | Purpose")
    print("-" * 130)
    for module, entries in module_dict.items():
        for i, entry in enumerate(entries):
            print(f"{module if i == 0 else '':<25} | {entry['file']:<40} | {entry['version']:<10} | {entry['lkg_version']:<8} | {', '.join(entry['flags']) if entry['flags'] else '-':<25} | {entry['purpose']}")

if __name__ == "__main__":
    module_data = list_modules()
    print_table(module_data)