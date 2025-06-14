# ✅ VERIFICATION.md

| Script               | Version   | Status             | Notes                                                                                                                                                                          | Last Verified    |
|:---------------------|:----------|:-------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
| detect_headings      | 1.0.3     | ✅ Last Known Good | Emits structured dicts with text+size for heading repair                                                                                                                       | 2025-06-02       |
| fix_headings         | 1.1.1     | ✅ Last Known Good | Adds interactive file menu fallback                                                                                                                                            | 2025-06-02       |
| segment_paragraphs   | 1.0.2     | ✅ Last Known Good | Skips .segmented.* files, interactive fallback                                                                                                                                 | 2025-06-02       |
| convert_to_md        | 2.0.9     | ✅ Last Known Good | Handles dict+string headings, structure fallback verified                                                                                                                      | 2025-06-02       |
| extract_text         | 1.6.3     | ✅ Last Known Good | Tested on 5 Greyhawk PDFs                                                                                                                                                      | 2025-05-31 09:45 |
| parse_visual_toc     | 1.3.6     | ✅ Last Known Good | Rewritten for robust fallback                                                                                                                                                  | 2025-06-01 08:05 |
| verify_scripts       | 1.0.1     | ✅ Last Known Good | Audits script headers and VERIFICATION.md                                                                                                                                      | 2025-06-01 10:14 |
| interactive_pipeline | 1.0.0     | ✅ Last Known Good | Interactive CLI pipeline that guides the user step-by-step through PDF → text → headings → markdown conversion using extract_text.py, detect_headings.py, and convert_to_md.py | 2025-06-02       |
| split_sections       | 1.0.0     | ✅ Last Known Good | Verified with synthetic test input (4-part split)                                                                                                                              | 2025-06-01       |
| extract_index        | 1.0.0     | ✅ Last Known Good | Verified on Classic_Guide_to_Greyhawk.txt (13 entries)                                                                                                                         | 2025-06-01       |

### ✅ clean_md_output.py – Last Known Good (LKG)

- **Version:** v1.0.2
- **Promoted:** 2025-06-02
- **Notes:** Fully passed test bench via run_testbench.py; output validated. Handles --all, <filename>, and menu prompt logic. Auto-cleans spacing, lists, and table formatting.
