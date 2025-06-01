# 📄 pdf-to-markdown-tools

A modular set of Python scripts for extracting, cleaning, and converting PDF documents into structured Markdown. Designed for flexibility, clarity, and lightweight processing — with optional support for enriching Greyhawk campaign material.

---

## 🧠 Project Goals

- Convert PDFs into clean Markdown to reduce size and improve token efficiency
- Modular script-per-task architecture for extensibility and clarity
- Support both structured (outline-based) and unstructured (visual) TOC extraction
- Optional enrichment with custom tags and geolocation using JSON files

---

## 🧩 Project Phases Overview

### 🔴 Phase 1 – Core Markdown Pipeline
- `extract_text.py` – Grab raw text from PDFs
- `detect_headings.py` – Identify headings via font size/position
- `convert_to_md.py` – Convert `.txt` to structured Markdown
- `split_sections.py` – Break long docs into sections
- `extract_index.py` – Parse PDF index pages for term references

### 🔴 Phase 2 – Cleanup & Structure Fixes
- Clean `headings.json` artifacts
- Normalize structural tags (e.g., bad headings)
- Improve `.txt` paragraph segmentation

### 🟠 Phase 3 – Post-Processing & Enhancements
- `clean_md_output.py` – Normalize spacing, fix levels, deduplication
- Table recognition and reformatting into valid Markdown tables

### 🟢 Phase 4 – Enrichment & Automation
- `tag_entities.py` – Add `[Ref: ...]`, `[MapRef: ...]` using JSON data
- `run_pipeline.py` – CLI runner chaining all modules
- `config.json` – Optional per-document rule customization
- GUI wrapper or Automator (optional)
- Logging and error capture

---

## 📁 Folder Layout

```
project_root/
├── src/                      # All Python scripts
├── data/
│   ├── input_pdfs/           # Raw PDFs
│   └── extracted_text/       # Output .txt and .md files
├── docs/                     # PROJECT_*.md docs, TODO, reference files
├── archive/                  # Versioned backups of .py scripts
│   └── LKG/                  # Last Known Good script versions
└── README.md, requirements.txt
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/pdf-to-markdown-tools.git
cd pdf-to-markdown-tools
bash create_project_structure_mac.sh
```

---

Created by Sean Hood and ChatGPT – 2025