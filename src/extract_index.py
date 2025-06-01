#!/usr/bin/env python3
"""
Script: extract_index.py
Version: 1.0.0
Purpose: Extract index terms and page numbers from .txt files for tagging or glossary use.
Author: ChatGPT for Hoody's PDF → Markdown Project
"""

import sys
import re
import json
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "extract_index.py"
SCRIPT_VERSION = "1.0.0"
SCRIPT_PURPOSE = "Extract index terms and page numbers from text"

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEXT_DIR = BASE_DIR / "../data/extracted_text"
OUTPUT_DIR = BASE_DIR / "../data/extracted_text/index_terms"

def parse_args():
    return {
        "show_help": "--help" in sys.argv or "-h" in sys.argv,
        "show_version": "--version" in sys.argv or "-v" in sys.argv,
        "run_all": "--all" in sys.argv,
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
  python extract_index.py --file filename.txt [--verbose]
  python extract_index.py --all

Options:
  --file <filename>     Process a single .txt file
  --all                 Process all .txt files in extracted_text
  --verbose             Print extracted terms to screen
  --version, -v         Show script version
  --help, -h            Show this help message
""")

def extract_index_entries(lines, verbose=False):
    entries = []
    pattern = re.compile(r"^(.*?)\.{2,}\s*(\d{1,4})$")
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            term = match.group(1).strip()
            page = match.group(2).strip()
            if verbose:
                print(f"  ➤ {term} → p.{page}")
            entries.append({"term": term, "page": int(page)})
    return entries

def write_outputs(stem, entries):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"{stem}.index_terms.json"
    md_path = OUTPUT_DIR / f"{stem}.index_terms.md"

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    # Save Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(f"- **{entry['term']}** — page {entry['page']}\n")

def process_file(filepath: Path, verbose=False):
    lines = filepath.read_text(encoding="utf-8").splitlines()
    entries = extract_index_entries(lines, verbose=verbose)
    write_outputs(filepath.stem, entries)
    print(f"✅ Extracted {len(entries)} index entries from {filepath.name}")

def main():
    args = parse_args()

    if args["show_help"]:
        print_help()
        return
    if args["show_version"]:
        print(f"{SCRIPT_NAME} v{SCRIPT_VERSION}")
        return

    print_header()

    files = []
    if args["run_all"]:
        files = sorted(TEXT_DIR.glob("*.txt"))
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

    for file in tqdm(files, desc="Extracting index", unit="file"):
        process_file(file, verbose=args["verbose"])

if __name__ == "__main__":
    main()
