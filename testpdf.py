from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(output_filename, test_number, questions):
    # Set up the document
    pdf = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Define styles for different lines in the center cell
    styles = getSampleStyleSheet()
    line1_style = ParagraphStyle('line1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, leading=20)
    line2_style = ParagraphStyle('line2', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1)

    # Paragraph for the center cell with different styles for each line
    center_cell_content = [
        Paragraph("Department of Forensics", line1_style),
        Paragraph("Card for Oral Examination of Board-I", line2_style)
    ]

    # Header Table Data
    header_data = [
        [f"Card No: {test_number}", center_cell_content, "Roll No"]
    ]

    # Create Header Table
    header_table = Table(header_data, colWidths=[100, 300, 100])  # Adjust column widths
    header_table.setStyle(
        TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Left-align the first cell
            ('ALIGN', (2, 0), (2, 0), 'LEFT'),  # Left-align the third (right) cell
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center-align vertically for all cells
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Bold font for the whole row
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Font size for all cells
        ])
    )

    elements.append(header_table)
    elements.append(Spacer(1, 20))  # Add space after header

    # Prepare the main table data
    def wrap_text(content):
        """Converts text with newlines to a Paragraph for wrapping."""
        content = content.replace("\n", "<br />")  # Replace newline with HTML break
        return Paragraph(content, styles["BodyText"])

    data = [
        ["Type", "Questions", "Remarks"],  # Header
        ["Knowledge-based", wrap_text("\n".join([f"{i+1}. {q}" for i, q in enumerate(questions["Knowledge"])])), ""],
        ["Analytical", wrap_text("\n".join([f"{i+1}. {q}" for i, q in enumerate(questions["Analytical"])])), ""],
        ["Problem-based", wrap_text("\n".join([f"{i+1}. {q}" for i, q in enumerate(questions["Problem"])])), ""]
    ]

    # Define table and apply styles
    table = Table(data, colWidths=[100, 300, 100])
    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header text alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
            ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),  # Center align vertically for Type column
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Center align text horizontally in Type column
            ('LEFTPADDING', (1, 1), (-1, -1), 5),  # Add padding for readability
            ('RIGHTPADDING', (1, 1), (-1, -1), 5),
        ])
    )

    # Add the table to the document
    elements.append(table)
    pdf.build(elements)

# Test the function
questions = {
    "Knowledge": [
        "Define forensic medicine.",
        "What is forensic ballistics?",
        "Define consent.",
        "What is euthanasia?",
        "Classify asphyxia."
    ],
    "Analytical": [
        "Differentiate forensic medicine and medical jurisprudence.",
        "Explain objectives of medical records.",
        "Describe the scope of forensic medicine."
    ],
    "Problem": [
        "Calculate intrauterine age from crown-heel length of 16 cm.",
        "A patient requested euthanasia. What type of consent is required?"
    ]
}

create_pdf("Custom_Header_Model_Test_1.pdf", 1, questions)
