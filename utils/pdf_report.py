# utils/pdf_report.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(output_file="output/sales_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_file)

    content = []

    content.append(Paragraph("Sales Analytics Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Dashboard Overview", styles['Heading2']))
    content.append(Spacer(1, 10))

    # Add dashboard image
    try:
        img = Image("output/dashboard.png", width=500, height=300)
        content.append(img)
    except:
        content.append(Paragraph("Dashboard image not found", styles['Normal']))

    doc.build(content)

    print("✅ PDF created:", output_file)