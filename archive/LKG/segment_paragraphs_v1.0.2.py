# ✅ Script name: segment_paragraphs.py
# ✅ Version: v1.0.2
# ✅ Purpose: Split extracted .txt files into paragraphs for downstream Markdown structuring
# ✅ Dependencies: None (standard library only)

import os
import argparse
from pathlib import Path

VERSION = "v1.0.2"

INPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "extracted_text"

def segment_text(content):
    lines = content.splitlines()
    paragraphs = []
    buffer = []

    for line in lines:
        stripped = line.strip()
        if not stripped or len(stripped) < 3:
            if buffer:
                paragraphs.append(" ".join(buffer).strip())
                buffer = []
        else:
            buffer.append(stripped)

    if buffer:
        paragraphs.append(" ".join(buffer).strip())
    return paragraphs

def process_file(filepath, output_dir):
    # Skip re-segmented files
    if ".segmented." in filepath.name:
        print(f"⏭️ Skipping already segmented file: {filepath.name}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    paragraphs = segment_text(content)
    filename = Path(filepath).stem + ".segmented.txt"
    outpath = output_dir / filename

    with open(outpath, "w", encoding="utf-8") as out:
        out.write("\n\n".join(paragraphs))

    print(f"✅ Segmented and saved: {outpath.name}")

def main():
    parser = argparse.ArgumentParser(description="Segment raw text files into paragraph blocks.")
    parser.add_argument("--file", type=str, help="Specify a single .txt file to segment")
    parser.add_argument("--all", action="store_true", help="Process all .txt files in the input folder")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    print(f"🧠 segment_paragraphs.py - {VERSION}\n")

    if not INPUT_DIR.exists():
        print("❌ Input folder not found.")
        return

    output_dir = INPUT_DIR
    txt_files = sorted(INPUT_DIR.glob("*.txt"))

    if args.all:
        for txt in txt_files:
            process_file(txt, output_dir)
        return

    if args.file:
        single = INPUT_DIR / args.file
        if single.exists():
            process_file(single, output_dir)
        else:
            print(f"❌ File not found: {single}")
        return

    # Interactive fallback
    if not txt_files:
        print("❌ No .txt files found in extracted_text/")
        return

    print("📄 Available .txt files:")
    for i, file in enumerate(txt_files):
        print(f"[{i}] {file.name}")
    choice = input("Enter number (or 'q' to quit): ").strip()
    if choice.lower() == 'q':
        print("❌ Operation canceled.")
        return

    try:
        selected = txt_files[int(choice)]
        process_file(selected, output_dir)
    except (ValueError, IndexError):
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
