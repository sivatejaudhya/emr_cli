#!/usr/bin/env python3
"""Lightweight EMR CLI: manage patient records using CSV."""

import argparse
import csv
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional

CSV_FILE = os.path.join(os.path.dirname(__file__), "patients.csv")
LOG_FILE = os.path.join(os.path.dirname(__file__), "emr.log")
FIELDNAMES = [
    "id",
    "name",
    "age",
    "gender",
    "phone",
    "meds",
    "appointments",
    "notes",
    "created_at",
    "updated_at",
]

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def ensure_csv() -> None:
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all() -> List[Dict[str, str]]:
    """Read all patient records from CSV."""
    ensure_csv()
    with open(CSV_FILE, newline="", encoding="utf-8") as file_handle:
        return list(csv.DictReader(file_handle))


def write_all(rows: List[Dict[str, str]]) -> None:
    """Write all patient records to CSV."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def next_id(rows: List[Dict[str, str]]) -> str:
    """Compute the next patient ID."""
    if not rows:
        return "1"
    ids = [int(row["id"]) for row in rows if row["id"].isdigit()]
    return str(max(ids) + 1)


def add_patient(args: argparse.Namespace) -> None:
    """Add a new patient record."""
    rows = read_all()
    patient_id = next_id(rows)
    now = datetime.utcnow().isoformat()
    record: Dict[str, str] = {
        "id": patient_id,
        "name": args.name.strip(),
        "age": str(args.age) if args.age else "",
        "gender": args.gender or "",
        "phone": args.phone or "",
        "meds": args.meds or "",
        "appointments": args.appointments or "",
        "notes": args.notes or "",
        "created_at": now,
        "updated_at": now,
    }
    rows.append(record)
    write_all(rows)
    logging.info("ADD id=%s name=%s", patient_id, args.name)
    print(f"Added patient id={patient_id} name={args.name}")


def list_patients(args: argparse.Namespace) -> None:
    """List patient records with optional limit."""
    rows = read_all()
    rows_sorted = sorted(rows, key=lambda row: int(row["id"]))
    limit = args.limit or 100
    for row in rows_sorted[:limit]:
        print(
            f'{row["id"]:>3} | {row["name"][:25]:25} | '
            f'age:{row["age"] or "-":>3} | phone:{row["phone"] or "-"}'
        )


def search_patients(args: argparse.Namespace) -> None:
    """Search patients by name or phone."""
    query = (args.name or "").lower()
    rows = read_all()
    results = [
        row
        for row in rows
        if query in row["name"].lower() or query in row.get("phone", "")
    ]
    if not results:
        print("No matching patients found.")
        return
    for row in results:
        print(f'[{row["id"]}] {row["name"]} | age:{row["age"]} | phone:{row["phone"]}')


def update_patient(args: argparse.Namespace) -> None:
    """Update patient record by ID."""
    rows = read_all()
    updated = False
    for row in rows:
        if row["id"] == str(args.id):
            if args.name:
                row["name"] = args.name
            if args.age is not None:
                row["age"] = str(args.age)
            if args.gender:
                row["gender"] = args.gender
            if args.phone:
                row["phone"] = args.phone
            if args.meds is not None:
                row["meds"] = args.meds
            if args.appointments is not None:
                row["appointments"] = args.appointments
            if args.notes is not None:
                row["notes"] = args.notes
            row["updated_at"] = datetime.utcnow().isoformat()
            updated = True
            logging.info("UPDATE id=%s", row["id"])
            print("Updated:", row["id"], row["name"])
            break
    if not updated:
        print("Patient id not found:", args.id)
    else:
        write_all(rows)


def delete_patient(args: argparse.Namespace) -> None:
    """Delete patient record by ID."""
    rows = read_all()
    new_rows = [row for row in rows if row["id"] != str(args.id)]
    if len(new_rows) == len(rows):
        print("Patient id not found:", args.id)
    else:
        write_all(new_rows)
        logging.info("DELETE id=%s", args.id)
        print("Deleted patient id:", args.id)


def export_data(args: argparse.Namespace) -> None:
    """Export patient records to JSON."""
    rows = read_all()
    output_file = args.out or "exported_patients.json"
    with open(output_file, "w", encoding="utf-8") as file_handle:
        json.dump(rows, file_handle, indent=2)
    print("Exported to", output_file)


def stats(_args: argparse.Namespace) -> None:
    """Show basic statistics of patients."""
    rows = read_all()
    total = len(rows)
    ages = [int(row["age"]) for row in rows if row["age"].isdigit()]
    avg_age: Optional[float] = sum(ages) / len(ages) if ages else None
    print("Total patients:", total)
    print("Avg age:", f"{avg_age:.1f}" if avg_age is not None else "-")


def parse_args(argv=None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(prog="emr_cli", description="Lightweight EMR CLI")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    parser_add = subparsers.add_parser("add", help="Add new patient")
    parser_add.add_argument("--name", required=True)
    parser_add.add_argument("--age", type=int)
    parser_add.add_argument("--gender", choices=["M", "F", "O"], default="O")
    parser_add.add_argument("--phone")
    parser_add.add_argument("--meds", default="")
    parser_add.add_argument("--appointments", default="")
    parser_add.add_argument("--notes", default="")
    parser_add.set_defaults(func=add_patient)

    parser_list = subparsers.add_parser("list", help="List patients")
    parser_list.add_argument("--limit", type=int, default=20)
    parser_list.set_defaults(func=list_patients)

    parser_search = subparsers.add_parser(
        "search", help="Search patients by name/phone"
    )
    parser_search.add_argument("--name", required=True)
    parser_search.set_defaults(func=search_patients)

    parser_update = subparsers.add_parser("update", help="Update patient fields by id")
    parser_update.add_argument("--id", required=True)
    parser_update.add_argument("--name")
    parser_update.add_argument("--age", type=int)
    parser_update.add_argument("--gender", choices=["M", "F", "O"])
    parser_update.add_argument("--phone")
    parser_update.add_argument("--meds")
    parser_update.add_argument("--appointments")
    parser_update.add_argument("--notes")
    parser_update.set_defaults(func=update_patient)

    parser_delete = subparsers.add_parser("delete", help="Delete patient by id")
    parser_delete.add_argument("--id", required=True)
    parser_delete.set_defaults(func=delete_patient)

    parser_export = subparsers.add_parser("export", help="Export data to JSON")
    parser_export.add_argument("--out", help="Output filename")
    parser_export.set_defaults(func=export_data)

    parser_stats = subparsers.add_parser("stats", help="Show basic stats")
    parser_stats.set_defaults(func=stats)

    return parser.parse_args(argv)


def main(argv=None) -> None:
    """Main CLI entrypoint."""
    arguments = parse_args(argv)
    try:
        arguments.func(arguments)
    except (argparse.ArgumentError, IOError, OSError) as exc:
        logging.exception("Error running command")
        print("Error:", exc)


if __name__ == "__main__":
    main()
