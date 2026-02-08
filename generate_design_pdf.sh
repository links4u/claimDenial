#!/bin/bash

# ClaimPilot™ PDF Generation Script
# Converts DESIGN_DOCUMENT.md to professional PDF

echo "🎯 ClaimPilot™ - Generating Design Document PDF..."

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc not found!"
    echo ""
    echo "📥 Install Pandoc:"
    echo "  macOS:   brew install pandoc basictex"
    echo "  Ubuntu:  sudo apt-get install pandoc texlive-xetex"
    echo "  Windows: choco install pandoc miktex"
    echo ""
    echo "Or use alternative:"
    echo "  1. Open DESIGN_DOCUMENT.md in VS Code"
    echo "  2. Install 'Markdown PDF' extension"
    echo "  3. Right-click → Markdown PDF: Export (pdf)"
    exit 1
fi

# Check for LaTeX (required by pandoc)
if ! command -v xelatex &> /dev/null; then
    echo "⚠️  LaTeX not found. Installing BasicTeX..."
    echo "  macOS: brew install basictex"
    echo "  Then run: sudo tlmgr update --self && sudo tlmgr install collection-fontsrecommended"
    exit 1
fi

# Convert to PDF
echo "📄 Converting DESIGN_DOCUMENT.md to PDF..."

pandoc docs/DESIGN_DOCUMENT.md \
    -o docs/ClaimPilot_Design_Document.pdf \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V documentclass=report \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -V toccolor=black \
    --metadata title="ClaimPilot™ Design Document" \
    --metadata subtitle="Agentic AI Platform for Professional Claim Denial Intelligence" \
    --metadata author="Engineering Team" \
    --metadata date="February 2026" \
    --highlight-style=tango

if [ $? -eq 0 ]; then
    echo "✅ PDF generated successfully!"
    echo "📍 Output: docs/ClaimPilot_Design_Document.pdf"
    
    # Get file size
    SIZE=$(du -h docs/ClaimPilot_Design_Document.pdf | cut -f1)
    echo "📦 File size: $SIZE"
    
    # Open PDF (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open docs/ClaimPilot_Design_Document.pdf
    fi
else
    echo "❌ PDF generation failed"
    echo "💡 Alternative: Use online converter at https://www.markdowntopdf.com/"
    echo "   Upload: docs/DESIGN_DOCUMENT.md"
    exit 1
fi
