
# 🛠 convert_to_md.py - v2.0.9
# Purpose: Convert extracted text and structure metadata into well-formatted Markdown
# Changelog:
# - Adds support for outline/heading entries that are plain strings (not dicts)
# - Maintains compatibility with dict-based structure data

import os
import json
from pathlib import Path

INPUT_DIR = "../data/extracted_text"
OUTPUT_DIR = "../data/converted_md"

def load_structure(base_name):
    for ext in ["headings.json", "outline.json", "visual_toc.json"]:
        path = os.path.join(INPUT_DIR, f"{base_name}.{ext}")
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        return [
                            {"text": h["text"] if isinstance(h, dict) and "text" in h else h,
                             "level": h.get("level", 1) if isinstance(h, dict) else 1}
                            for h in data
                        ], ext.split(".")[0]
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON in: {path}")
    return None, "fallback"

def write_markdown(base_name, lines, headings, source):
    md_path = os.path.join(OUTPUT_DIR, f"{base_name}.md")
    with open(md_path, "w") as md_file:
        if headings:
            md_file.write(f"<!-- Structure used: {source} -->\n\n")
            for heading in headings:
                text = heading["text"]
                level = heading.get("level", 1)
                md_file.write(f"{'#' * level} {text}\n\n")
        else:
            md_file.writelines(lines)
    print(f"✅ Converted {base_name} → {base_name}.md (Structure: {source})")

def convert_file(base_name):
    txt_path = os.path.join(INPUT_DIR, f"{base_name}.txt")
    if not os.path.exists(txt_path):
        print(f"❌ Text file missing: {txt_path}")
        return
    with open(txt_path, "r") as f:
        lines = f.readlines()

    headings, source = load_structure(base_name)
    write_markdown(base_name, lines, headings, source)

def list_available():
    files = Path(INPUT_DIR).glob("*.txt")
    return sorted(f.stem for f in files)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert extracted text to Markdown")
    parser.add_argument("filename", nargs="?", help="PDF base name (no extension)")
    parser.add_argument("--version", "-v", action="version", version="2.0.9")
    args = parser.parse_args()

    if args.filename:
        base = Path(args.filename).stem
        convert_file(base)
    else:
        files = list_available()
        print("Choose a PDF to convert to Markdown:")
        for i, name in enumerate(files, 1):
            print(f"[{i}] {name}")
        choice = input("Enter number (0 to exit): ")
        if choice == "0":
            return
        try:
            index = int(choice) - 1
            convert_file(files[index])
        except (ValueError, IndexError):
            print("❌ Invalid selection")

if __name__ == "__main__":
    main()
