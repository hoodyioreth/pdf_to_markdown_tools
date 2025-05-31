# ✅ PDF → Markdown Project – TODO  
_Last updated: May 31, 2025_

## 🏗️ Project Structure

- [x] Choose modular script-per-task design
- [x] Draft high-level overview (`PROJECT_OVERVIEW.md`)
- [x] Set up folder structure (`src/`, `docs/`, `data/`, etc.)

## 🔨 Core Modules (Phase One)

| Script                    | Status         | Version   | Notes                                      |
|---------------------------|----------------|-----------|--------------------------------------------|
| `extract_text.py`         | ✅ Verified     | v1.4.0    | Auto-input select, progress bar, verbose   |
| `extract_outline.py`      | ✅ Verified     | v1.4.0    | Auto-input select, outline to txt/json     |
| `parse_visual_toc.py`     | ✅ Verified     | v1.2.0    | Auto-input select, TOC scan, progress bar  |
| `detect_headings.py`      | 📥 Planned      | -         | Based on font sizes / layout heuristics    |
| `convert_to_md.py`        | 📥 Planned      | -         | Build structured Markdown output           |
| `split_sections.py`       | 📥 Planned      | -         | Chunk large documents into parts           |
| `extract_index.py`        | 📥 Planned      | -         | Identify index pages and terms             |

## 🧠 Optional / Enrichment Modules

- [ ] `tag_entities.py` – Add `[Ref: ...]` or `[MapRef: ...]` tags using known JSON data  
  _Uses: `ref_keywords.json`, `longitudes_from_map.json`_  
  _Priority: Low until core modules are stable_

## 🛠️ Future Enhancements

- [ ] `run_pipeline.py` – Optional CLI script to chain modules together
- [ ] `config.json` – Allow custom rules and toggles per document
- [ ] Markdown beautification and table handling
- [ ] Basic GUI wrapper or Automator action (Mac-only, optional)
- [ ] Error handling and logging framework

---

📁 **Folder suggestions**:
- `src/` – All Python scripts
- `data/` – JSON reference data, extracted text files
- `docs/` – Overview, TODO, Markdown output samples
