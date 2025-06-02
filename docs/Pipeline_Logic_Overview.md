# 📘 PDF to Markdown Pipeline Logic Overview

This document outlines the logic, usage conditions, and CLI prompts for each step in the PDF → Markdown pipeline. It covers required and optional steps, branching behavior, and phase organization.

---

## 🔁 Overview of Phases

### 🧩 Phase 1: Text & Structural Extraction
| Script | Purpose | CLI Example |
|--------|---------|-------------|
| `extract_text.py` | Extract raw text from PDF to `.txt` | `python3 extract_text.py Greyhawk_Rebooted.pdf` or `--all` |
| `detect_headings.py` | Detect heading candidates based on font size | `python3 detect_headings.py Greyhawk_Rebooted.pdf` or no args for menu |
| `fix_headings.py` | Validate/patch headings JSON (adds level field) | `python3 fix_headings.py --file Greyhawk_Rebooted.headings.json --fix` or menu mode |

### 🧩 Phase 2: Optional Enhancers & Parallel Branches
| Script | Purpose | CLI Example |
|--------|---------|-------------|
| `extract_outline.py` | Pull outline bookmarks from PDF (not yet implemented) | `python3 extract_outline.py --all` (planned) |
| `parse_visual_toc.py` | Detect TOC visually from PDF (planned) | `python3 parse_visual_toc.py --file filename.pdf` |
| `segment_paragraphs.py` | Split long text files into paragraphs (independent) | `python3 segment_paragraphs.py --file Greyhawk_Rebooted.txt` or `--all` |

### 🧩 Phase 3: Conversion to Markdown
| Script | Purpose | CLI Example |
|--------|---------|-------------|
| `convert_to_md.py` | Merge `.txt` + optional `.headings.json` / outline / TOC → Markdown | `python3 convert_to_md.py Greyhawk_Rebooted.pdf` or menu |

---

## 🔄 Branch Logic Summary

### Core Path to Markdown
```
extract_text.py
   ↓
detect_headings.py
   ↓
fix_headings.py
   ↓
convert_to_md.py
```

### Fallback Paths
- If `detect_headings.py` is not used or fails:
  - `convert_to_md.py` falls back to using `outline.json` or `visual_toc.json`
  - If none available, it still converts using basic line logic

### Enhancer (Optional)
- `segment_paragraphs.py` can be used **after** `extract_text.py` to break `.txt` into better-parsed `.segmented.txt` for inspection or preprocessing

---

## 💡 Script Prompts and Behaviors

### `extract_text.py`
- Lists PDFs from `../data/input_pdfs/`
- Saves `.txt` to `../data/extracted_text/`
- CLI Flags:
  - `--all`, `--version`, `--help`, `-v`

### `detect_headings.py`
- Requires `.txt` file from extract step
- Outputs `.headings.json`
- CLI Flags:
  - `--all`, `--version`, `--help`, `-v`

### `fix_headings.py`
- Prompts user if no `--file` is specified
- Rewrites `.headings.json` with size → level fallback
- CLI Flags:
  - `--fix`, `--all`, `--version`, `--help`, `-v`

### `segment_paragraphs.py`
- Works on `.txt` or any intermediate text-based file
- Appends `.segmented.txt` only if file not already segmented
- CLI Flags:
  - `--file`, `--all`, `--version`, `--help`, `-v`

### `convert_to_md.py`
- Looks for `.txt` and optionally `.headings.json`, `.outline.json`, `.visual_toc.json`
- Prioritizes structure in this order:
  1. `headings.json`
  2. `outline.json`
  3. `visual_toc.json`
  4. fallback line logic
- CLI Flags:
  - accepts direct filename or launches menu
  - `--version`, `--help`, `-v`

---

_Last updated: 2025-06-02_