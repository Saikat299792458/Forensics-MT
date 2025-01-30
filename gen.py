import os
import random
import re
#from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

elements = []
pdf = SimpleDocTemplate("Questions/Cards.pdf", pagesize=A4)
cards = 100

def create_pdf(questions):
    # Set up the document
    styles = getSampleStyleSheet()

    # Define styles for different lines in the center cell
    styles = getSampleStyleSheet()
    line1_style = ParagraphStyle('line1', parent=styles['Normal'], fontName='Times-Bold', fontSize=16, alignment=1, leading=25)
    line2_style = ParagraphStyle('line2', parent=styles['Normal'], fontName='Times-Roman', fontSize=14, alignment=1, leading=20)

    # Paragraph for the center cell with different styles for each line
    center_cell_content = [
        Paragraph("Structured Oral Examination - SOE", line1_style),
        Paragraph("2<sup>nd</sup> Professional MBBS Final", line2_style),
        Paragraph("Total Marks - 50, Each question carries equal mark (05)", line2_style),
        Paragraph("Total time - 15 minutes", line2_style),
    ]

    # Create Header Table
    header_table = Table([[center_cell_content]])  # Adjust column widths
    header_table.setStyle(
        TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Left-align
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # Center-align vertically
            #('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Bold font for the whole row
            ('FONTSIZE', (0, 0), (-1, -1), 14),  # Font size for all cells
        ])
    )

    elements.append(header_table)
    elements.append(Spacer(1, 20))  # Add space after header

    # Prepare the main table data
    def wrap_text(content, font_size=13):
        """Converts text with newlines to a Paragraph for wrapping."""
        # Create a custom paragraph style for consistent font size
        paragraph_style = styles["BodyText"].clone('custom')
        paragraph_style.fontSize = font_size  # Match the table's font size
        paragraph_style.fontName = "Times-Roman"  # Use Times New Roman
        paragraph_style.leading = font_size + 2  # Adjust leading for readability
        content = content.replace("\n", "<br />")  # Replace newline with HTML break
        return Paragraph(content, paragraph_style)


    # Prepare the table data dynamically
    data = [["Type", "Questions"]]  # Header row

    # Updated rows with font size 14
    knowledge_rows = [["Knowledge-based", wrap_text(f'{i+1}. ' + q["question"], font_size=14)] for i, q in enumerate(questions["Knowledge"])]
    analytical_rows = [["Analytical", wrap_text(f'{i+1}. ' + q["question"], font_size=14)] for i, q in enumerate(questions["Analytical"])]
    problem_rows = [["Problem-based", wrap_text(f'{i+1}. ' + q["question"], font_size=14)] for i, q in enumerate(questions["Problem"])]


    # Combine all rows
    data.extend(knowledge_rows + analytical_rows + problem_rows)

    # Create the table
    questions_table = Table(data, colWidths=[130, 370])

    # Define the table style with merged cells
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header text alignment
        ('ALIGN', (1, 1), (0, -1), 'LEFT'),  # Left-align all cells
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),  # Set font
        ('FONTSIZE', (0, 0), (-1, -1), 15),  # Set font size
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Top-align all cells
        ('LEFTPADDING', (1, 1), (-1, -1), 5),  # Add padding for readability
        ('RIGHTPADDING', (1, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('SPAN', (0, 1), (0, len(questions["Knowledge"]))),  # Merge "Knowledge-based" rows
        ('SPAN', (0, len(questions["Knowledge"]) + 1), (0, len(questions["Knowledge"]) + len(questions["Analytical"]))),  # Merge "Analytical" rows
        ('SPAN', (0, len(questions["Knowledge"]) + len(questions["Analytical"]) + 1), (0, len(data) - 1)),  # Merge "Problem-based" rows
    ])

    # Apply the style
    questions_table.setStyle(table_style)


    # Add the table to the document
    elements.append(questions_table)
    elements.append(PageBreak())

# Step 1: Read the Files
# Initialize dictionaries for question storage
questions = {"Knowledge": [], "Analytical": [], "Problem": []}

# Define the files to process
files = [f"Items/Item{i+1}.txt" for i in range(10)]  # Add your file names here

# Process each file
for file in files:
    k,a,p = 0,0,0
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

        current_category = None
        current_question = None

        for line in lines:
            line = line.strip()  # Remove leading/trailing spaces

            # Skip empty lines
            if not line:
                continue

            # Detect headings to set category
            if line.upper().strip().startswith("KNOWLEDGE BASED") or line.upper().strip().startswith("RECALL"):
                current_category = "Knowledge"
                continue
            elif line.upper().strip().startswith("ANALYTICAL"):
                current_category = "Analytical"
                continue
            elif line.upper().strip().startswith("PROBLEM BASED"):
                current_category = "Problem"
                continue

            # Process problem-based multiline questions
            if current_category == "Problem":
                if line.startswith("*"):
                    p = p+1
                    # If a new question starts, save the previous question if it exists
                    if current_question:
                        questions[current_category].append({"file": file, "question": current_question.strip()})
                    # Start a new question
                    current_question = line[1:].strip()
                else:
                    # Append to the current question
                    if current_question is not None:
                        current_question += "\n" + line.strip()
            else:
                # For other categories, treat each line as a new question
                if current_category:
                    if current_category == "Analytical":
                        a = a+1
                    elif current_category == "Knowledge":
                        k = k+1
                    cleaned_line = re.sub(r'^[^a-zA-Z]+', '', line)
                    questions[current_category].append({"file": file, "question": cleaned_line.strip()})

        # Ensure the last multiline question is saved
        if current_category == "Problem" and current_question:
            questions[current_category].append({"file": file, "question": current_question.strip()})
    print(file, k, a, p)


# Step 2: Create model tests
for i in range(cards):
    selected_questions = {"Knowledge": [], "Analytical": [], "Problem": []}
    used_files = []

    for category, count in [("Knowledge", 5), ("Analytical", 3), ("Problem", 2)]:
        available = [q for q in questions[category]]
        random.shuffle(available)
        ind = 0
        for j in range(count):
            while True:
                test = available[ind]
                if test['file'] not in used_files:
                    selected_questions[category].append(test)
                    used_files.append(test['file'])
                    break
                ind = ind+1
    # Append current questions to a page in pdf
    print(f"\rCreating pdf: {i+1}/{cards}", end="")
    create_pdf(selected_questions)

pdf.build(elements)
print(f"\nCreated Questions/Cards.pdf!")
