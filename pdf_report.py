from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf(report, output_path="clinical_report.pdf"):

    doc = SimpleDocTemplate(output_path)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("<b>Cancer Variant Interpretation Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Total Variants: {report['total_variants']}", styles["Normal"]))
    elements.append(Paragraph(f"Prioritized Variants: {report['prioritized_variants']}", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    for v in report["findings"]:
        elements.append(Paragraph(f"<b>Gene:</b> {v['gene']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Classification:</b> {v['acmg_classification']}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return output_path
