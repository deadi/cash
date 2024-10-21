#import json

# Function to load configuration from a JSON file
""" def load_config(json_path):
    with open(json_path, 'r') as file:
        config = json.load(file)
    return config["keys_to_search"] """

import json
import os

def load_config(json_path):
    """Load configuration from a JSON file."""
    
    # Check if the file exists
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"Configuration file '{json_path}' not found.")
    
    with open(json_path, 'r', encoding='utf-8') as file:
        try:
            config = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from config file: {e}")

    # Ensure the necessary keys exist
    if "csv" not in config:
        raise KeyError("Missing required key 'csv' in the config file.")
    if "keys_to_search" not in config:
        raise KeyError("Missing required key 'keys_to_search' in the config file.")

    return config  # Return the complete configuration object
