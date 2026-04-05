"""
================================================================================
COM5413 — The Benji Protocol
Task 1: The Evidence Collector
File:   log_parser.py
================================================================================

MISSION BRIEF
-------------
Before any operation, Benji pulls the logs. Something happened on that server.
The evidence is in the noise — if you know how to read it.

Your job is to parse a Linux auth.log file and extract Indicators of Compromise
(IoC). Specifically, you are looking for failed authentication attempts that
suggest a brute-force attack. Your output must be structured, consistent, and
machine-readable — sloppy evidence gets people killed in the field.

WHAT THIS SCRIPT MUST DO
-------------------------
1. Accept a log file path as a command-line argument (argparse — no input built-in).
2. Use regular expressions (re) to identify lines containing:
   - "Failed password"
   - "Invalid user"
3. Extract from each matching line:
   - Timestamp
   - IP Address
   - User Account
4. Write a CSV report to suspects.csv (or a path specified via --output).
   CSV headers must be exactly: Timestamp, IP_Address, User_Account
5. Handle errors gracefully:
   - File not found
   - Empty file
   - No matches found (report zero results, do not crash)

CONSTRAINTS
-----------
- Python 3.10+ only.
- Standard library only (re, csv, argparse, pathlib).
- NO use of the input built-in — all input via argparse.
- NO use of os.system() or subprocess.

OUTPUT CONTRACT (auto-grader depends on this)
---------------------------------------------
CSV file with headers: Timestamp, IP_Address, User_Account
Rows are comma-separated, one per matching log event.
Duplicate entries must be de-duplicated (same timestamp + IP + user = one row).

EXAMPLE USAGE
-------------
    python log_parser.py /var/log/auth.log
    python log_parser.py /var/log/auth.log --output /tmp/suspects.csv

BUILD LOG
---------
Use docs/build.md to record your development notes, decisions, and reflections
as you build this tool. Benji documents everything.
================================================================================
"""

import argparse
import re
import sys
from pathlib import Path


def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Parse Linux auth logs")
    parser.add_argument("input_file", help="Path to the log file")
    parser.add_argument("--output", default="suspects.csv", help="Output CSV file")
    return parser.parse_args()


def parse_log(file_path: Path) -> list[dict]:
    """
    Reads log file and extracts IoC records.
    """
    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(f"No log file found at: {file_path}")

    unique_records = set()  # used for deduplication
    records = []

    # Required patterns from assignment brief
    password_pattern = re.compile(r"Failed password")
    invalid_user_pattern = re.compile(r"Invalid user")

    # OPTIONAL extension (real-world logs)
    pam_pattern = re.compile(r"authentication failure")

    # Extraction patterns
    ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
    pam_ip_pattern = re.compile(r"rhost=(\d+\.\d+\.\d+\.\d+)")
    pam_user_pattern = re.compile(r"user=(\S+)")

    # Timestamp patterns (handles both syslog + ISO format)
    syslog_timestamp_pattern = re.compile(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}")
    iso_timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as log_file:
        first_line = log_file.readline()

        # Handle empty file case
        if not first_line:
            raise ValueError(f"log file is empty at: {file_path}")

        def process_line(line: str):
            """
            Processes a single log line and extracts IoC data.
            """

            # Step 1 — Filter relevant lines (based on brief + optional extension)
            if not (
                password_pattern.search(line)
                or invalid_user_pattern.search(line)
                or pam_pattern.search(line)
            ):
                return

            # Step 2 — Extract timestamp
            timestamp_match = syslog_timestamp_pattern.search(line)
            if not timestamp_match:
                timestamp_match = iso_timestamp_pattern.search(line)
            if not timestamp_match:
                return

            timestamp = timestamp_match.group()

            ip_address = None
            user_account = None

            # Step 3 — Handle PAM-style logs (authentication failure)
            if pam_pattern.search(line):
                pam_ip_match = pam_ip_pattern.search(line)
                pam_user_match = pam_user_pattern.search(line)

                if not pam_ip_match or not pam_user_match:
                    return

                ip_address = pam_ip_match.group(1)
                user_account = pam_user_match.group(1)

            # Step 4 — Handle standard auth.log patterns
            else:
                ip_match = ip_pattern.search(line)
                if not ip_match:
                    return

                user_match = None

                if password_pattern.search(line):
                    user_match = re.search(r"for (?:invalid user )?(\S+) from", line)

                elif invalid_user_pattern.search(line):
                    user_match = re.search(r"Invalid user (\S+) from", line)

                if not user_match:
                    return

                ip_address = ip_match.group()
                user_account = user_match.group(1)

            # Step 5 — Deduplicate entries
            dedup_key = (timestamp, ip_address, user_account)

            if dedup_key not in unique_records:
                unique_records.add(dedup_key)

                records.append(
                    {
                        "Timestamp": timestamp,
                        "IP_Address": ip_address,
                        "User_Account": user_account,
                    }
                )

        # Process first line separately (already read)
        process_line(first_line)

        # Process remaining lines
        for line in log_file:
            process_line(line)

    return records


def write_csv(records: list[dict], output_path: Path) -> None:
    """
    Writes extracted records to CSV file.
    """
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        file.write("Timestamp,IP_Address,User_Account\n")

        for record in records:
            file.write(
                f"{record['Timestamp']},{record['IP_Address']},{record['User_Account']}\n"
            )


def main():
    args = parse_arguments()

    try:
        records = parse_log(args.input_file)
        write_csv(records, args.output)

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
