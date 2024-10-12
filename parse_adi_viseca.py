import pdfplumber
import re
import os
from collections import defaultdict

# Function to extract and filter relevant text from the PDF
def extract_relevant_text(pdf_path):
    relevant_text = []
    capture = False  # Flag to start capturing text

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                if "Kartenlimite CHF" in line:
                    capture = True  # Start capturing after this line
                elif "Total Karte Visa Classic" in line:
                    capture = False  # Stop capturing after this line
                elif capture:
                    relevant_text.append(line)
    
    # Debug: print the extracted relevant text
    print(f"Extracted text from {pdf_path}:\n", "\n".join(relevant_text), "\n")
    return "\n".join(relevant_text)

# Function to parse descriptions and amounts using regex
def parse_credit_card_transactions(text):
    # Modify this regex based on the structure of your data
    transaction_pattern = re.compile(
        r"(\d{2}\.\d{2}\.\d{2})\s+(\d{2}\.\d{2}\.\d{2})\s+([A-Za-z0-9,.() ]+)\s+([0-9]*[.,]?[0-9]+)"
    )

    transactions = []

    for line in text.split('\n'):
        match = transaction_pattern.search(line)
        if match:
            date_from = match.group(1)
            date_to = match.group(2)
            description = match.group(3).strip()
            amount = match.group(4).replace(',', '.')

            # Debug: print matched transaction info
            print(f"Matched transaction -> Date From: {date_from}, Date To: {date_to}, Description: {description}, Amount: {amount}")
            
            transactions.append((date_from, date_to, description, float(amount)))
        else:
            # Debug: print lines that didn't match the regex
            print(f"Line didn't match regex: {line}")
    
    return transactions

# Function to process all PDFs in a directory and sum amounts by description
def process_pdfs_and_sum_by_description(pdf_directory):
    description_sums = defaultdict(float)  # Dictionary to sum amounts for each description
    total_sum = 0  # Variable to track the overall total sum

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(pdf_directory, filename)
            print(f"Processing {pdf_path}...")
            
            # Extract relevant text and parse the transactions
            relevant_text = extract_relevant_text(pdf_path)
            transactions = parse_credit_card_transactions(relevant_text)
            
            file_sum = 0  # Sum for the current file

            # Sum amounts by description and also calculate total for the current file
            for transaction in transactions:
                description = transaction[2]
                amount = transaction[3]
                description_sums[description] += amount
                file_sum += amount

            # Debug: print the sum for the current file
            print(f"Sum for {filename}: {file_sum:.2f}")

            # Add the file sum to the overall total sum
            total_sum += file_sum

    # Debug: print total sum
    print(f"Total sum after processing all files: {total_sum:.2f}")
    return description_sums, total_sum

# Path to your PDF directory
pdf_directory = '/home/adi/cash/data/viseca/2024/adi/'

# Process all PDFs and sum amounts by description
description_sums, total_sum = process_pdfs_and_sum_by_description(pdf_directory)

# Sort the description_sums dictionary by amount in descending order
sorted_description_sums = sorted(description_sums.items(), key=lambda x: x[1], reverse=True)

# Print the sorted sums
print("Summed amounts by description (sorted by total amount DESC):")
for description, total_amount in sorted_description_sums:
    print(f"Description: {description}, Total Amount: {total_amount:.2f}")

# Print the total sum of all transactions
print(f"\nTotal sum of all transactions: {total_sum:.2f}")
