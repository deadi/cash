import csv

def get_top_no_key_lines(file_path, keys_to_search, top_n=5):
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
