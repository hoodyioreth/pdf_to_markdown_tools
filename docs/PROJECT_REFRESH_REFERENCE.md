# 🔁 PROJECT_REFRESH_REFERENCE.md  
_Use this file to reestablish project rules and memory when continuing work in an active ChatGPT session._

## 🧠 Purpose
This file is a **live reference** to help ChatGPT recall project standards, architecture, and validation behaviors during a session.  
It supplements `PROJECT_SETUP_REFERENCE.md` but is used **mid-session** to:

- ✅ Refresh the project structure and behavior rules
- ⏳ Detect if uploaded `.md` or `.py` files are **newer or older** than known versions
- 🔄 Enforce naming/versioning/CLI/output rules across session memory gaps

---

## 🗂️ Project Structure (Relative Paths – GitHub-Friendly)

```
project_root/
├── src/                      # Python scripts (run with relative paths)
├── data/
│   ├── input_pdfs/           # Raw PDFs to process
│   └── extracted_text/       # Text/Markdown outputs
├── docs/                     # PROJECT_*.md documents, logs, session notes
├── archive/                  # Archived .py scripts by version
│   └── LKG/                  # Last Known Good verified script copies
└── README.md, requirements.txt
```

---

# Extract the accompanying ZIP file with paths
I have uploaded a backup of my files : session_core_backup.zip . This zip file need to be unzipped now. It has all active files from src/ and docs/ directories, which need to be kept in your memory and needs to be compared against any version of these files you have in memory already. Prompt me to resolve any conflicts. Please confirm that you have done this and understand this step.


## 🧰 Script Rules

- All scripts **must include**:
  - Header with script name, purpose, version
  - Terminal printout of version and script name at start
  - ✅ `--help`, `--version`, `-v`, and `--all` flags
  - ✅ `--verbose` is optional (only if diagnostic output needed)

- CLI Example:
```bash
python extract_text.py ../data/input_pdfs/myfile.pdf --verbose
```

- All outputs go to: `../data/...` from within `src/`
- Scripts must **auto-create** output folders if missing
- Default behavior: show progress bar using `tqdm`
- `--all` runs batch mode on every PDF in `../data/input_pdfs/`

---

## 🔍 Versioning and File Checks

When `.py` or `.md` files are re-uploaded or edited:
- ChatGPT should **compare version numbers, dates, or content** to verify freshness.
- Use `VERIFICATION.md` to track LKG (Last Known Good) Python scripts.
- Use `TODO.md` to identify stale or incomplete module features.

---

## 🧼 File Naming Rules

| Type       | Rule                                                            |
|------------|-----------------------------------------------------------------|
| Scripts    | Use suffix `_vX.Y.Z.py` for versions, with `scriptname.py` as stable |
| Outputs    | Always relative to `../data/`, e.g. `../data/extracted_text/`   |
| Markdown   | Docs saved to `docs/`, use uppercase naming convention          |

---

## 📊 Output Expectations

- Scripts print filename and progress per file
- Final summary shown when `--all` is used
- Markdown outputs should be token-efficient and clean (YAML header optional)

---

## 🧠 Reminder for ChatGPT

When a user uploads `.py` or `.md` files:
- Check if filename matches a known script
- Compare version or file content with previous session memory (if available)
- Confirm whether this is a **refresh of a newer version**, a rollback, or a parallel test version
- Ask if you are unsure which version should be treated as active

---

---

### 🛠️ Standard CLI Behavior (PDF → Markdown Tools)

Each script accepts the following options:

- `--all`  
→ Automatically process all valid files in the correct data directory (e.g., `../data/converted_md/` or `../data/input_pdfs/`)

- `<filename>`  
→ Run on a single file. If no path is given, the script will **look in the expected input folder** (e.g., `../data/converted_md/filename.md`)

- _No arguments_  
→ Launches an interactive **menu picker** that lists valid files in the appropriate folder for you to choose from

- `--help`, `--version`, `-v`  
→ Standard metadata and usage flags

💡 All scripts are run from the `src/` directory and use **relative paths** to stay GitHub-safe.