# Script: verify_scripts.py
# Version: 1.2.0
# Purpose: Audit .py scripts in src/ for proper headers and verification match, with tabular output

import os
import re
from pathlib import Path

VER_FILE = Path("../docs/VERIFICATION.md")

def parse_verification_md():
    entries = {}
    if not VER_FILE.exists():
        return entries
    for line in VER_FILE.read_text().splitlines():
        if line.strip().startswith("|") and "Script" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 3:
                entries[parts[0]] = parts[1]
    return entries

def extract_header_info(file_path):
    version, header_ok = "Unknown", "❌"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [next(f, "") for _ in range(5)]
    for line in lines:
        if "Script:" in line and "Version:" in lines[1] and "Purpose:" in lines[2]:
            header_ok = "✅"
        if "Version:" in line:
            match = re.search(r"(\d+\.\d+\.\d+)", line)
            if match:
                version = match.group(1)
    return header_ok, version

def summarize_results(results):
    headers = ["Script", "Header", "Version", "VERIFICATION.md", "Action Needed"]
    col_widths = [30, 8, 10, 18, 30]
    line = "|".join(f" {{:<{w}}} " for w in col_widths)
    sep = "|".join("-" * (w + 2) for w in col_widths)

    print(line.format(*headers))
    print(sep)
    for r in results:
        print(line.format(r['script'], r['header_ok'], r['version'], r['verification_status'], r['action']))

def main():
    print("🛠 verify_scripts.py - v1.2.0")
    print("📘 Purpose: Audit .py scripts in src/ for proper headers and verification match\n")
    ver_data = parse_verification_md()
    results = []

    for file in sorted(Path(".").glob("*.py")):
        script = file.name
        base = file.stem.replace("_v", "").split(".")[0]
        header_ok, version = extract_header_info(file)
        ver_ver = ver_data.get(base, None)

        if ver_ver is None:
            ver_status = "❌"
            action = "Add to verification" if header_ok == "✅" else "Needs header + entry"
        else:
            ver_status = "✅"
            action = "" if ver_ver == version else "Mismatch: update VER.md"

        results.append({
            "script": script,
            "header_ok": header_ok,
            "version": version,
            "verification_status": ver_status,
            "action": action
        })

    summarize_results(results)

if __name__ == "__main__":
    main()
