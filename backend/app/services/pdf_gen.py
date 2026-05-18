# backend/app/services/pdf_gen.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_audit_pdf(company_name: str, insights: dict, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")
    SECONDARY_COLOR = colors.HexColor("#2B6CB0")
    TEXT_COLOR = colors.HexColor("#2D3748")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=24, textColor=PRIMARY_COLOR, spaceAfter=15)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=12, textColor=SECONDARY_COLOR, spaceAfter=20)
    h2_style = ParagraphStyle('SectionH2', parent=styles['Heading2'], fontSize=14, textColor=PRIMARY_COLOR, spaceBefore=12, spaceAfter=8)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=10, textColor=TEXT_COLOR, spaceAfter=6)
    bullet_style = ParagraphStyle('BulletCustom', parent=styles['Normal'], fontSize=10, textColor=TEXT_COLOR, leftIndent=12, spaceAfter=4)

    story = [
        Paragraph("STRATEGIC BUSINESS BRIEFING", title_style),
        Paragraph(f"Prepared Exclusively for: <b>{company_name}</b>", subtitle_style),
        Spacer(1, 10),
        Paragraph("Executive Focus & Market Position", h2_style),
        Paragraph(f"<b>Core Vertical/Domain:</b> {insights.get('domain')}", body_style),
        Paragraph(f"<b>Identified Value Proposition:</b> {insights.get('value_proposition')}", body_style),
        Spacer(1, 10),
        Paragraph("Key Strategic Vulnerabilities & Bottlenecks", h2_style)
    ]
    
    for bottleneck in insights.get('growth_bottlenecks', []):
        story.append(Paragraph(f"• {bottleneck}", bullet_style))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Targeted Actionable Recommendations", h2_style))
    for rec in insights.get('actionable_recommendations', []):
        story.append(Paragraph(f"▪ {rec}", bullet_style))
        
    story.append(Spacer(1, 20))
    t = Table([["Confidential audit prepared by SimplifIQ Automation Engine."]], colWidths=[500])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#718096")),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    doc.build(story)