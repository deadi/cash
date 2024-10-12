import csv
import json
from top_amounts_nici import get_top_no_key_lines  # Import the function from the other script
import codecs  # For UTF-8 BOM handling

#output_csv_path = "/home/adi/windows/data/shared/CashCsv/2024nici.csv"
output_csv_path = "/home/adi/cash/output/2024nici.csv"


# Function to load configuration from a JSON file
def load_config(json_path):
    with open(json_path, 'r') as file:
        config = json.load(file)
    return config["keys_to_search"]

def debug_row_processing(row, description, amount, key_found, group, desc):
    print(f"Row processed: {row}")
    print(f"Description used: {description}")
    print(f"Amount: {amount}")
    print(f"Key found: {key_found}, Group: {group}, Description: {desc}\n")

def clean_amount(value):
    """Clean amount string by removing thousand separators and converting to float."""
    value = value.strip()  # Remove any extra spaces
    if value:  # If value is not empty
        return float(value.replace("'", "").replace(",", "."))
    return 0.0  # Return 0 if the value is empty

def summarize_amounts(file_path, keys_to_search):
    amounts = {}
    group_totals = {}

    # Initialize amounts for each key and group
    for group, descriptions in keys_to_search.items():
        for desc in descriptions:
            amounts[desc] = 0
        group_totals[group] = 0

    amounts["no_key"] = 0
    amounts["Bankfee"] = 0

    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        # Skip the header row
        next(csv_reader)

        for row in csv_reader:
            # Extract descriptions from columns 12, 13, 14 ('Beschreibung 1-3')
            description_1 = row[12]
            description_2 = row[13]
            description_3 = row[14]

            # Determine the amount: negative in row[18] or positive in row[19]
            if row[18].strip():  # If row[18] is not empty, it's the negative amount
                amount = -clean_amount(row[18])  # Make it negative
            elif row[19].strip():  # If row[19] is not empty, it's the positive amount
                amount = clean_amount(row[19])
            elif row[17].strip():  # If both row[18] and row[19] are empty, use row[17] for "Bankfee"
                amount = clean_amount(row[17])
                amounts["Bankfee"] += amount  # Add to "Bankfee"
                continue  # Skip further processing for this row
            else:
                amount = 0.0  # No valid amount found

            # Check if any of the descriptions contain the keys
            key_found = False
            description = None  # Keep track of which description matched the key
            for group, descriptions in keys_to_search.items():
                for desc in descriptions:
                    if desc in description_1 or desc in description_2 or desc in description_3:
                        amounts[desc] += amount
                        group_totals[group] += amount
                        key_found = True
                        description = desc  # Record which description was used
                        break
                if key_found:
                    break

            # If no key was found, add the amount to 'no_key'
            if not key_found:
                amounts["no_key"] += amount

            # Debug row processing
            debug_row_processing(row, description, amount, key_found, group, description if description else "No description matched")

    return amounts, group_totals  # Return the amounts and group_totals


def main():
    configs = [
        {"csv": "/home/adi/bo/cash/data/2024-pk-nici.csv", "json": "/home/adi/bo/cash/config/nici.json"}
    ]

    for config in configs:
        # Load the search keys from the JSON configuration
        keys_to_search = load_config(config["json"])

        # Summarize amounts for the corresponding CSV file
        print(f"Processing {config['csv']} with {config['json']}")
        amounts, group_totals = summarize_amounts(config["csv"], keys_to_search)  # Capture returned values
        print()  # For a clearer separation between outputs

        # Get the top no-key lines and display them
        top_lines = get_top_no_key_lines(config["csv"], keys_to_search, top_n=10)
        print(f"Top {len(top_lines)} 'no key' lines for {config['csv']}:")
        for line in top_lines:
            truncated_description = line[13][:50] + ('...' if len(line[13]) > 50 else '')
            print([truncated_description] + line[11:])  # Truncate description and print the rest
        print()  # Separation between file results

        # Export results to CSV with UTF-8 encoding
        with open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')  # Use semicolon as delimiter
            
            # Write header for key totals
            csv_writer.writerow(['Key', 'Total Amount'])

            # Write the results for each key
            for key, total in amounts.items():
                csv_writer.writerow([key, f"{total:.2f}"])

            # Write group totals header
            csv_writer.writerow([])
            csv_writer.writerow(['Group', 'Group Total'])

            # Write group totals
            for group in keys_to_search:
                csv_writer.writerow([group, f"{group_totals[group]:.2f}"])

            # Write the total amount for 'no_key'
            csv_writer.writerow([])
            csv_writer.writerow(['No Key', f"{amounts['no_key']:.2f}"])

        print(f"Results have been exported to {output_csv_path}")

# Run the main function
if __name__ == "__main__":
    main()