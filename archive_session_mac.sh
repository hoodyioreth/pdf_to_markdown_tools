#!/bin/bash
# archive_session_mac.sh
# Purpose: Archive key project files for ChatGPT session continuity

echo "📦 Archiving core project files..."

# Define output archive names
CORE_ARCHIVE="session_core_backup.zip"
BOTH_ARCHIVE="session_both_backup.zip"
FULL_ARCHIVE="session_full_backup.zip"

# Paths
ROOT="$(pwd)"
SRC="src"
DOCS="docs"
CONVERTED_MD="data/converted_md"

# Core only: src
zip -r "$CORE_ARCHIVE" "$SRC" -x "*.DS_Store" > /dev/null
echo "✅ Created $CORE_ARCHIVE (includes src/)"

# Core backup: src + docs
zip -r "$BOTH_ARCHIVE" "$SRC" "$DOCS" -x "*.DS_Store" > /dev/null
echo "✅ Created $BOTH_ARCHIVE (includes src/ and docs/)"

# Full backup: src + docs + converted_md
if [ -d "$CONVERTED_MD" ]; then
  zip -r "$FULL_ARCHIVE" "$SRC" "$DOCS" "$CONVERTED_MD" -x "*.DS_Store" > /dev/null
  echo "✅ Created $FULL_ARCHIVE (includes src/, docs/, and data/converted_md/)"
else
  echo "⚠️  Skipped $FULL_ARCHIVE — $CONVERTED_MD not found"
fi

echo "🧾 Backup complete. Files ready for ChatGPT reinitialization."
