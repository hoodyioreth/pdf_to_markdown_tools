#!/usr/bin/env python3
"""
Script: fix_headings.py
Version: 1.1.0
Purpose: Validate and optionally fix malformed headings.json files with size→level fallback
Author: ChatGPT for Hoody's PDF → Markdown Project
"""

import sys
import json
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "fix_headings.py"
SCRIPT_VERSION = "1.1.0"
SCRIPT_PURPOSE = "Validate and optionally fix malformed headings.json files (with size→level fallback)"

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEXT_DIR = BASE_DIR / "../data/extracted_text"

def parse_args():
    return {
        "show_help": "--help" in sys.argv or "-h" in sys.argv,
        "show_version": "--version" in sys.argv or "-v" in sys.argv,
        "run_all": "--all" in sys.argv,
        "fix": "--fix" in sys.argv,
        "verbose": "--verbose" in sys.argv,
        "target_file": next((sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--file"), None)
    }

def print_header():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")

def print_help():
    print_header()
    print("""
Usage:
  python fix_headings.py --file filename.headings.json [--fix] [--verbose]
  python fix_headings.py --all [--fix]

Options:
  --file <filename>     Validate one headings.json file
  --all                 Validate all headings.json files
  --fix                 Apply fixes and overwrite the file
  --verbose             Print problematic entries
  --version, -v         Show script version
  --help, -h            Show this help message
""")

def size_to_level(size):
    try:
        size = float(size)
        if size >= 20: return 1
        elif size >= 16: return 2
        elif size >= 14: return 3
        elif size >= 12: return 4
        elif size >= 10: return 5
        else: return 6
    except:
        return None

def validate_and_fix(path: Path, fix: bool = False, verbose: bool = False):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to parse {path.name}: {e}")
        return

    if not isinstance(data, list):
        print(f"❌ {path.name} is not a list.")
        return

    fixed = []
    errors = 0
    for entry in data:
        if not isinstance(entry, dict):
            errors += 1
            if verbose:
                print(f"  ⚠️ Skipping non-dict entry: {entry}")
            continue
        if "text" not in entry or not entry["text"].strip():
            errors += 1
            if verbose:
                print(f"  ⚠️ Missing/empty text: {entry}")
            continue

        level = None
        if "level" in entry:
            try:
                level = int(entry["level"])
            except:
                level = None
        elif "size" in entry:
            level = size_to_level(entry["size"])

        if level is None:
            errors += 1
            if verbose:
                print(f"  ⚠️ Invalid level and size fallback failed: {entry}")
            continue

        entry["level"] = level
        fixed.append(entry)

    if fix:
        path.write_text(json.dumps(fixed, indent=2), encoding="utf-8")
        print(f"✅ Fixed and saved {path.name} ({len(fixed)} valid headings)")
    else:
        print(f"✅ Validated {path.name} → {len(fixed)} valid / {len(data)} total entries")

def main():
    args = parse_args()

    if args["show_help"]:
        print_help()
        return

    if not args["run_all"] and not args["target_file"]:
        json_files = sorted(TEXT_DIR.glob("*.headings.json"))
        if not json_files:
            print("❌ No .headings.json files found in extracted_text/")
            return

        print("\n📄 Available .headings.json files:")
        for i, file in enumerate(json_files):
            print(f"[{i}] {file.name}")
        choice = input("Enter number (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            print("❌ Operation canceled.")
            return

        try:
            selected = json_files[int(choice)]
            validate_and_fix(selected, fix=args["fix"], verbose=args["verbose"])
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
        return
    if args["show_version"]:
        print(f"{SCRIPT_NAME} v{SCRIPT_VERSION}")
        return

    print_header()

    files = []
    if args["run_all"]:
        files = sorted(TEXT_DIR.glob("*.headings.json"))
    elif args["target_file"]:
        target = TEXT_DIR / args["target_file"]
        if not target.exists():
            print(f"❌ File not found: {target}")
            return
        files = [target]
    else:
        print("❌ No input provided. Use --file or --all.")
        print_help()
        return

    for file in tqdm(files, desc="Validating headings", unit="file"):
        validate_and_fix(file, fix=args["fix"], verbose=args["verbose"])

if __name__ == "__main__":
    main()
