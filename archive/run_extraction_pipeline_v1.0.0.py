
import subprocess

print("🔁 Starting PDF-to-Markdown extraction pipeline...")

scripts = [
    "extract_text.py",
    "extract_outline.py",
    "parse_visual_toc.py"
]

for script in scripts:
    print(f"▶️ Running {script}...")
    result = subprocess.run(["python3", script])
    if result.returncode != 0:
        print(f"❌ Error running {script}, aborting pipeline.")
        exit(1)
    print(f"✅ Completed {script}.")

print("🎉 All extraction steps completed successfully.")
