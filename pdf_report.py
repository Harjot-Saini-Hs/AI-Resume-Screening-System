from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(name, email, phone, score, matched, missing, recommendation, suggestions):

    pdf = SimpleDocTemplate("report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AI Resume Screening Report</b>", styles['Title']))
    elements.append(Paragraph(f"Candidate Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Email: {email}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {phone}", styles['Normal']))
    elements.append(Paragraph(f"Resume Score: {score}%", styles['Normal']))
    elements.append(Paragraph(f"Recommendation: {recommendation}", styles['Normal']))

    elements.append(Paragraph("<b>Matched Skills</b>", styles['Heading2']))
    for skill in matched:
        elements.append(Paragraph(skill, styles['Normal']))

    elements.append(Paragraph("<b>Missing Skills</b>", styles['Heading2']))
    for skill in missing:
        elements.append(Paragraph(skill, styles['Normal']))

    elements.append(Paragraph("<b>AI Suggestions</b>", styles['Heading2']))
    for suggestion in suggestions:
        elements.append(Paragraph(suggestion, styles['Normal']))

    pdf.build(elements)