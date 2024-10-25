import csv
import json

def clean_amount(value):
    """Clean amount string by removing thousand separators and converting to float."""
    value = value.strip()  # Remove any extra spaces
    if value:  # If value is not empty
        return float(value.replace("'", "").replace(",", "."))
    return 0.0  # Return 0 if the value is empty

def debug_no_key_lines(file_path, keys_to_search):
    """Print all lines that are categorized as 'no_key'."""
    no_key_lines = []

    # Open the file using the correct encoding (UTF-8 or ISO-8859-1)
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        headers = next(csv_reader)  # Skip the header row
        print("Headers:", headers)

        for row in csv_reader:
            description_1 = row[12]  # 'Beschreibung 1'
            description_2 = row[13]  # 'Beschreibung 2'
            description_3 = row[14]  # 'Beschreibung 3'
            description = f"{description_1} {description_2} {description_3}"
            
            # Determine the amount: negative in row[18] or positive in row[19]
            if row[18].strip():  # If Belastung is not empty, it's a negative amount
                amount = -clean_amount(row[18])
            elif row[19].strip():  # If Gutschrift is not empty, it's a positive amount
                amount = clean_amount(row[19])
            elif row[20].strip():  # If both are empty, but row[20] has a value
                amount = clean_amount(row[20])
            else:
                amount = 0.0  # No amount found

            # Check if the description contains any of the keywords
            if not any(keyword in description for keywords in keys_to_search.values() for keyword in keywords):
                no_key_lines.append((description, amount, row))
    
    # Print lines categorized as 'no_key'
    print("\nLines categorized as 'no_key':")
    for desc, amt, row in no_key_lines:
        print(f"Description: {desc}, Amount: {amt:.2f}, Row: {row}")

# Example usage
if __name__ == "__main__":
    file_path = '/home/adi/cash/data/2023-pk-nici.csv'
    config_path = '/home/adi/cash/config/nici.json'
    
    # Load JSON config
    with open(config_path, 'r') as file:
        config = json.load(file)
    keys_to_search = config["keys_to_search"]
    
    # Run the debug function to print 'no_key' lines
    debug_no_key_lines(file_path, keys_to_search)
