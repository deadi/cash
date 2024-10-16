import json

# Function to load configuration from a JSON file
def load_config(json_path):
    with open(json_path, 'r') as file:
        config = json.load(file)
    return config["keys_to_search"]