"""
================================================================================
COM5413 — The Benji Protocol
Task 4: The Web Enumerator
File:   web_enum.py
================================================================================

MISSION BRIEF
-------------
The web layer talks too much. Server versions buried in HTTP headers. Developer
notes left in HTML comments. Sensitive paths left exposed because nobody
thought to check. Benji listens. A well-configured web server tells you almost
nothing; most servers are not well-configured.

Your job is to build an HTTP reconnaissance tool that extracts intelligence
from HTTP response headers and HTML source. This is passive reconnaissance —
you are reading what the server is already broadcasting, not probing for
weaknesses directly.

WHAT THIS SCRIPT MUST DO
-------------------------
1. Accept a target URL as a command-line argument.
2. Send an HTTP GET request and analyse the response headers for:
   - Server (e.g., Apache/2.2.8)
   - X-Powered-By (e.g., PHP/5.2.4)
   - Any other headers that reveal technology or version information.
3. Parse the HTML response using BeautifulSoup to extract:
   - All HTML comments (<!-- --> blocks) — flags are often hidden here.
4. Check for the existence of sensitive paths:
   - /robots.txt
   - /admin
   - /phpmyadmin
   - /login
   - /.git
   (Report found/not found for each — do not enumerate further.)
5. Output a structured summary (JSON or formatted plaintext).

CONSTRAINTS
-----------
- Python 3.10+ only.
- Must use requests and beautifulsoup4 (bs4).
- Set a request timeout (default 5s) — never hang.
- Handle redirects gracefully (requests does this by default — be aware of it).
- NO use of input() — all input via argparse.
- NO use of the input built-in — all input via argparse.

OUTPUT CONTRACT (auto-grader depends on this)
---------------------------------------------
Print a summary containing at minimum:
    [HEADERS]
    Server: <value or "Not present">
    X-Powered-By: <value or "Not present">

    [COMMENTS]
    Found <n> HTML comment(s):
    1. <comment text>
    2. <comment text>

    [SENSITIVE PATHS]
    /robots.txt       → FOUND (200)
    /admin            → NOT FOUND (404)
    ...

EXAMPLE USAGE
-------------
    python web_enum.py http://192.168.56.101
    python web_enum.py http://192.168.56.101/dvwa --timeout 10

BUILD LOG
---------
Use docs/build.md to record what you find when running against Metasploitable.
HTML comments in particular — document what you find and what it implies.
This intelligence feeds directly into the Vulnerability Hunt diagnosis phase.
================================================================================
"""

# Your imports go here
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup, Comment
except ImportError as e:
    print(
        f"[-] Missing dependency: {e}. Run: pip install requests beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(1)


# Sensitive paths to probe — this list can be extended
SENSITIVE_PATHS = [
    "/robots.txt",
    "/admin",
    "/phpmyadmin",
    "/login",
    "/.git",
    "/drupal",
    "/drupal/CHANGELOG.txt",
    "/drupal/q=user",
    "/dbadmin",
    "/backup",
    "/backup.zip",
    "/dev",
    "/test",
    "/.env",
    "/config.php",
]


def save_results_to_json(
    output_path: Path,
    target_url: str,
    headers: dict,
    comments: list[str],
    sensitive_paths: dict,
) -> None:
    """
    Save web enumeration results to a JSON file.
    """
    data = {
        "target": target_url,
        "headers": headers,
        "comments": comments,
        "sensitive_paths": sensitive_paths,
    }

    try:
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"[-] ERROR: Could not write JSON file: {error}", file=sys.stderr)
        sys.exit(1)


def parse_arguments():
    """
    Define and parse command-line arguments.

    Returns the parsed namespace object.
    Required: url (positional)
    Optional: --timeout (default 5)
    """
    parser = argparse.ArgumentParser(
        description="HTTP enumeration tool — analyse headers, extract comments, probe paths"
    )
    parser.add_argument("url", help="Target URL (e.g., http://172.16.19.101)")
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("web_results.json"),
    )
    return parser.parse_args()


def analyse_headers(response: requests.Response) -> dict:
    """
    Extract security-relevant information from HTTP response headers.

    Args:
        response: A requests.Response object.

    Returns:
        Dict of relevant header names to values.
        Use "Not present" for missing headers.
    """
    relevant_headers = {
        "Server": response.headers.get("Server", "Not present"),
        "X-Powered-By": response.headers.get("X-Powered-By", "Not present"),
    }

    # Add any other revealing headers if present
    optional_headers = [
        "X-AspNet-Version",
        "X-Generator",
        "Via",
        "X-Backend-Server",
    ]

    for header in optional_headers:
        if header in response.headers:
            relevant_headers[header] = response.headers[header]

    return relevant_headers


def extract_comments(html: str) -> list[str]:
    """
    Extract all HTML comments from a page's source.

    Args:
        html: Raw HTML string.

    Returns:
        List of comment strings (stripped of <!-- --> delimiters).
    """
    soup = BeautifulSoup(html, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    return [comment.strip() for comment in comments if comment.strip()]


def check_sensitive_paths(base_url: str, timeout: int) -> dict:
    """
    Probe a list of sensitive paths and record HTTP status codes.

    Args:
        base_url: The target base URL.
        timeout:  Request timeout in seconds.

    Returns:
        Dict mapping path string to status code integer (or None if error).
    """
    results = {}

    for path in SENSITIVE_PATHS:
        full_url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))

        try:
            response = requests.get(full_url, timeout=timeout, allow_redirects=False)
            results[path] = response.status_code
        except requests.exceptions.RequestException:
            results[path] = None

    return results


def main():
    args = parse_arguments()

    # Basic validation — ensure URL includes scheme like http://
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print(
            "[-] ERROR: Please provide a valid URL including http:// or https://",
            file=sys.stderr,
        )
        sys.exit(1)

    # Main page request
    try:
        response = requests.get(args.url, timeout=args.timeout)
    except requests.exceptions.RequestException as e:
        print(f"[-] ERROR: Could not connect to {args.url}: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[-] INTERRUPTED: Execution stopped by user.(ctl+C)", file=sys.stderr)
        sys.exit(1)

    headers = analyse_headers(response)
    comments = extract_comments(response.text)
    path_results = check_sensitive_paths(args.url, args.timeout)

    # Save results to a JSON file
    save_results_to_json(
        Path("web_enum_results.json"),
        args.url,
        headers,
        comments,
        path_results,
    )

    # Print formatted output
    print("[HEADERS]")
    print(f"Server: {headers.get('Server', 'Not present')}")
    print(f"X-Powered-By: {headers.get('X-Powered-By', 'Not present')}")

    for key, value in headers.items():
        if key not in ("Server", "X-Powered-By"):
            print(f"{key}: {value}")

    print()
    print("[COMMENTS]")
    print(f"Found {len(comments)} HTML comment(s):")
    if comments:
        for index, comment in enumerate(comments, start=1):
            print(f"{index}. {comment}")

    print()
    print("[SENSITIVE PATHS]")
    for path, status_code in path_results.items():
        if status_code is None:
            print(f"{path:<16} → ERROR")
        elif status_code == 200:
            print(f"{path:<16} → FOUND ({status_code})")
        elif status_code == 403:
            print(f"{path:<16} → Forbidden ({status_code})")
        elif status_code == 301:
            print(f"{path:<16} → Redirect ({status_code})")
        else:
            print(f"{path:<16} → NOT FOUND ({status_code})")


if __name__ == "__main__":
    main()
