#!/usr/bin/env python3
"""
Script: split_sections.py
Version: 1.0.0
Purpose: Split large .md or .txt files by heading level into smaller segment files.
Author: ChatGPT for Hoody's PDF → Markdown Project
"""

import sys
from pathlib import Path
from tqdm import tqdm

SCRIPT_NAME = "split_sections.py"
SCRIPT_VERSION = "1.0.0"
SCRIPT_PURPOSE = "Split large Markdown or text files by heading level"

# Paths
BASE_DIR = Path(__file__).resolve().parent
EXTRACTED_DIR = BASE_DIR / "../data/extracted_text"
OUTPUT_DIR = BASE_DIR / "../data/extracted_text/split"

# CLI flags
def parse_args():
    return {
        "show_help": "--help" in sys.argv or "-h" in sys.argv,
        "show_version": "--version" in sys.argv or "-v" in sys.argv,
        "run_all": "--all" in sys.argv,
        "level": int(next((sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--level"), 2)),
        "target_file": next((sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--file"), None)
    }

def print_header():
    print(f"🛠 {SCRIPT_NAME} - v{SCRIPT_VERSION}")
    print(f"📘 Purpose: {SCRIPT_PURPOSE}")

def print_help():
    print_header()
    print("""
Usage:
  python split_sections.py --file filename.md [--level 2]
  python split_sections.py --all [--level 2]

Options:
  --file <filename>     Process a single .md or .txt file
  --all                 Process all .md and .txt files in extracted_text
  --level <n>           Heading level to split at (default: 2)
  --version, -v         Show script version
  --help, -h            Show this help message
""")

def split_file(filepath: Path, level: int):
    lines = filepath.read_text(encoding="utf-8").splitlines()
    heading_prefix = "#" * level
    parts = []
    current = []

    for line in lines:
        if line.startswith(heading_prefix) and (len(line) == len(heading_prefix) or line[len(heading_prefix)] == " "):
            if current:
                parts.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append(current)

    out_dir = OUTPUT_DIR / filepath.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, part in enumerate(parts, 1):
        part_path = out_dir / f"{filepath.stem}_part{i}.md"
        part_path.write_text("\n".join(part), encoding="utf-8")

    print(f"✅ Saved {len(parts)} segments for {filepath.name}")

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
        files = sorted(EXTRACTED_DIR.glob("*.md")) + sorted(EXTRACTED_DIR.glob("*.txt"))
    elif args["target_file"]:
        target = EXTRACTED_DIR / args["target_file"]
        if not target.exists():
            print(f"❌ File not found: {target}")
            return
        files = [target]
    else:
        print("❌ No input provided. Use --file or --all.")
        print_help()
        return

    for file in tqdm(files, desc="Splitting files", unit="file"):
        split_file(file, args["level"])

if __name__ == "__main__":
    main()
