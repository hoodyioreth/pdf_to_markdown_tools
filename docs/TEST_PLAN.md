# 🧪 TEST_PLAN.md – PDF → Markdown Pipeline

_Last updated: 2025-06-02_

This test plan defines a stable set of test inputs to validate each script in the pipeline using real files from `data/input_pdfs/`, `data/extracted_text/`, and `data/converted_md/`.

---

## 🧾 Test Inputs (Manually Copied to Active Folders)

| Purpose              | File Location                   | Input Type | Structure Source     |
|----------------------|----------------------------------|------------|-----------------------|
| Heading detection    | input_pdfs/5e_2024_House_Rules_draft_v_0.2.pdf | PDF        | `headings`            |
| Outline fallback     | input_pdfs/Classic_Guide_to_Greyhawk.pdf       | PDF        | `outline`             |
| Visual fallback      | input_pdfs/Greyhawk_Expanded_-_A_Players_Guide_to_Oerik.pdf | PDF | `visual_toc`          |
| Mixed outline/visual | input_pdfs/VER1-03_Gift_of_Beauty_(3E).pdf     | PDF        | `outline + visual`    |
| Post-clean test      | converted_md/Greyhawk_Rebooted_cleaned.md      | Markdown   | Already processed     |
| Fallback / raw .txt  | extracted_text/broken_example.txt              | Text       | No structure (manual) |

---

## ✅ Script-by-Script Test Expectations

### `extract_text.py`
- Test all 4 PDFs → `.txt` appears in `extracted_text/`
- Ensure all outputs are readable and > 500 characters

### `detect_headings.py`
- Should succeed only on headings-style file (House Rules)
- Should fallback silently or fail on others

### `extract_outline.py`
- Should succeed on outline-available files
- Skip or warn on `headings`/`visual`-only inputs

### `parse_visual_toc.py`
- Should succeed on Greyhawk_Expanded and VER1-03
- Should not create output for non-visual files

### `convert_to_md.py`
- For each test PDF:
  - Try converting with structure preference fallback: `headings → outline → visual → raw`
  - Verify `.md` file created

### `clean_md_output.py`
- Run on `Greyhawk_Rebooted_cleaned.md` and newly generated `.md` files
- Ensure outputs are not corrupted or changed on second run

---

## 📁 Expected Output Folders

| Folder            | Contents                          |
|-------------------|-----------------------------------|
| extracted_text/   | `.txt`, `.outline.json`, `.visual_toc.txt` |
| converted_md/     | `.md` and `_cleaned.md` versions  |

---

## 🚧 Notes

- This test bench uses real-world edge cases from the user’s D&D collection
- Files should be copied manually or scripted from verified PDF sources
- Future: include checksum comparison for post-cleaning outputs


### ✅ clean_md_output.py – Test Bench Result

- **Test Date:** 2025-06-02
- **Test Context:** Executed via `run_testbench.py`
- **PDFs Processed:** 4 test documents
- **Result:** Cleaned `_cleaned.md` generated successfully
- **Status:** ✅ Verified functional and promoted to LKG

---

### 🚨 Detected Issue: Missing Tables and Bullet Lists

During analysis of all five testbench Markdown outputs, **no tables or bullet lists were detected** in any file. This suggests:

- Either the source PDFs lacked such elements (unlikely)
- Or, current conversion logic does **not handle table or bullet formatting properly**

🛠️ This needs to be verified and fixed in the Markdown conversion logic. Possibly enhance `convert_to_md.py` or `clean_md_output.py`.

---

### 🔍 Detected Issue: Heading Formatting and Fragmentation

**Spot-check of converted Markdown files revealed:**

- Excessive fragmentation of headings (e.g., `# Spell`, `# Concentration` instead of `# Spell Concentration`)
- False-positive headings like `# O`, `# G`, caused by misinterpreting header fonts or OCR noise
- Duplicated headings and one-letter noise entries
- Breaks semantic grouping and increases token waste when read by GPT

🛠️ Needs refinement in heading detection or during Markdown assembly.

