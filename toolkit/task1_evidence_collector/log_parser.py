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
1. Accept a log file path as a command-line argument (argparse — NO prompts).
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
- All input via argparse.
- NO use of os.system() or subprocess.

OUTPUT CONTRACT (auto-grader depends on this)
---------------------------------------------
CSV file with headers: Timestamp, IP_Address, User_Account
Rows are comma-separated, one per matching log event.
Duplicate entries must be de-duplicated.

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

# Your imports go here
import argparse
import re
import sys
from ipaddress import ip_address
from pathlib import Path


def parse_arguments():
    """
    Define and parse command-line arguments.
    Returns the parsed namespace object.
    """
    # TODO: Implement argparse
    # Required: input_file (positional)
    # Optional: --output (default: suspects.csv)

    parser = argparse.ArgumentParser(description="parse linux auth logs")
    parser.add_argument("input_file", help="path to the desired file")
    parser.add_argument("--output", default="suspects.csv", help="output Csv file")
    args = parser.parse_args()
    return args


def parse_log(file_path: Path) -> list[dict]:
    """
    Read the log file and extract IoC records.

    Args:
        file_path: Path object pointing to the log file.

    Returns:
        A list of dicts, each containing:
        {'Timestamp': str, 'IP_Address': str, 'User_Account': str}

    Raises:
        FileNotFoundError: If the log file does not exist.
        ValueError: If the file is empty.
    """
    # TODO: Implement log parsing logic
    # Hint: compile your regex patterns before the loop for efficiency

    file_path = Path(file_path)

    # Check that the specified path for the file exists, if not fail gracefully.
    if not file_path.exists():
        raise FileNotFoundError(f"No log file found at: {file_path}")

    # Create an empty set for unique results to be stored in
    unique_records = set()
    records = []

    # Compile regex patterns that will be used
    password = re.compile(r"Failed password")
    user = re.compile(r"Invalid user")
    ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

    # Open the file, read it, close it and store the results in the specified file
    with open(file_path, "r", encoding="utf-8") as log_file:

        # Read the first line to check if its empty, if it is empty fail gracefully.
        first_line = log_file.readline()
        if not first_line:
            raise ValueError(f"log file is empty at: {file_path}")

        # If the file is not empty check the first line to look for the specified patterns
        if password.search(first_line) or user.search(first_line):

            Timestamp = " ".join(first_line.split()[0:3])
            ip_match = ip_pattern.search(first_line)

            user_match = None

            if password.search(first_line):
                user_match = re.search(r"for (?:invalid user )?(\S+) from", first_line)

            if user.search(first_line):
                user_match = re.search(r"user (\S+) from", first_line)

            if ip_match and user_match:

                IP_Address = ip_match.group()
                User_Account = user_match.group(1)

                dedup_key = (IP_Address, User_Account)

                if dedup_key not in unique_records:
                    unique_records.add(dedup_key)
                    records.append(
                        {
                            "Timestamp": Timestamp,
                            "IP_Address": IP_Address,
                            "User_Account": User_Account,
                        }
                    )

        # Loop through each line in the log file in search of the specified patterns.
        for line in log_file:

            if password.search(line) or user.search(line):

                Timestamp = " ".join(line.split()[0:3])
                ip_match = ip_pattern.search(line)

                user_match = None

                if password.search(line):
                    user_match = re.search(r"for (?:invalid user )?(\S+) from", line)

                if user.search(line):
                    user_match = re.search(r"user (\S+) from", line)

                if ip_match and user_match:

                    IP_Address = ip_match.group()
                    User_Account = user_match.group(1)

                    dedup_key = (IP_Address, User_Account)

                    if dedup_key not in unique_records:
                        unique_records.add(dedup_key)
                        records.append(
                            {
                                "Timestamp": Timestamp,
                                "IP_Address": IP_Address,
                                "User_Account": User_Account,
                            }
                        )

    return records


def write_csv(records: list[dict], output_path: Path) -> None:
    """
    Write extracted records to a CSV file.

    Args:
        records:     List of IoC record dicts.
        output_path: Path object for the output CSV file.
    """
    # TODO: Implement CSV writing
    # Headers must be exactly: Timestamp, IP_Address, User_Account

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        file.write("Timestamp,IP_Address,User_Account\n")
        for record in records:
            file.write(
                f"{record['Timestamp']},{record['IP_Address']},{record['User_Account']}\n"
            )


def main():
    args = parse_arguments()
    # TODO: Wire parse_arguments → parse_log → write_csv
    # Handle exceptions and print informative messages to stderr
    try:
        records = parse_log(args.input_file)
        write_csv(records, args.output)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
