# 📄 pdf-to-markdown-tools

A modular set of Python scripts for extracting, cleaning, and converting PDF documents into structured Markdown. Designed for flexibility, clarity, and lightweight processing — with optional support for enriching Greyhawk campaign material.

---

## 🧠 Project Goals

- Convert PDFs into clean Markdown to reduce size and improve token efficiency
- Support both structured (outline-based) and unstructured (visual) TOC extraction
- Modular design: run only the parts you need
- Optional enrichment with custom tags and geolocation using JSON files

---

## 🛠 Key Features

- **extract_text.py** – Grab raw text from PDFs
- **extract_outline.py** – Use embedded PDF bookmarks (if available)
- **parse_visual_toc.py** – Detect visual table of contents
- **detect_headings.py** – Identify headings using fonts and spacing
- **convert_to_md.py** – Convert structured content into Markdown
- **split_sections.py** – Break long PDFs into smaller logical parts
- **tag_entities.py** – Optional tagging using Greyhawk reference data

---

## 📁 Folder Layout

- `src/` – All core scripts
- `data/` – Input PDFs, extracted text, JSON references
- `docs/` – Project notes, examples, TODO
- `run_pipeline.py` – Optional future runner for chaining modules
- `requirements.txt` – Dependency list
- `README.md` – This file

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/pdf-to-markdown-tools.git
cd pdf-to-markdown-tools
bash create_project_structure_mac.sh
```

---

Created by Sean Hood and ChatGPT – 2025
