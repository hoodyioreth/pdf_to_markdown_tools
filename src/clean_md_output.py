"""
Script: clean_md_output.py
Version: 1.0.2
Purpose: Post-process Markdown files to normalize spacing, fix lists, clean tables, and tidy headings.
"""

import os
import argparse
from pathlib import Path
from tqdm import tqdm

def normalize_spacing(text):
    lines = text.splitlines()
    cleaned = []
    last_blank = False
    for line in lines:
        if line.strip() == "":
            if not last_blank:
                cleaned.append("")
                last_blank = True
        else:
            cleaned.append(line.rstrip())
            last_blank = False
    return "\n".join(cleaned).strip()

def clean_headings(text):
    import re
    lines = text.splitlines()
    return "\n".join([re.sub(r'^(#+)(\s*)', lambda m: m.group(1) + ' ', line) for line in lines])

def fix_list_markers(text):
    import re
    return re.sub(r'^[\-•*]\s+', '- ', text, flags=re.MULTILINE)

def process_file(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = normalize_spacing(content)
    content = clean_headings(content)
    content = fix_list_markers(content)

    out_path = md_path.with_name(md_path.stem + "_cleaned.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path

def resolve_md_file(filename, fallback_dir):
    direct_path = Path(filename)
    if direct_path.exists():
        return direct_path
    fallback_path = fallback_dir / filename
    if fallback_path.exists():
        return fallback_path
    raise FileNotFoundError(f"Markdown file not found: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Post-process Markdown files to normalize and clean formatting.")
    parser.add_argument("file", nargs="?", help="Markdown filename (searched in ../data/converted_md/ if not found)")
    parser.add_argument("--all", action="store_true", help="Process all .md files in ../data/converted_md/")
    parser.add_argument("--version", "-v", action="version", version="clean_md_output.py v1.0.2")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    target_dir = base_dir / "../data/converted_md"

    files = []
    if args.all:
        files = list(target_dir.glob("*.md"))
    elif args.file:
        try:
            resolved = resolve_md_file(args.file, target_dir)
            files = [resolved]
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return
    
    else:
        available = list(target_dir.glob("*.md"))
        if not available:
            print("⚠️ No Markdown files found in ../data/converted_md/")
            return
        print("📄 Select a Markdown file to clean:")
        for i, f in enumerate(available):
            print(f"{i + 1}. {f.name}")
        choice = input("Enter number: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(available)):
            print("❌ Invalid selection.")
            return
        files = [available[int(choice) - 1]]


    for md_path in tqdm(files, desc="Cleaning Markdown"):
        try:
            process_file(md_path)
        except Exception as e:
            print(f"⚠️ Error processing {md_path.name}: {e}")

if __name__ == "__main__":
    print("🧼 clean_md_output.py v1.0.2 – Markdown Post-Processor")
    main()
