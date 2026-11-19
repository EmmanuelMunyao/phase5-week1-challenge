# Sauti ya Nkubu FM Advert Report

A Python command-line tool for processing Sauti ya Nkubu FM's monthly advert log.

The tool:

- Reads an advert CSV file from the command line.
- Validates every advert row.
- Reports invalid rows with their line numbers and reasons.
- Calculates advert prices using the station's rate card.
- Totals spots, seconds and amounts by advertiser.
- Ranks advertisers by total amount.
- Totals revenue by advertising slot.
- Prints a report to the terminal.
- Saves the report as a JSON file in the `reports/` directory.

## Project Setup

Create and activate the virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the requirements:

```powershell
python -m pip install -r requirements.txt
```

## Run the Advert Report

From the `week1-challenge` directory:

```powershell
python .\adreport.py .\data\adlog-2026-11.csv
```

The generated JSON report is saved to:

```text
reports/adlog-2026-11-report.json
```

## Run the Tests

Run the complete test suite with:

```powershell
pytest -q
```

For verbose test output:

```powershell
pytest -v
```

## Project Structure

```text
week1-challenge/
├── adreport.py
├── checks.py
├── summary.py
├── test_checks.py
├── test_summary.py
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── adlog-2026-11.csv
└── reports/
    └── adlog-2026-11-report.json
```

## Sample Result

The supplied November data contains 29 rows:

- 22 accepted spots
- 7 rejected rows
- Total billing: KSh 26,200

The tool reports validation problems such as invalid times, invalid advert lengths, duplicate spot IDs, blank advertisers and invalid dates.