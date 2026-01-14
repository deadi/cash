import csv
import argparse
import os
from config_loader import load_config
from data_processing import (
    summarize_amounts_adi,
    summarize_amounts_nici,
    get_lines_for_key_adi,
    get_lines_for_key_nici,
    get_lines_for_group_adi,
    get_lines_for_group_nici,
    get_top_no_key_lines_adi,
    get_top_no_key_lines_nici,
    export_to_csv
)

# Print current working directory and workspace path for reference
print("Current Working Directory:", os.getcwd())
workspace_folder = os.getenv('VSCODE_WORKSPACE_FOLDER', "Not set")
print("Workspace Folder Path:", workspace_folder)

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process CSV files based on JSON config and output to specified path.")
    parser.add_argument('--config', required=True, help="Path to the JSON config file (e.g., adi.json or nici.json)")
    parser.add_argument('--output', required=True, help="Path to the output CSV file")
    parser.add_argument('--list-groups', action='store_true', help="Print the group keys from the config and exit")
    parser.add_argument('--print-group', help="Print the terms for a specific group key and exit")
    parser.add_argument('--find-key', help="Search for a key and print matching CSV rows before summarizing")
    parser.add_argument('--find-group', help="Search for a group key and print all matching CSV rows before summarizing")
    parser.add_argument('--find-limit', type=int, default=50, help="Limit for printed rows when using --find-key")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output for debugging")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    try:
        # Load config and extract relevant data
        config_data = load_config(args.config)
        csv_file_path = config_data["csv"]
        keys_to_search = config_data["keys_to_search"]
        output_csv_path = args.output

        # Exit early if the user only wants to inspect group keys or group contents.
        if args.list_groups:
            for group_key in keys_to_search.keys():
                print(group_key)
            return

        if args.print_group:
            group_terms = keys_to_search.get(args.print_group)
            if not group_terms:
                print(f"Group '{args.print_group}' not found in config.")
            else:
                print(f"{args.print_group}:")
                for term in group_terms:
                    print(f"- {term}")
            return

        # Map config to specific functions
        # Normalize config filename to detect adi/nici configs regardless of case.
        config_type = 'adi' if 'adi.json' in args.config.lower() else 'nici'
        func_map = {
            'adi': (summarize_amounts_adi, get_top_no_key_lines_adi, get_lines_for_key_adi, get_lines_for_group_adi),
            'nici': (summarize_amounts_nici, get_top_no_key_lines_nici, get_lines_for_key_nici, get_lines_for_group_nici)
        }

        summarize_func, top_lines_func, find_lines_func, find_group_func = func_map[config_type]
        print(f"Processing {csv_file_path} with {args.config} (using {config_type.capitalize()} functions)")

        # Optional direct lookup: print rows that match a provided key before summarizing.
        if args.find_key:
            matching_rows = find_lines_func(csv_file_path, args.find_key)
            limited_rows = matching_rows[:args.find_limit]
            print(f"Found {len(matching_rows)} rows for key '{args.find_key}'. Showing {len(limited_rows)}:")
            for row in limited_rows:
                print(row)

        # Optional group lookup: print all rows that match any term in the group before summarizing.
        if args.find_group:
            if args.find_group not in keys_to_search:
                print(f"Group '{args.find_group}' not found in config.")
            else:
                matching_rows = find_group_func(csv_file_path, args.find_group, keys_to_search)
                print(f"Found {len(matching_rows)} rows for group '{args.find_group}'. Showing all results:")
                for row in matching_rows:
                    print(row)

        # Summarize amounts and retrieve top 'no key' lines
        amounts, group_totals = summarize_func(csv_file_path, keys_to_search)
        top_lines = top_lines_func(csv_file_path, keys_to_search, top_n=100)

        # Display top lines if verbose mode is enabled
        if args.verbose:
            print(f"Top {len(top_lines)} 'no key' lines for {csv_file_path}:")
            for line in top_lines:
                truncated_description = line[2][:50] + ('...' if len(line[2]) > 50 else '')
                print([truncated_description] + line[3:])

        # Export results to CSV
        export_to_csv(output_csv_path, amounts, group_totals, keys_to_search)

    except KeyError as e:
        print(f"Error: Missing key in config file: {e}")
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
