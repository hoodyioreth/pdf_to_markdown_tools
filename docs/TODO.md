# ✅ PDF → Markdown Project – TODO  
_Last updated: 2025-06-02_

## ✅ Project Setup

- [x] Modular script-per-task architecture
- [x] Folder structure: `src/`, `docs/`, `data/`
- [x] CLI conventions: `--all`, `--version`, `--help`

---

## 🧩 Phase 1 – Core Extraction

- [x] `extract_text.py` – Extract `.txt` from PDF
- [x] `detect_headings.py` – Font-size based heading detection
- [x] `fix_headings.py` – Validate and repair `headings.json`
- [x] `extract_outline.py` – Outline bookmarks to `.json`
- [x] `parse_visual_toc.py` – Visual TOC scan (fallback)
- [x] `convert_to_md.py` – Build Markdown from `.txt` and metadata
- [x] `split_sections.py` – Split `.md` by heading level
- [x] `extract_index.py` – Parse index into `index_terms.json`

---

## 🔧 Phase 2 – Markdown Cleanup & Structure

- [x] `segment_paragraphs.py` – Segment text blocks into readable paragraphs
- [x] `clean_headings_json.py` – Clean malformed headings JSON (duplicate removal etc.)
- [x] `diagnose_structure_sources.py` – Diagnostic fallback for structure choice
- [x] `clean_md_output.py` – Post-process: normalize spacing, fix lists/tables ✅ LKG v1.0.2

---

## 🎨 Phase 3 – Output Enhancement

- [ ] `Generate valid Markdown tables` – Reformat list blocks into pipe-style tables
- [ ] `add_yaml_metadata.py` – Inject frontmatter metadata block into `.md`

---

## 🌍 Phase 4 – Enrichment & Automation

- [ ] `tag_entities.py` – Auto-tag `[Ref: ...]` and `[MapRef: ...]` using JSON
- [ ] `run_pipeline.py` – Batch CLI runner for all PDFs
- [ ] `config.json` – Per-document rule toggles
- [ ] GUI wrapper (macOS Automator or Tkinter)
- [ ] Error handling + logging framework (`--log`, failover capture)

---

## 🧰 Utility Scripts

- [x] `interactive_pipeline.py` – Guided CLI flow (v1.0.0 ✅ LKG)
- [ ] `run_extraction_pipeline.py` – Auto-run pipeline (`--all`, `--summary`)
- [ ] `verify_scripts_v1.2.0.py` – Verify versions & headers across repo
- [ ] `list_python_modules.py` – Utility: show import tree for debugging
- [ ] Refine heading detection to avoid over-fragmentation (e.g., multiple one-word headers)
- [ ] Suppress false-positive headings from OCR noise (e.g., `# O`, `# TO`, `# G`)
- [ ] Deduplicate identical headings that appear in close proximity
- [ ] Add validation to heading detection or convert_to_md to consolidate related heading lines