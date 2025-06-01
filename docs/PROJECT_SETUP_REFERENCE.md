# 🧾 Project Setup Reference – PDF to Markdown Tools

You are helping me manage a modular Python project to convert D&D PDFs into Markdown. I’ve uploaded the key project reference files including:

- `PROJECT_OVERVIEW.md`: explains overall goals, inputs, outputs
- `PROJECT_SETUP_REFERENCE.md`: details project folder structure, naming rules, and CLI conventions
- `TODO.md`: current and completed development tasks
- `VERIFICATION.md`: tracks last known good (LKG) script versions

Please refer to these files to maintain consistency in script updates, syntax rules, flag conventions, and directory structure. I’ll be adding or modifying Python scripts, and I want you to ensure they follow the policies in these documents (especially `PROJECT_SETUP_REFERENCE.md`). Also help me maintain these `.md` files as the project evolves.

I have uploaded a backup of my files : session_core_backup.zip . This zip file need to be unzipped now. It has all active files from src/ and docs/ directories, which need to be kept in your memory and updates any version of these files you have in memory already. PLease confirm that you have done this and understand this step.


# 🗂️ Folder Layout (relative paths, GitHub-friendly)
project_root/
├── src/                      # Python scripts (called with relative paths)
├── data/
│   ├── input_pdfs/           # Raw PDFs
│   └── extracted_text/       # All extracted or processed outputs
├── docs/                     # PROJECT_OVERVIEW.md, PROJECT_SETUP_REFERENCE.md, TODO.md, VERIFICATION.md, other docs
├── archive/                  # old .py versions
│   └── LKG/                  # Last Known Good versions
└── README.md, requirements.txt

# Extract the accompanying ZIP file with paths
I have uploaded a backup of my files : session_core_backup.zip . This zip file need to be unzipped now. It has all active files from src/ and docs/ directories, which need to be kept in your memory and updates any version of these files you have in memory already. PLease confirm that you have done this and understand this step.

# 🧰 Script Naming & Versioning
- All Python files must include:
  - Script name, purpose, version number in a header comment
  - Matching printout to terminal when run
  - Default mode: shows a simple progress bar using tqdm
  - --all flag for choosing all PDFs to process , have a count / summary at end of script when using this flag
- Verbose flag: --verbose for detailed CLI debugging output (optional)

- Output versioned download files as:
  - `scriptname_v1.2.3.py` ← for initial testing, then  archival in `archive/`
  - `scriptname.py`        ← for active use in `src/`

- Internal calls and relative imports must use the **non-versioned filename**
- All outputs must go to relative folders using `../data/...` from within `src/`

# ✅ Output Rule
- Scripts auto-create output folders if missing
- Example: `../data/extracted_text/filename.txt` from inside `src/`

# 🔁 Usage Style
- If no input file is given on the command line, the script will list PDFs in `../data/input_pdfs/` and prompt for a selection.
Scripts are called directly with CLI:
```bash
python extract_text.py ../data/input_pdfs/myfile.pdf --verbose
```

# 💡 Execution Behavior
- If `--verbose` is enabled: print detailed logs
- If no flag is used: show clean progress bar (`tqdm`)
- All output paths are relative, GitHub-safe


