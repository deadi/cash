# cash
Python app für Nici und Adi: Bankdaten als CSV werden analysiert und in Gruppen geteilt.

## Source summary
- `src/main.py`: CLI entry point that loads config files, dispatches to Nici/Adi processors, prints verbose output, and exports results.
- `src/data_processing.py`: Core CSV parsing, grouping, and export logic for both Nici and Adi, including no-key reporting helpers.
- `src/config_loader.py`: Loads and validates JSON configuration files containing CSV paths and keys to search.
- `src/utils.py`: Utility helper for cleaning amount strings into floats.
- `src/debug.py`: Debug helper for printing row processing details.
- `src/visualization.py`: Placeholder for future visualization logic (currently empty).

## Project structure
```
.
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
