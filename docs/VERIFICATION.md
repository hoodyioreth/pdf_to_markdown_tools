# VERIFICATION.md

This file tracks Last Known Good (LKG) versions, notes, and validation outcomes for all Python scripts used in the PDF-to-Markdown project.

| Script Name           | File                             | Version | Status             | Validation Notes                                                  | Last Verified       |
|-----------------------|----------------------------------|---------|--------------------|-------------------------------------------------------------------|---------------------|
| extract_text          | extract_text_v1.4.0.py           | 1.4.0   | ✅ Last Known Good | Tested on Classic_Guide_to_Greyhawk.pdf and Greyhawk_Expanded_-_A_Players_Guide_to_Oerik.pdf. Both extracted correctly. | 2025-05-31 15:59 |
| extract_outline       | extract_outline_v1.5.1.py        | 1.5.1   | ✅ Last Known Good | Correctly handled outline extraction and fallback. Verbose trace included. Passed on both outline-present and outline-absent PDFs. | 2025-05-31 15:59 |
| parse_visual_toc      | parse_visual_toc_v1.3.1.py       | 1.3.1   | ✅ Last Known Good | Handles fallback gracefully. TOC detected where expected, fallback message where not. | 2025-05-31 15:59 |
| detect_headings       | detect_headings_v1.0.1.py        | 1.0.1   | ✅ Last Known Good | Font-size-based heading detection fallback                         | 2025-05-31 |
| convert_to_md         | convert_to_md_v2.0.2.py          | 2.0.2   | ✅ Last Known Good | Phase 1 complete: outline/headings structure verified across 7 PDFs | 2025-06-01 |
| list_python_modules   | list_python_modules_v1.2.4.py    | 1.2.4   | ✅ Last Known Good | Replaces old LKG flag with version string for accurate reporting | 2025-06-01 |
