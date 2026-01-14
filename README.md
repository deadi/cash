# cash
Python app für Nici und Adi: Bankdaten als CSV werden analysiert und in Gruppen geteilt.
Search terms from JSON configs are matched case-insensitively in CSV descriptions.

1. Csv Structure for Nici:
`Abschlussdatum;Abschlusszeit;Buchungsdatum;Valutadatum;Währung;Belastung;Gutschrift;Einzelbetrag;Saldo;Transaktions-Nr.;Beschreibung1;Beschreibung2;Beschreibung3;Fussnoten;`

2. Csv Structure for Adi:
`IBAN;Booked At;Text;Credit/Debit Amount;Balance;Valuta Date`


## Source summary
- `src/main.py`: CLI entry point that loads config files, dispatches to Nici/Adi processors, prints verbose output, supports key/group lookups, and exports results.
- `src/data_processing.py`: Core CSV parsing, grouping, and export logic for both Nici and Adi, including case-insensitive keyword matching, no-key reporting helpers, and key/group-based row lookups.
- `src/config_loader.py`: Loads and validates JSON configuration files containing CSV paths and keys to search.
- `src/utils.py`: Utility helper for cleaning amount strings into floats.
- `src/debug.py`: Debug helper for printing row processing details.
- `src/visualization.py`: Placeholder for future visualization logic (currently empty).

## Usage
```
python src/main.py --config config/adi.json --output out.csv
```

List group keys from a config file:
```
python src/main.py --config config/adi.json --output out.csv --list-groups
```

Print the terms for a single group key (example: Entertainment):
```
python src/main.py --config config/adi.json --output out.csv --print-group "Entertainment"
```

To query rows that contain a key directly (Adi matches `Text`, Nici matches `Beschreibung1/2`):
```
python src/main.py --config config/adi.json --output out.csv --find-key "rent" --find-limit 20
```

To query rows that match any term in a config group (Adi matches `Text`, Nici matches `Beschreibung1/2`):
```
python src/main.py --config config/adi.json --output out.csv --find-group "Entertainment"
```

## Project structure
```
.
├── .gitignore
├── AGENTS.md
├── README.md
├── requirements.txt
├── src
│   ├── config_loader.py
│   ├── data_processing.py
│   ├── debug.py
│   ├── main.py
│   ├── utils.py
│   └── visualization.py
└── todo
```
