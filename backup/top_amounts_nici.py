import csv

def clean_amount(value):
    """Clean amount string by removing thousand separators and converting to float."""
    value = value.strip()  # Remove any extra spaces
    if value:  # If value is not empty
        return float(value.replace("'", "").replace(",", "."))
    return 0.0  # Return 0 if the value is empty

def get_top_no_key_lines(file_path, keys_to_search, top_n=5):
    no_key_lines = []

    # Open the file using the correct encoding (UTF-8 or ISO-8859-1)
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            # Extract descriptions from columns 12, 13, 14 ('Beschreibung 1-3')
            description_1 = row[12]
            description_2 = row[13]
            description_3 = row[14]

            amount = 0.0

            # Determine the amount: negative in row[18] or positive in row[19]
            if row[18].strip():  # If Belastung is not empty, it's the negative amount
                amount = -clean_amount(row[18])  # Make it negative
            elif row[19].strip():  # If Gutschrift is not empty, use it as the positive amount
                amount = clean_amount(row[19])

            # Check if any of the three descriptions contain any of the keywords
            key_found = False
            for keywords in keys_to_search.values():
                for keyword in keywords:
                    if keyword in description_1 or keyword in description_2 or keyword in description_3:
                        key_found = True
                        break
                if key_found:
                    break

            # If no key was found, add this row to the no_key_lines
            if not key_found:
                no_key_lines.append((f"{description_1} {description_2} {description_3}", amount, row))

    # Sort by amount in descending order and get the top_n
    top_lines = sorted(no_key_lines, key=lambda x: x[1], reverse=True)[:top_n]

    # Return only the CSV rows of the top lines
    return [line[2] for line in top_lines]
