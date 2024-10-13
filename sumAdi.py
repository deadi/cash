import csv
import json
from top_amounts import get_top_no_key_lines  # Import the function from the other script

#output_csv_path = "/home/adi/docker/windows/data/shared/CashCsv/2024adi.csv"
output_csv_path = "/home/adi/cash/output/2024adi.csv" # Testhilfe


def debug_row_processing(row, description, amount, key_found, group, desc):
    print(f"Row processed: {row}")
    print(f"Description used: {description}")
    print(f"Amount: {amount}")
    print(f"Key found: {key_found}, Group: {group}, Description: {desc}\n")

# Function to load configuration from a JSON file
def load_config(json_path):
    with open(json_path, 'r') as file:
        config = json.load(file)
    return config["keys_to_search"]

# Function to parse and summarize the amounts
def summarize_amounts(file_path, keys_to_search):
    amounts = {}
    group_totals = {}
    
    # Initialize amounts for each key and group
    for group, descriptions in keys_to_search.items():
        for desc in descriptions:
            amounts[desc] = 0
        group_totals[group] = 0

    amounts["no_key"] = 0

    with open(file_path, mode='r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=';')

        # Skip the header row
        next(csv_reader)

        for row in csv_reader:
            # Extract the description and amount
            description = row[2]
            amount = float(row[3])

            # Check if the description contains any of the keys
            key_found = False
            for group, descriptions in keys_to_search.items():
                for desc in descriptions:
                    if desc in description:
                        amounts[desc] += amount
                        group_totals[group] += amount
                        key_found = True
                        break
                if key_found:
                    break

            # If no key was found, add the amount to 'no_key'
            if not key_found:
                amounts["no_key"] += amount

            # Debug row processing
            #debug_row_processing(row, description, amount, key_found, group, description if description else "No description matched")


    # Print the group totals in the order they appear in keys_to_search
    print("\nGroup Totals:")
    for group in keys_to_search:
        print(f"{group}: {group_totals[group]:.2f}")
    
    # Print the total amount for 'no key'
    print(f"No Key: {amounts['no_key']:.2f}")
        
    # Print a clearer separation between file outputs
    print("\n---------------------------------------------\n")
    
    return amounts, group_totals  # Return the amounts and group_totals

def main():
    configs = [
        {"csv": "/home/adi/cash/data/2024-mpk-adi.csv", "json": "/home/adi/cash/config/adi.json"},
    ]

    for config in configs:
        # Load the search keys from the JSON configuration
        keys_to_search = load_config(config["json"])

        # Summarize amounts for the corresponding CSV file and capture the results
        print(f"Processing {config['csv']} with {config['json']}")
        amounts, group_totals = summarize_amounts(config["csv"], keys_to_search)
        print()  # For a clearer separation between outputs

        # Get the top no-key lines and display them (excluding the first element of each row)
        top_lines = get_top_no_key_lines(config["csv"], keys_to_search, top_n=10)
        print(f"Top {len(top_lines)} 'no key' lines for {config['csv']}:")
        for line in top_lines:
            # Print first 50 characters of description, then the rest of the row
            truncated_description = line[2][:50] + ('...' if len(line[2]) > 50 else '')
            print([truncated_description] + line[3:])  # Truncate description and print the rest
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
