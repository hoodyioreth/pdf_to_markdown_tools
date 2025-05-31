#!/bin/bash
# create_project_structure_mac.sh
# Purpose: Sets up the folder structure for the PDF → Markdown project
# Version: 1.0.0

echo "📁 Creating folder structure for PDF → Markdown project..."

mkdir -p pdf-to-md-project/src
mkdir -p pdf-to-md-project/data/input_pdfs
mkdir -p pdf-to-md-project/data/extracted_text
mkdir -p pdf-to-md-project/docs/examples

touch pdf-to-md-project/README.md
touch pdf-to-md-project/requirements.txt

echo "✅ Folder structure created successfully."
