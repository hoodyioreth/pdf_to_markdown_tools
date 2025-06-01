#!/usr/bin/env python3
"""
Script: clean_headings_json.py
Version: 1.0.0
Purpose: Sanitize headings JSON files to remove malformed entries (e.g. lists like [1, 'Intro', 3])
"""

import json
from pathlib import Path

SCRIPT_NAME = "clean_headings_json.py"
SCRIPT_VERSION = "1.0.0"
SCRIPT_PURPOSE = "Sanitize malformed entries in headings JSON files"

BASE = Path(__file__).resolve().parent
HEADINGS_DIR = BASE / "../data/extracted_text"

def is_valid_heading(entry):
    return isinstance(entry, dict) and isinstance(entry.get("text"), str) and len(entry["text"].strip()) > 0

def sanitize_file(path: Path):
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            print(f"⚠️  Skipped (not a list): {path.name}")
            return

        cleaned = []
        for item in data:
            if isinstance(item, dict):
                # Validate 'text' is a clean string, not a list or empty
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    cleaned.append(item)
                elif isinstance(text, list):
                    # Join list to string, if all elements are str/int
                    try:
                        joined = " ".join(str(x) for x in text if isinstance(x, (str, int)))
                        if joined.strip():
                            item["text"] = joined.strip()
                            cleaned.append(item)
                    except Exception:
                        continue

        path.write_text(json.dumps(cleaned, indent=2))
        print(f"✅ Cleaned: {path.name} ({len(cleaned)} valid entries)")
    except Exception as e:
        print(f"❌ Error processing {path.name}: {e}")

def main():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")
    print(f"📂 Scanning: {HEADINGS_DIR.resolve()}")
    print("")

    json_files = sorted(HEADINGS_DIR.glob("*.headings.json"))
    if not json_files:
        print("❌ No .headings.json files found.")
        return

    for file in json_files:
        sanitize_file(file)

if __name__ == "__main__":
    main()
