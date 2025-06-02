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


---

_Last updated automatically during session sync._

## Phase 1

- [x] `convert_to_md.py` – ✅ Completed and validated (v1.0.4 LKG)
- [x] `split_sections.py` – ✅ Completed and verified (v1.0.0 LKG)
- [x] `extract_index.py` – ✅ Completed and verified (v1.0.0 LKG)
- [x] Build `interactive_pipeline.py` from scratch (v1.0.0) — interactive flow for converting PDF to Markdown - ✅ Verified on 2025-06-02

## Phase 2

- [ ] `Fix malformed headings.json` – To be verified if already partially implemented
- [ ] `Clean bad structural tags` – Regex-based cleanup needed for structural debris
- [ ] `Segment .txt into paragraphs` – Text block segmentation pending implementation

## Phase 3

- [ ] `clean_md_output.py` – Post-processing module not yet in `src/`
- [ ] `Generate valid Markdown tables` – No table generator module found

## Phase 4

- [ ] `tag_entities.py` – Entity/reference tagger missing
- [ ] `run_pipeline.py` – Batch orchestrator not yet implemented
- [ ] `config.json` – JSON config system design pending
- [ ] `GUI wrapper (macOS)` – Optional GUI/Automator wrapper
- [ ] `Error handling framework` – Needs `--log` support and structured logging

## 📦 Module Phase Checklist

### Phase 1
- [x] `convert_to_md.py` – ✅ Completed and validated (v1.0.4 LKG)
- [x] `split_sections.py` – ✅ Completed and verified (v1.0.0 LKG)
- [x] `extract_index.py` – ✅ Completed and verified (v1.0.0 LKG)

### Phase 2
- [ ] `Fix malformed headings.json` – To be verified if already partially implemented
- [ ] `Clean bad structural tags` – Regex-based cleanup needed for structural debris
- [ ] `Segment .txt into paragraphs` – Text block segmentation pending implementation

### Phase 3
- [ ] `clean_md_output.py` – Post-processing module not yet in `src/`
- [ ] `Generate valid Markdown tables` – No table generator module found

### Phase 4
- [ ] `tag_entities.py` – Entity/reference tagger missing
- [ ] `run_pipeline.py` – Batch orchestrator not yet implemented
- [ ] `config.json` – JSON config system design pending
- [ ] `GUI wrapper (macOS)` – Optional GUI/Automator wrapper
- [ ] `Error handling framework` – Needs `--log` support and structured logging

---

🧭 Pipeline Execution Tools (Added: 2025-06-02)
Script Name	Phase	Priority	Description
interactive_pipeline.py	1–4	🔴 High	CLI-based guided flow for one PDF, showing outputs and prompting at each step
run_pipeline.py	1–4	🟠 Medium	Batch runner that auto-processes all PDFs in data/input_pdfs/ using --all

🔧 interactive_pipeline.py Goals (Priority: Start Now)
Let user pick a PDF from data/input_pdfs/

Show live progress at each step:

✅ Text extraction

✅ Heading or outline detection

✅ Markdown conversion

🛠 Optionally: index term extraction, reference tagging

Ask before continuing each step, with CLI displays

Useful for debugging pipeline, verifying quality

🔁 run_pipeline.py Goals (For Later)
Auto-run the best-available version of each core module

Use --all to process all PDFs without interaction

CLI flags: --skip-index, --log, --summary

Output summary table after completion

## 🆕 Newly Discovered or Untracked Scripts

| Script Name                   | Version | Phase | Status   | Description |
|------------------------------|---------|--------|----------|-------------|
| clean_headings_json.py       | TBD     | Phase 2 | 🟠 Review | Possibly overlaps with fix_headings or post-processing |
| diagnose_structure_sources.py| TBD     | Phase 2 | 🟠 Review | May assist with fallback logic validation |
| run_extraction_pipeline.py   | TBD     | Phase 4 | 🟠 Review | Likely batch processor for Markdown pipeline |
| verify_scripts_v1.2.0.py     | 1.2.0   | Utility | 🟢 New    | Advanced verification of scripts and versions |
| list_python_modules.py       | TBD     | Utility | 🟢 New    | Lists/inspects Python modules for debugging |