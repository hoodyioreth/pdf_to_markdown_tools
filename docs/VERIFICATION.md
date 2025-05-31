# VERIFICATION.md

This file tracks Last Known Good (LKG) statuses and validation notes for core scripts in the PDF-to-Markdown project.

| Script                     | Version   | Status             | Validation Notes                                                                                                                   | Last Verified    |
|:---------------------------|:----------|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:-----------------|
| extract_text_v1.4.0.py     | 1.4.0     | ✅ Last Known Good | Tested on Classic_Guide_to_Greyhawk.pdf and Greyhawk_Expanded_-_A_Players_Guide_to_Oerik.pdf. Both extracted correctly.            | 2025-05-31 15:59 |
| extract_outline_v1.5.1.py  | 1.5.1     | ✅ Last Known Good | Correctly handled outline extraction and fallback. Verbose trace included. Passed on both outline-present and outline-absent PDFs. | 2025-05-31 15:59 |
| parse_visual_toc_v1.3.1.py | 1.3.1     | ✅ Last Known Good | Handles fallback gracefully. TOC detected where expected, fallback message where not.                                              | 2025-05-31 15:59 |

## ✅ Verified on 2025-05-31

The following scripts were tested and confirmed as LKG (Last Known Good):

- `extract_text_v1.5.3.py`
- `extract_outline_v1.6.1.py`
- `parse_visual_toc_v1.3.2.py`
