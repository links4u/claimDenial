#!/usr/bin/env python3
"""
ClaimPilot™ Professional PDF Generator using ReportLab

Generates enterprise-grade PDF from DESIGN_DOCUMENT.md
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted
)
from reportlab.lib import colors
from pathlib import Path
import re

def parse_markdown_to_pdf_elements(md_content, styles):
    """Convert markdown content to ReportLab elements."""
    
    elements = []
    lines = md_content.split('\n')
    i = 0
    
    # Track if we're in a code block or table
    in_code_block = False
    code_block_lines = []
    in_table = False
    table_lines = []
    
    while i < len(lines):
        line = lines[i]
        
        # Skip YAML frontmatter or document control
        if line.startswith('---') or line.startswith('**Version**:'):
            i += 1
            continue
        
        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                # End code block
                code_text = '\n'.join(code_block_lines)
                elements.append(Preformatted(code_text, styles['Code']))
                elements.append(Spacer(1, 0.2 * inch))
                in_code_block = False
                code_block_lines = []
            i += 1
            continue
        
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue
        
        # Tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
            i += 1
            # Check if next line is not a table
            if i < len(lines) and '|' not in lines[i]:
                # Process table
                table_element = create_table(table_lines)
                if table_element:
                    elements.append(table_element)
                    elements.append(Spacer(1, 0.2 * inch))
                in_table = False
                table_lines = []
            continue
        
        # Headers
        if line.startswith('# '):
            text = line[2:].strip()
            # Remove anchor links
            text = re.sub(r'\{#.*?\}', '', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Remove links
            elements.append(Spacer(1, 0.3 * inch))
            elements.append(Paragraph(text, styles['Heading1']))
            elements.append(Spacer(1, 0.1 * inch))
        
        elif line.startswith('## '):
            text = line[3:].strip()
            text = re.sub(r'\{#.*?\}', '', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            elements.append(PageBreak())
            elements.append(Paragraph(text, styles['Heading2']))
            elements.append(Spacer(1, 0.1 * inch))
        
        elif line.startswith('### '):
            text = line[4:].strip()
            text = re.sub(r'\{#.*?\}', '', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            elements.append(Spacer(1, 0.15 * inch))
            elements.append(Paragraph(text, styles['Heading3']))
            elements.append(Spacer(1, 0.05 * inch))
        
        elif line.startswith('#### '):
            text = line[5:].strip()
            text = re.sub(r'\{#.*?\}', '', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(text, styles['Heading4']))
        
        # Horizontal rules
        elif line.strip() == '---':
            elements.append(Spacer(1, 0.1 * inch))
        
        # Bullet lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            text = format_inline_markdown(text)
            elements.append(Paragraph(f"• {text}", styles['BodyText']))
        
        # Numbered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            text = format_inline_markdown(text)
            elements.append(Paragraph(text, styles['BodyText']))
        
        # Regular paragraphs
        elif line.strip():
            text = format_inline_markdown(line.strip())
            elements.append(Paragraph(text, styles['BodyText']))
            elements.append(Spacer(1, 0.05 * inch))
        
        # Empty lines
        else:
            if elements and not isinstance(elements[-1], Spacer):
                elements.append(Spacer(1, 0.1 * inch))
        
        i += 1
    
    return elements

def format_inline_markdown(text):
    """Format inline markdown (bold, italic, code)."""
    # Bold
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    # Code
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9">\1</font>', text)
    # Links - just show the text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'<i>\1</i>', text)
    return text

def create_table(table_lines):
    """Create a table from markdown table lines."""
    if not table_lines:
        return None
    
    # Parse table
    rows = []
    for line in table_lines:
        if line.strip().startswith('|---') or line.strip().startswith('|-'):
            continue  # Skip separator line
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)
    
    if not rows:
        return None
    
    # Create table
    table = Table(rows)
    
    # Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ])
    
    table.setStyle(style)
    return table

def generate_pdf():
    """Generate the professional PDF."""
    
    print("🎯 ClaimPilot™ - Generating Professional Design Document PDF...")
    
    project_root = Path(__file__).parent
    md_file = project_root / "docs" / "DESIGN_DOCUMENT.md"
    output_pdf = project_root / "docs" / "ClaimPilot_Design_Document.pdf"
    
    if not md_file.exists():
        print(f"❌ Error: {md_file} not found")
        return False
    
    print(f"📄 Reading {md_file.name}...")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print("📝 Creating PDF document...")
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Customize styles
    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Title'],
        fontSize=36,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.grey,
        spaceAfter=48,
        alignment=TA_CENTER,
    ))
    
    styles.add(ParagraphStyle(
        name='CoverMeta',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        alignment=TA_CENTER,
    ))
    
    styles['Heading1'].fontSize = 24
    styles['Heading1'].textColor = colors.HexColor('#1a1a1a')
    styles['Heading1'].spaceAfter = 12
    styles['Heading1'].fontName = 'Helvetica-Bold'
    
    styles['Heading2'].fontSize = 18
    styles['Heading2'].textColor = colors.HexColor('#1a1a1a')
    styles['Heading2'].spaceAfter = 10
    styles['Heading2'].fontName = 'Helvetica-Bold'
    
    styles['Heading3'].fontSize = 14
    styles['Heading3'].textColor = colors.HexColor('#333333')
    styles['Heading3'].spaceAfter = 8
    styles['Heading3'].fontName = 'Helvetica-Bold'
    
    styles['Heading4'].fontSize = 12
    styles['Heading4'].textColor = colors.HexColor('#555555')
    styles['Heading4'].spaceAfter = 6
    styles['Heading4'].fontName = 'Helvetica-Bold'
    
    styles['BodyText'].fontSize = 11
    styles['BodyText'].alignment = TA_JUSTIFY
    styles['BodyText'].spaceAfter = 6
    
    styles['Code'].fontSize = 9
    styles['Code'].fontName = 'Courier'
    styles['Code'].leftIndent = 20
    styles['Code'].backColor = colors.HexColor('#f5f5f5')
    
    # Build document
    story = []
    
    # Cover page
    print("📋 Building cover page...")
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("ClaimPilot™", styles['CoverTitle']))
    story.append(Paragraph(
        "Agentic AI Platform for Professional Claim Denial Intelligence<br/>System Architecture &amp; Design Review",
        styles['CoverSubtitle']
    ))
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("<b>Version:</b> 1.0", styles['CoverMeta']))
    story.append(Paragraph("<b>Date:</b> February 2026", styles['CoverMeta']))
    story.append(Paragraph("<b>Classification:</b> Internal Technical Documentation", styles['CoverMeta']))
    story.append(Paragraph("<b>Prepared By:</b> Engineering Team", styles['CoverMeta']))
    story.append(PageBreak())
    
    # Content
    print("📝 Converting markdown to PDF elements...")
    content_elements = parse_markdown_to_pdf_elements(md_content, styles)
    story.extend(content_elements)
    
    # Build PDF
    print("🖨️  Rendering PDF (this may take 30-60 seconds)...")
    try:
        doc.build(story)
        
        if output_pdf.exists():
            file_size = output_pdf.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"✅ PDF generated successfully!")
            print(f"📍 Output: {output_pdf}")
            print(f"📦 File size: {file_size_mb:.2f} MB")
            
            return True
        else:
            print("❌ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_pdf()
    exit(0 if success else 1)
