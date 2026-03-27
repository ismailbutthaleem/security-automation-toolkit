"""
================================================================================
COM5413 — The Benji Protocol
Task 2: The Network Cartographer
File:   scan.py
================================================================================

MISSION BRIEF
-------------
Ethan cannot go in blind. Benji maps every door, every service, every version
number. The scan is not the attack — it is the intelligence that makes the
attack possible. A missed service or a wrong version assumption costs the
mission.

Your job is to build a threaded TCP port scanner that identifies open ports and
grabs the service banner from each one. The banner is the service telling you
exactly what it is and what version it is running. Listen carefully.

WHAT THIS SCRIPT MUST DO
-------------------------
1. Accept a target IP and port range/list as command-line arguments.
2. Attempt a TCP connection to each port using Python's socket library.
3. If the port is open, attempt to receive the service banner (the greeting
   text the service sends on connection).
4. Use threading (ThreadPoolExecutor) to scan multiple ports concurrently.
5. Implement a connection timeout (default 0.5s) — hanging the scanner is not
   an option in the field.
6. Output results as JSON: printed to stdout AND saved to recon_results.json.

CONSTRAINTS
-----------
- Python 3.10+ only.
- Use socket — do NOT wrap nmap or any external scanner.
<<<<<<< HEAD
- NO use of input() — all input via argparse.
=======
- NO use of the input built-in — all input via argparse.
>>>>>>> template/main
- Timeout must be configurable via --timeout argument.

OUTPUT CONTRACT (auto-grader depends on this)
---------------------------------------------
JSON structure:
{
    "target": "192.168.x.x",
    "scan_time": "YYYY-MM-DD HH:MM:SS",
    "open_ports": [
        {"port": 21, "banner": "220 (vsFTPd 2.3.4)"},
        {"port": 22, "banner": "SSH-2.0-OpenSSH_4.7p1"},
        {"port": 80, "banner": ""}
    ]
}
"banner" must always be present — use empty string if no banner received.

EXAMPLE USAGE
-------------
    python scan.py 192.168.56.101 --ports 1-1024
    python scan.py 192.168.56.101 --ports 21,22,80,443
    python scan.py 192.168.56.101 --ports 1-65535 --timeout 1.0 --threads 100

BUILD LOG
---------
Use docs/build.md to record your development notes, decisions, and reflections
as you build this tool. Pay particular attention to documenting what you observe
in the banner output when scanning Metasploitable — this feeds directly into
the Vulnerability Hunt.
================================================================================
"""

# Your imports go here
import argparse
import json
import socket
import sys
<<<<<<< HEAD
from concurrent.futures import ThreadPoolExecutor
=======
from concurrent.futures import ThreadPoolExecutor, as_completed
>>>>>>> template/main
from datetime import datetime
from pathlib import Path


def parse_arguments():
    """
    Define and parse command-line arguments.

    Returns the parsed namespace object.
    Required: target (positional IP address)
    Optional: --ports, --timeout, --threads, --output
    """
    # TODO: Implement argparse
    # --ports should accept both ranges (1-1024) and lists (21,22,80)
<<<<<<< HEAD

    parser = argparse.ArgumentParser(description="parse ports")
    parser.add_argument("target", help="scan a tcp port")
    parser.add_argument(
        "--output", default="recon_results.json", help="output JSON file"
    )
    parser.add_argument("--ports", default="1-1024", help="select a port range")
    parser.add_argument(
        "--timeout", default=0.5, type=float, help="timeout duration in seconds"
    )
    parser.add_argument("--threads", default=50, type=int, help="number of threads")
    args = parser.parse_args()
    return args
=======
    pass
>>>>>>> template/main


def parse_port_input(port_string: str) -> list[int]:
    """
    Parse a port string into a list of integer port numbers.

    Accepts:
        "1-1024"    → [1, 2, 3, ..., 1024]
        "21,22,80"  → [21, 22, 80]

    Args:
        port_string: Raw string from argparse.

    Returns:
        Sorted list of port integers.

    Raises:
        ValueError: If the format is unrecognised or ports are out of range.
    """
    # TODO: Implement port range/list parsing
<<<<<<< HEAD

    """
    Convert a port specification string into a sorted list of unique integers.
    """
    ports = []

    for part in port_string.split(","):
        part = part.strip()

        if "-" in part:
            try:
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
            except ValueError:
                raise ValueError(f"Invalid port range: {part}")

            if start > end:
                raise ValueError(f"Invalid range (start > end): {part}")

            if start < 1 or end > 65535:
                raise ValueError(f"Port out of valid range: {part}")

            ports.extend(range(start, end + 1))

        else:
            try:
                port = int(part)
            except ValueError:
                raise ValueError(f"Invalid port value: {part}")

            if port < 1 or port > 65535:
                raise ValueError(f"Port out of valid range: {port}")

            ports.append(port)

    return sorted(set(ports))
=======
    pass
>>>>>>> template/main


def grab_banner(sock: socket.socket, timeout: float = 0.5) -> str:
    """
    Attempt to receive a banner string from an open socket.

    Args:
        sock:    An already-connected socket object.
        timeout: Seconds to wait for banner data.

    Returns:
        Decoded banner string, or empty string if no banner received.
    """
    # TODO: Implement banner grabbing
    # Handle: timeout, decode errors, empty response
<<<<<<< HEAD
    try:
        sock.settimeout(timeout)
        banner_data = sock.recv(1024)
        return banner_data.decode(
            "utf-8",
            errors="ignore",
        ).strip()
    except (socket.timeout, OSError):
        return ""
=======
    pass
>>>>>>> template/main


def check_port(target: str, port: int, timeout: float) -> dict | None:
    """
    Attempt a TCP connection to target:port.

    Args:
        target:  IP address string.
        port:    Port number integer.
        timeout: Connection timeout in seconds.

    Returns:
        Dict {"port": int, "banner": str} if open, None if closed/filtered.
    """
    # TODO: Implement TCP connect attempt
    # On success: call grab_banner(), return result dict
    # On failure: return None (do not raise)
<<<<<<< HEAD

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))

        if result == 0:
            banner = grab_banner(sock, timeout)
            return {"port": port, "banner": banner}

        return None

    except (socket.timeout, OSError):
        return None

    finally:
        sock.close()
=======
    pass
>>>>>>> template/main


def main():
    args = parse_arguments()
    # TODO: Wire parse_arguments → parse_port_input → ThreadPoolExecutor
    #       → collect results → write JSON output
<<<<<<< HEAD

    try:
        ports = parse_port_input(args.ports)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(check_port, args.target, port, args.timeout): port
            for port in ports
        }

        for future in futures:
            result = future.result()
            if result is not None:
                open_ports.append(result)

    open_ports.sort(key=lambda item: item["port"])

    output = {
        "target": args.target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports": open_ports,
    }

    json_output = json.dumps(output, indent=2)

    print(json_output)
    Path(args.output).write_text(json_output)
=======
    pass
>>>>>>> template/main


if __name__ == "__main__":
    main()
