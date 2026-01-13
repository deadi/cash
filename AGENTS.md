1. Summarize /src files and update README.md
2. Update Project Structure in README.md in Tree view.
3. Explain code in comments
4. focus on def summarize_amounts_nici(file_path, keys_to_search):
- help me implement the new csv structure of the bank data since it changed.
- Belastung;Gutschrift;Einzelbetrag; is new seperately provided, so there is no need to check if its positive or negative amount
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

2024 old csv structure
Bewertungsdatum;Bankbeziehung;Portfolio;Produkt;IBAN;Whrg.;Datum von;Datum bis;Beschreibung;Abschluss;Buchungsdatum;Valuta;Beschreibung 1;Beschreibung 2;Beschreibung 3;Transaktions-Nr.;Devisenkurs zum Originalbetrag in Abrechnungswährung;Einzelbetrag;Belastung;Gutschrift;Saldo

2025 new csv structure
Abschlussdatum;Abschlusszeit;Buchungsdatum;Valutadatum;Währung;Belastung;Gutschrift;Einzelbetrag;Saldo;Transaktions-Nr.;Beschreibung1;Beschreibung2;Beschreibung3;Fussnoten;

5. also adjust the indexes according to the new structure for function
def get_top_no_key_lines_nici(file_path, keys_to_search, top_n=5):
- again,  Belastung;Gutschrift;Einzelbetrag; is new seperately provided, so there is no need to check if its positive or negative amount


