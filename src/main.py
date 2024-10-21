import csv
import argparse
from config_loader import load_config
from data_processing import summarize_amounts_adi, get_top_no_key_lines_adi

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process CSV files based on JSON config and output to specified path.")
    
    # Add arguments for the JSON config file and output CSV path
    parser.add_argument('--config', required=True, help="Path to the JSON config file (e.g., adi.json or nici.json)")
    parser.add_argument('--output', required=True, help="Path to the output CSV file")
    
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load the config, which includes both the CSV path and search keys
    config_data = load_config(args.config)
    
    # Extract the CSV file path and search keys from the loaded config
    csv_file_path = config_data["csv"]
    keys_to_search = config_data["keys"]

    # Get the output path from the command-line arguments
    output_csv_path = args.output

    # Summarize amounts for the corresponding CSV file and capture the results
    print(f"Processing {csv_file_path} with {args.config}")
    amounts, group_totals = summarize_amounts_adi(csv_file_path, keys_to_search)
    print()  # For a clearer separation between outputs

    # Get the top no-key lines and display them (excluding the first element of each row)
    top_lines = get_top_no_key_lines_adi(csv_file_path, keys_to_search, top_n=10)
    print(f"Top {len(top_lines)} 'no key' lines for {csv_file_path}:")
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
