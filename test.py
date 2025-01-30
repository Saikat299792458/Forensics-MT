import os

# Initialize dictionaries for question storage
questions = {"Knowledge": [], "Analytical": [], "Problem": []}

# Define the files to process
files = [f"Item{i+1}.txt" for i in range(10)]  # Add your file names here

# Process each file
for file in files:
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
            if "KNOWLEDGE BASED" in line.upper() or "RECALL" in line.upper():
                current_category = "Knowledge"
                continue
            elif "ANALYTICAL" in line.upper():
                current_category = "Analytical"
                continue
            elif "PROBLEM BASED" in line.upper():
                current_category = "Problem"
                continue

            # Process problem-based multiline questions
            if current_category == "Problem":
                if line.startswith("*"):
                    # If a new question starts, save the previous question if it exists
                    if current_question:
                        questions[current_category].append({"file": file, "question": current_question.strip()})
                    # Start a new question
                    current_question = line[1:].strip()
                else:
                    # Append to the current question
                    if current_question is not None:
                        current_question += " " + line.strip()
            else:
                # For other categories, treat each line as a new question
                if current_category:
                    questions[current_category].append({"file": file, "question": line[1:].strip()})

        # Ensure the last multiline question is saved
        if current_category == "Problem" and current_question:
            questions[current_category].append({"file": file, "question": current_question.strip()})

# Print the categorized questions for verification
for category, qs in questions.items():
    print(f"{category} Questions ({len(qs)}):")
    for q in qs[:5]:  # Display the first 5 questions for each category
        print(f"  - {q['question']} (from {q['file']})")
    print()
