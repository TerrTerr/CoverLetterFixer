
import os
from fpdf import FPDF

def replace_problematic_chars(text):
    """Replace characters that can cause issues with fpdf."""
    replacements = {
        '’': "'",
        '“': '"',
        '”': '"',
        '–': '-',
        '—': '-',
        '…': '...',
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    print(text)  # In terminal copy, printed version of letter in terminal
    return text

def pattern_search(text, pattern, replacement, case_sensitive=True):
    fixed_text = ""
    num_skips = 0
    count = 0

    for index in range(len(text)):
        if num_skips > 0:
            num_skips -= 1
            continue

        if case_sensitive:
            match = text[index: index + len(pattern)] == pattern
        else:
            match = text[index: index + len(pattern)].lower() == pattern.lower()

        if match:
            count += 1
            fixed_text += replacement  # append the replacement instead of the pattern
            num_skips = len(pattern) - 1  # set the number of characters to skip
        else:
            fixed_text += text[index]  # append the current character to fixed_text

    return fixed_text

def save_to_pdf(text, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    line_height = 6
    pdf.multi_cell(0, line_height, text)
    desktop_path = os.path.expanduser("~/Desktop/")
    pdf_name = new_company + "Cover.pdf"
    pdf_path = os.path.join(desktop_path, pdf_name)
    pdf.output(pdf_path)

# Read original content
file_name = "A.txt"
with open(file_name, 'r') as file:
    original_content = file.read()

# Get input from the user
new_company = input("Enter the new company name: ")
new_position = input("Enter the new position name: ")
new_date = input("Enter the new date: ")

# Ask the user which letter they want to modify
print("Which letter would you like to modify?")
print("1: A.txt")
print("2: B.txt")
print("3: C.txt")
choice = input("Enter 1, 2 or 3: ")

if choice == "1":
    file_name = "A.txt"
elif choice == "2":
    file_name = "B.txt"
elif choice == "3":
    file_name = "C.txt"
else:
    print("Invalid choice. Exiting program.")
    exit()

# Read the chosen file content
with open(file_name, 'r') as file:
    original_content = file.read()

# Replace placeholders with user input
content_with_company = pattern_search(original_content, "Company", new_company)
content_with_position = pattern_search(content_with_company, "Position", new_position)
final_content = pattern_search(content_with_position, "Date", new_date)

# Save modified content to PDF
final_content = replace_problematic_chars(final_content)
pdf_name = new_company + "Cover.pdf"
save_to_pdf(final_content, pdf_name)

# Restore original content
with open(file_name, 'w') as file:
    file.write(original_content)

print("PDF generated and original file restored.")

