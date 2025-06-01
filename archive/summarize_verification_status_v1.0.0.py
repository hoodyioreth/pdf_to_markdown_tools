# Script: summarize_verification_status.py
# Version: 1.0.0
# Purpose: Display a simplified summary of header and verification status for .py scripts

import pandas as pd

data = [
    ("clean_headings_json.py", "✅", "1.0.0", "❌", "Add to verification"),
    ("convert_to_md.py", "✅", "2.0.2", "✅", "—"),
    ("detect_headings.py", "✅", "1.0.1", "✅", "—"),
    ("diagnose_structure_sources_v1.0.0.py", "✅", "1.0.0", "❌", "Add to verification"),
    ("extract_outline.py", "❌", "—", "❌", "Needs header + entry"),
    ("extract_text.py", "✅", "1.6.3", "✅", "—"),
    ("list_python_modules.py", "✅", "1.2.4", "❌", "Add to verification"),
    ("parse_visual_toc.py", "❌", "—", "❌", "Needs header + entry"),
    ("parse_visual_toc_v1.3.6.py", "✅", "1.3.6", "❌", "Add to verification"),
    ("run_extraction_pipeline.py", "❌", "—", "❌", "Needs header + entry"),
    ("verify_scripts.py", "✅", "1.0.0", "✅", "Mismatch: update VERIFICATION.md"),
    ("verify_scripts_v1.0.1.py", "✅", "1.0.1", "✅", "—"),
    ("verify_scripts_v1.1.0.py", "✅", "1.1.0", "✅", "Mismatch: update VERIFICATION.md"),
    ("verify_scripts_v1.1.6.py", "✅", "1.1.6", "✅", "Mismatch: update VERIFICATION.md"),
    ("verify_scripts_v1.1.7.py", "✅", "1.1.7", "✅", "Mismatch: update VERIFICATION.md"),
    ("verify_scripts_v1.1.8.py", "✅", "1.1.8", "✅", "Mismatch: update VERIFICATION.md"),
]

df = pd.DataFrame(data, columns=["Script", "Header", "Version", "VERIFICATION.md", "Action Needed"])
print(df.to_string(index=False))
