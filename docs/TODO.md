# ✅ PDF → Markdown Project – TODO  
_Last updated: 2025-05-31_

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
| `detect_headings.py`      | ✅ Verified     | v1.0.1    | Font-size heading detection fallback logic |
| `convert_to_md.py`        | 📥 Planned      | -         | Build structured Markdown output           |
| `split_sections.py`       | 📥 Planned      | -         | Chunk large documents into parts           |
| `extract_index.py`        | 📥 Planned      | -         | Identify index pages and terms             |

## 🧠 Optional / Enrichment Modules

- [ ] `tag_entities.py` – Add `[Ref: ...]` or `[MapRef: ...]` tags using known JSON data  
  _Uses: `ref_keywords.json`, `longitudes_from_map.json`_  
  _Priority: Low until core modules are stable_


---

📁 **Folder suggestions**:
- `src/` – All Python scripts
- `data/` – JSON reference data, extracted text files
- `docs/` – Overview, TODO, Markdown output samples


## 🛠️ Future Enhancements
_Added: 2025-05-30_

- [ ] `run_pipeline.py` – Optional CLI script to chain modules together
- [ ] `config.json` – Allow custom rules and toggles per document
- [ ] Markdown beautification and table handling
- [ ] Basic GUI wrapper or Automator action (Mac-only, optional)
- [ ] Error handling and logging framework

## 📝 Markdown Output Quality Improvements (Planned)
_Added: 2025-05-31_

| Priority | Fix                                         | Strategy                                                             |
|----------|---------------------------------------------|----------------------------------------------------------------------|
| 🔴 High  | Strip bad structural tags like `[1, 'X', 3]`| Convert to clean heading like `## X`                                |
| 🔴 High  | Clean raw text blocks from `.txt`           | Use smarter paragraph segmentation and spacing                      |
| 🟠 Medium| Generate valid Markdown tables              | Detect structured blocks and format using `|` + `---` syntax         |
| 🟢 Optional | Auto-link `[MapRef: X]` or `[Ref: Y]`       | Use known JSON references for entity enrichment                     |
| 🟢 Optional | Add YAML front matter or TOC              | Helps with downstream parsing, especially in VTTs like Obsidian     |

## 🧼 Structural Cleanup and Markdown Enhancement (Planned)
_Added: 2025-05-31_

| Priority | Task                                                       | Description                                                                 |
|----------|------------------------------------------------------------|-----------------------------------------------------------------------------|
| 🔴 High  | Clean malformed `headings.json` entries                    | Strip lists like `[1, 'Contents', 3]`, retain only usable string headings  |
| 🔴 High  | Improve AI-based heading detection logic (`detect_headings.py`) | Tune heuristics or filters to reduce garbage headings                      |
| 🟠 Medium| Add Markdown post-processing pass (`clean_md_output.py`)   | Normalize spacing, deduplicate text, fix heading levels, tidy tables       |

---

## 📋 Upcoming Validation Tasks

| Script Name           | Expected Version | Task Description                                      | Notes                                              | Status     |
|-----------------------|------------------|-------------------------------------------------------|----------------------------------------------------|------------|
| group_content_by_heading | v1.0.0           | Implement logic to assign paragraphs under headings   | Needed for Phase 2 (semantic Markdown structure)   | ⏳ Pending |
| enrich_with_tags      | v1.0.0           | Inject [Ref:...] and [MapRef:...] tags into Markdown  | Uses keyword map and coordinate database           | ⏳ Pending |
| add_yaml_metadata     | v1.0.0           | Prepend YAML frontmatter block to .md files           | For indexing and token control                     | ⏳ Pending |
| extract_images        | v1.0.0           | Detect and optionally export images from PDFs         | Optional Phase 4 extension                         | ⏳ Pending |