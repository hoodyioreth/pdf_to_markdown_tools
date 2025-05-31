# 📚 Project Overview: PDF → Markdown Converter (Modular)

This project converts PDFs into structured Markdown documents. It is designed to be modular, allowing flexible extraction and enrichment steps for various types of documents, including general academic files and Greyhawk-related campaign material (e.g., TOEE).

## 🎯 Purpose

- Convert PDFs into clean Markdown to reduce size and improve token efficiency
- Support flexible parsing logic across different PDF structures
- Enable Greyhawk enrichment by tagging places, factions, and locations using reference JSONs

## 🧱 Modular Script-Per-Task Architecture

Each module does one job. Example scripts include:

- `extract_text.py` – Raw text extraction (v1.4.0, input picker, progress bar)
- `extract_outline.py` – Built-in PDF TOC/bookmarks (v1.4.0, input picker)
- `parse_visual_toc.py` – Visual TOC scanning (v1.2.0, input picker)
- `detect_headings.py` – Heading detection (planned)
- `convert_to_md.py` – Markdown output (planned)
- `split_sections.py` – Break long PDFs (planned)
- `tag_entities.py` – Optional Greyhawk tagging (planned)

## 🧰 Output Rules

- All scripts output to `../data/extracted_text/` from within `src/`
- Default mode shows progress bar (via `tqdm`)
- `--verbose` flag prints detailed logs instead

## ✅ Project Status

See `TODO.md` for live progress tracking.

---

Created with ChatGPT. Last updated May 31, 2025.
