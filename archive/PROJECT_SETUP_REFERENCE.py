# 🧾 Project Setup Reference – PDF to Markdown Tools

# 🗂️ Folder Layout (relative paths, GitHub-friendly)
project_root/
├── src/                      # Python scripts (called with relative paths)
├── data/
│   ├── input_pdfs/           # Raw PDFs
│   └── extracted_text/       # All extracted or processed outputs
├── docs/                     # README, TODO, examples, project setup notes
└── README.md, requirements.txt

# 🧰 Script Naming & Versioning
- All Python files must include:
  - Script name, purpose, version number in a header comment
  - Matching printout to terminal when run
  - Verbose flag: --verbose for detailed CLI debugging output
  - Default mode: shows a simple progress bar using tqdm

- Output versioned download files as:
  - `scriptname_v1.2.3.py` ← for archival/download
  - `scriptname.py`        ← for active use in `src/`

- Internal calls and relative imports must use the **non-versioned filename**
- All outputs must go to relative folders using `../data/...` from within `src/`

# ✅ Output Rule
- Scripts auto-create output folders if missing
- Example: `../data/extracted_text/filename.txt` from inside `src/`

# 🔁 Usage Style
Scripts are called directly with CLI:
```bash
python extract_text.py ../data/input_pdfs/myfile.pdf --verbose
```

# 💡 Execution Behavior
- If `--verbose` is enabled: print detailed logs
- If no flag is used: show clean progress bar (`tqdm`)
- All output paths are relative, GitHub-safe

# 🧠 Tip
Use `README.md`, `TODO.md`, and this file in `/docs` to track structure, expectations, and team workflows.
