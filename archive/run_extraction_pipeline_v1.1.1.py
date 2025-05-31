#!/usr/bin/env python3
import subprocess
import argparse
import sys

SCRIPT_VERSION = "v1.1.1"
SCRIPT_NAME = "run_extraction_pipeline.py"

scripts = [
    "extract_text.py",
    "extract_outline.py",
    "parse_visual_toc.py"
]

def run_all(filename, verbose=False):
    for script in scripts:
        print(f"▶️ Running {script}...")
        cmd = ["python3", script, filename]
        if verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"❌ Error running {script}, aborting pipeline.")
            sys.exit(1)
        print(f"✅ Completed {script}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run full PDF-to-Markdown extraction pipeline."
    )
    parser.add_argument("filename", nargs="?", help="PDF file to process")
    parser.add_argument("--all", action="store_true", help="Run all steps on a specific file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose mode")
    parser.add_argument("--version", action="store_true", help="Show script version")

    args = parser.parse_args()

    if args.version:
        print(f"{SCRIPT_NAME} - {SCRIPT_VERSION}")
        sys.exit(0)

    print("🔁 Starting PDF-to-Markdown extraction pipeline...")

    if args.all:
        if not args.filename:
            print("❌ --all requires a filename argument.")
            sys.exit(1)
        run_all(args.filename, verbose=args.verbose)
    else:
        print("❌ You must specify --all and a filename.")
        sys.exit(1)
