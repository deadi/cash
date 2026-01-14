import csv
from debug import debug_row_processing


def normalize_keys_to_search(keys_to_search):
    # Normalize search terms once so CSV matching can be case-insensitive.
    return {
        group: [(desc, desc.lower()) for desc in descriptions]
        for group, descriptions in keys_to_search.items()
    }


def _normalize_group_terms(keys_to_search, group):
    # Build a normalized list of terms for a specific group key.
    group_terms = keys_to_search.get(group, [])
    return [(term, term.lower()) for term in group_terms]

##################################################

# Adi functions

##################################################

# Return rows whose description contains the provided key (case-insensitive).
def get_lines_for_key_adi(file_path, key):
    matching_rows = []
    key_lower = key.lower()

    # The Adi CSV uses a semicolon delimiter and ISO-8859-1 encoding.
    with open(file_path, mode='r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip header row to align with data rows.

        for row in csv_reader:
            description_lower = row[2].lower()
            if key_lower in description_lower:
                matching_rows.append(row)

    return matching_rows


def get_lines_for_group_adi(file_path, group, keys_to_search):
    # Expand the provided group into its search terms, then match any of them.
    matching_rows = []
    normalized_group_terms = _normalize_group_terms(keys_to_search, group)

    # The Adi CSV uses a semicolon delimiter and ISO-8859-1 encoding.
    with open(file_path, mode='r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip header row to align with data rows.

        for row in csv_reader:
            description_lower = row[2].lower()
            if any(term_lower in description_lower for _, term_lower in normalized_group_terms):
                matching_rows.append(row)

    return matching_rows


# Function to parse and summarize the amounts
def summarize_amounts_adi(file_path, keys_to_search):
    amounts = {}
    group_totals = {}
    normalized_keys = normalize_keys_to_search(keys_to_search)
    
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
            description_lower = description.lower()
            amount = float(row[3])

            # Check if the description contains any of the keys
            key_found = False
            for group, descriptions in normalized_keys.items():
                for desc, desc_lower in descriptions:
                    if desc_lower in description_lower:
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
    normalized_keywords = [
        desc.lower()
        for descriptions in keys_to_search.values()
        for desc in descriptions
    ]

    # Open the file using a forgiving encoding (ISO-8859-1)
    with open(file_path, mode='r', encoding='ISO-8859-1') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            description = row[2]
            description_lower = description.lower()
            amount = float(row[3])

            # Check if the description contains any of the keywords
            if not any(keyword in description_lower for keyword in normalized_keywords):
                no_key_lines.append((description, amount, row))

    # Sort by amount in descending order and get the top_n
    top_lines = sorted(no_key_lines, key=lambda x: x[1], reverse=False)[:top_n]

    # Return only the CSV rows of the top lines
    return [line[2] for line in top_lines]


##################################################

# Nici functions

##################################################

# Return rows whose description1 or description2 contains the key (case-insensitive).
def get_lines_for_key_nici(file_path, key):
    matching_rows = []
    key_lower = key.lower()

    # The Nici CSV uses a semicolon delimiter and UTF-8 encoding.
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip header row to align with data rows.

        for row in csv_reader:
            description_1_lower = row[10].lower()
            description_2_lower = row[11].lower()
            if key_lower in description_1_lower or key_lower in description_2_lower:
                matching_rows.append(row)

    return matching_rows


def get_lines_for_group_nici(file_path, group, keys_to_search):
    # Expand the group key into its terms and match any term in Beschreibung1/2.
    matching_rows = []
    normalized_group_terms = _normalize_group_terms(keys_to_search, group)

    # The Nici CSV uses a semicolon delimiter and UTF-8 encoding.
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip header row to align with data rows.

        for row in csv_reader:
            description_1_lower = row[10].lower()
            description_2_lower = row[11].lower()
            if any(
                term_lower in description_1_lower or term_lower in description_2_lower
                for _, term_lower in normalized_group_terms
            ):
                matching_rows.append(row)

    return matching_rows

def summarize_amounts_nici(file_path, keys_to_search):
    amounts = {}
    group_totals = {}
    normalized_keys = normalize_keys_to_search(keys_to_search)

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
            # 2025 CSV structure indices:
            # 0 Abschlussdatum; 1 Abschlusszeit; 2 Buchungsdatum; 3 Valutadatum; 4 Währung
            # 5 Belastung; 6 Gutschrift; 7 Einzelbetrag; 8 Saldo; 9 Transaktions-Nr.
            # 10 Beschreibung1; 11 Beschreibung2; 12 Beschreibung3; 13 Fussnoten
            description_1 = row[10]
            description_2 = row[11]
            description_1_lower = description_1.lower()
            description_2_lower = description_2.lower()

            # Determine amount using the separated debit/credit fields.
            # Belastung (debit) values are already negative in the CSV.
            belastung = row[5].strip()
            gutschrift = row[6].strip()
            einzelbetrag = row[7].strip()

            if belastung:
                amount = float(belastung)
            elif gutschrift:
                amount = float(gutschrift)
            elif einzelbetrag:
                # Einzelbetrag is used for standalone fees; bucket it as "Bankfee".
                amount = float(einzelbetrag)
                amounts["Bankfee"] += amount
                continue
            else:
                amount = 0.0

            # Check if any of the descriptions contain the keys
            key_found = False
            description = None  # Keep track of which description matched the key
            for group, descriptions in normalized_keys.items():
                for desc, desc_lower in descriptions:
                    if desc_lower in description_1_lower or desc_lower in description_2_lower:
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

def get_top_no_key_lines_nici(file_path, keys_to_search, top_n=5):
    no_key_lines = []
    normalized_keywords = [
        desc.lower()
        for descriptions in keys_to_search.values()
        for desc in descriptions
    ]

    # Open the file using the correct encoding (UTF-8 or ISO-8859-1)
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')

        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            # 2025 CSV structure indices for the descriptions.
            description_1 = row[10]
            description_2 = row[11]
            description_1_lower = description_1.lower()
            description_2_lower = description_2.lower()

            amount = 0.0

            # Use separated debit/credit fields for the amount.
            belastung = row[5].strip()
            gutschrift = row[6].strip()
            einzelbetrag = row[7].strip()

            if belastung:
                amount = float(belastung)
            elif gutschrift:
                amount = float(gutschrift)
            elif einzelbetrag:
                amount = float(einzelbetrag)

            # Check if any of the three descriptions contain any of the keywords
            # Use normalized keywords to keep matching case-insensitive.
            key_found = any(
                keyword in description_1_lower or keyword in description_2_lower
                for keyword in normalized_keywords
            )

            # If no key was found, add this row to the no_key_lines
            if not key_found:
                no_key_lines.append((f"{description_1} {description_2}", amount, row))

    # Sort by amount in descending order and get the top_n
    top_lines = sorted(no_key_lines, key=lambda x: x[1], reverse=True)[:top_n]

    # Return only the CSV rows of the top lines
    return [line[2] for line in top_lines]

##################################################

# CSV export functions

##################################################

# Function to write summary results to CSV
def export_to_csv(output_path, amounts, group_totals, keys_to_search):
    with open(output_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow(['Key', 'Total Amount'])
        for key, total in amounts.items():
            csv_writer.writerow([key, f"{total:.2f}"])
        
        csv_writer.writerow([])
        csv_writer.writerow(['Group', 'Group Total'])
        for group in keys_to_search:
            csv_writer.writerow([group, f"{group_totals[group]:.2f}"])
        
        csv_writer.writerow([])
        csv_writer.writerow(['No Key', f"{amounts.get('no_key', 0.0):.2f}"])
    print(f"Results have been exported to {output_path}")
