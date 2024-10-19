import csv
from debug import debug_row_processing
from utils import clean_amount

##################################################

# Adi functions

##################################################



# Function to parse and summarize the amounts
def summarize_amounts_adi(file_path, keys_to_search):
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


# No Key Lines
def get_top_no_key_lines_adi(file_path, keys_to_search, top_n=5):
    no_key_lines = []

    # Open the file using a forgiving encoding (ISO-8859-1)
    with open(file_path, mode='r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            description = row[2]
            amount = float(row[3])

            # Check if the description contains any of the keywords
            if not any(keyword in description for keywords in keys_to_search.values() for keyword in keywords):
                no_key_lines.append((description, amount, row))

    # Sort by amount in descending order and get the top_n
    top_lines = sorted(no_key_lines, key=lambda x: x[1], reverse=False)[:top_n]

    # Return only the CSV rows of the top lines
    return [line[2] for line in top_lines]


##################################################

# Nici functions

##################################################

def summarize_amounts_nici(file_path, keys_to_search):
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


##################################################

# CSV export functions

##################################################

