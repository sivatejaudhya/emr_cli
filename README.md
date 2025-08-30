# Lightweight EMR CLI

A simple command-line tool to manage patient records using CSV files. Ideal for quick data entry, retrieval, updates, and export of patient information.

---

## Features

- Add new patients (demographics, medications, appointments, notes)
- List patients with optional limits
- Search patients by name or phone number
- Update patient records by ID
- Delete patient records by ID
- Export data to JSON
- Show basic statistics (total patients, average age)
- Operation logs in `emr.log`

---

## Tech Stack

- **Python 3**
- **CSV** for data storage
- **JSON** for export
- **Logging** for audit trails
- **Unittest** for testing

---

## Setup

1. Clone the repository:

```bash
git clone <your-github-repo-url>
cd emr-cli


python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt


2. Usage:

python emr_cli.py <command> [options]

Examples:

python emr_cli.py add --name "John Doe" --age 30 --gender M --phone "1234567890" --meds "Paracetamol" --appointments "2025-09-01" --notes "First visit"

python emr_cli.py list --limit 10

python emr_cli.py search --name "John"

python emr_cli.py update --id 1 --phone "9876543210" --notes "Follow-up scheduled"

python emr_cli.py delete --id 1

python emr_cli.py export --out patients.json

python emr_cli.py stats


3. Tests:

python -m unittest tests_emr.py


4. Folder Structure:

emr-cli/
│
├── emr_cli.py           # Main CLI application
├── patients.csv         # CSV database (auto-generated)
├── emr.log              # Log file
├── tests_emr.py         # Unit tests
├── README.md            # Project documentation
└── .gitignore           # Ignore CSV, logs, and env
```
