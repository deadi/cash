import csv
from config_loader import load_config
from data_processing import summarize_amounts_adi, get_top_no_key_lines_adi

#output_csv_path = "/home/adi/docker/windows/data/shared/CashCsv/2024adi.csv"
output_csv_path = "/home/adi/cash/output/2024adi.csv" # Testhilfe

def main():
    configs = [
        {"csv": "/home/adi/cash/data/2024-mpk-adi.csv", "json": "/home/adi/cash/config/adi.json"},
    ]

    for config in configs:
        # Load the search keys from the JSON configuration
        keys_to_search = load_config(config["json"])

        # Summarize amounts for the corresponding CSV file and capture the results
        print(f"Processing {config['csv']} with {config['json']}")
        amounts, group_totals = summarize_amounts_adi(config["csv"], keys_to_search)
        print()  # For a clearer separation between outputs

        # Get the top no-key lines and display them (excluding the first element of each row)
        top_lines = get_top_no_key_lines_adi(config["csv"], keys_to_search, top_n=10)
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