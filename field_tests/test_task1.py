"""
================================================================================
COM5413 — The Benji Protocol
IMF Field Test — Task 1: The Evidence Collector
================================================================================

These tests verify that log_parser.py meets the output contract defined in
the assessment brief. They are run by the auto-grader at submission and can
be run locally by you at any time.

Run with:
    pytest field_tests/test_task1.py -v

All tests must pass for full marks on the automated component of Task 1.
A failing test tells you exactly what the contract violation is — fix it.
================================================================================
"""

import csv
import subprocess
import sys
from pathlib import Path

<<<<<<< HEAD
=======
import pytest

>>>>>>> template/main
# Path resolution — tests run from repo root
SCRIPT = Path("toolkit/task1_evidence_collector/log_parser.py")
SAMPLE_LOG = Path("field_tests/fixtures/sample_auth.log")
OUTPUT_CSV = Path("field_tests/fixtures/test_output.csv")

# ---------------------------------------------------------------------------
# Fixture: synthetic auth.log with known content
# ---------------------------------------------------------------------------

SAMPLE_LOG_CONTENT = """\
Jan 10 06:55:48 ubuntu sshd[1234]: Failed password for root from 192.168.56.200 port 22 ssh2
Jan 10 06:55:49 ubuntu sshd[1235]: Failed password for invalid user admin from 10.0.0.5 port 22 ssh2
Jan 10 06:55:50 ubuntu sshd[1236]: Invalid user testuser from 172.16.0.1 port 22
Jan 10 06:55:51 ubuntu sshd[1237]: Accepted password for msfadmin from 192.168.56.1 port 22 ssh2
<<<<<<< HEAD
Jan 10 06:55:52 ubuntu sshd[1238]: Failed password for root from 192.168.56.200 port 22 ssh2
"""


def setup_fixtures():
    """Create fixture files needed for tests."""
=======
Jan 10 06:55:48 ubuntu sshd[1238]: Failed password for root from 192.168.56.200 port 22 ssh2
"""


@pytest.fixture(autouse=False)
def fixtures():
    """Create and tear down fixture files for each test."""
>>>>>>> template/main
    fixture_dir = Path("field_tests/fixtures")
    fixture_dir.mkdir(parents=True, exist_ok=True)
    SAMPLE_LOG.write_text(SAMPLE_LOG_CONTENT)
    if OUTPUT_CSV.exists():
        OUTPUT_CSV.unlink()
<<<<<<< HEAD
=======
    yield
    # Teardown
    if OUTPUT_CSV.exists():
        OUTPUT_CSV.unlink()
>>>>>>> template/main


def run_parser(args: list[str]) -> subprocess.CompletedProcess:
    """Helper: run log_parser.py with given arguments."""
    return subprocess.run(
<<<<<<< HEAD
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True
=======
        [sys.executable, str(SCRIPT)] + args, capture_output=True, text=True
>>>>>>> template/main
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

<<<<<<< HEAD
=======

>>>>>>> template/main
def test_script_exists():
    """Task 1 script must exist at the expected path."""
    assert SCRIPT.exists(), f"Script not found at {SCRIPT}"


<<<<<<< HEAD
def test_script_runs_without_error():
    """Script must execute without Python errors against a valid log."""
    setup_fixtures()
=======
def test_script_runs_without_error(fixtures):
    """Script must execute without Python errors against a valid log."""
>>>>>>> template/main
    result = run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    assert result.returncode == 0, f"Script exited with error:\n{result.stderr}"


<<<<<<< HEAD
def test_output_csv_created():
    """suspects.csv (or --output target) must be created."""
    setup_fixtures()
=======
def test_output_csv_created(fixtures):
    """suspects.csv (or --output target) must be created."""
>>>>>>> template/main
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    assert OUTPUT_CSV.exists(), "Output CSV was not created."


<<<<<<< HEAD
def test_csv_headers():
    """CSV must have exactly the required headers in the correct order."""
    setup_fixtures()
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["Timestamp", "IP_Address", "User_Account"], \
            f"Unexpected headers: {reader.fieldnames}"


def test_correct_ip_extraction():
    """Must correctly extract IP addresses from Failed password lines."""
    setup_fixtures()
=======
def test_csv_headers(fixtures):
    """CSV must have exactly the required headers in the correct order."""
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == [
            "Timestamp",
            "IP_Address",
            "User_Account",
        ], f"Unexpected headers: {reader.fieldnames}"


def test_correct_ip_extraction(fixtures):
    """Must correctly extract IP addresses from Failed password lines."""
>>>>>>> template/main
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    ips = {row["IP_Address"] for row in rows}
    assert "192.168.56.200" in ips, "Expected IP 192.168.56.200 not found."
    assert "10.0.0.5" in ips, "Expected IP 10.0.0.5 not found."
    assert "172.16.0.1" in ips, "Expected IP 172.16.0.1 not found."


<<<<<<< HEAD
def test_accepted_password_excluded():
    """Accepted password lines must NOT appear in output."""
    setup_fixtures()
=======
def test_correct_user_extraction(fixtures):
    """Must correctly extract User_Account values, including from compound patterns.
    The line "Failed password for invalid user admin" must yield User_Account=admin,
    not "invalid", "user", or "invalid user admin"."""
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    # testuser from Invalid user line
    testuser_rows = [r for r in rows if r["IP_Address"] == "172.16.0.1"]
    assert len(testuser_rows) == 1, "Expected one row for 172.16.0.1"
    assert (
        testuser_rows[0]["User_Account"] == "testuser"
    ), f"Expected 'testuser', got '{testuser_rows[0]['User_Account']}'"
    # admin from 'Failed password for invalid user admin' — must strip 'invalid user' prefix
    admin_rows = [r for r in rows if r["IP_Address"] == "10.0.0.5"]
    assert len(admin_rows) == 1, "Expected one row for 10.0.0.5"
    assert (
        admin_rows[0]["User_Account"] == "admin"
    ), f"Expected 'admin', got '{admin_rows[0]['User_Account']}' — check 'invalid user' prefix handling"


def test_correct_timestamp_extraction(fixtures):
    """Must correctly extract the Timestamp from matching log lines."""
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    target = [r for r in rows if r["IP_Address"] == "172.16.0.1"]
    assert len(target) == 1
    assert (
        target[0]["Timestamp"] == "Jan 10 06:55:50"
    ), f"Expected timestamp 'Jan 10 06:55:50', got '{target[0]['Timestamp']}'"


def test_accepted_password_excluded(fixtures):
    """Accepted password lines must NOT appear in output."""
>>>>>>> template/main
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    ips = [row["IP_Address"] for row in rows]
<<<<<<< HEAD
    assert "192.168.56.1" not in ips, \
        "Accepted password IP incorrectly included in suspects.csv"


def test_deduplication():
    """Duplicate entries (same timestamp+IP+user) must appear only once."""
    setup_fixtures()
=======
    assert (
        "192.168.56.1" not in ips
    ), "Accepted password IP incorrectly included in suspects.csv"


def test_deduplication(fixtures):
    """Duplicate entries (same timestamp, IP address, and user account) must appear only once.
    The fixture contains two identical attempts: root from 192.168.56.200 at 06:55:48.
    After deduplication, only one row should remain for this IP/user/timestamp combination.
    """
>>>>>>> template/main
    run_parser([str(SAMPLE_LOG), "--output", str(OUTPUT_CSV)])
    with open(OUTPUT_CSV, newline="") as f:
        rows = list(csv.DictReader(f))
    # 192.168.56.200 appears twice in the fixture — should appear once after dedup
<<<<<<< HEAD
    root_rows = [r for r in rows if r["IP_Address"] == "192.168.56.200" and r["User_Account"] == "root"]
    assert len(root_rows) == 1, \
        f"Duplicate entries not removed: found {len(root_rows)} rows for 192.168.56.200/root"


def test_missing_file_handled():
    """Script must exit cleanly (non-zero) when log file does not exist."""
    result = run_parser(["/tmp/this_file_does_not_exist_com5413.log"])
    assert result.returncode != 0, "Script should exit non-zero for missing input file."


def test_no_input_function_used():
    """Script must not contain input() calls — this breaks automation."""
    source = SCRIPT.read_text()
    assert "input(" not in source, \
        "input() found in script. All input must use argparse. NO EXCEPTIONS."
=======
    root_rows = [
        r
        for r in rows
        if r["IP_Address"] == "192.168.56.200" and r["User_Account"] == "root"
    ]
    assert (
        len(root_rows) == 1
    ), f"Duplicate entries not removed: found {len(root_rows)} rows for 192.168.56.200/root"


def test_missing_file_handled(fixtures):
    """Script must exit with non-zero code when log file does not exist,
    and must print the error message to stderr (not stdout)."""
    result = run_parser(["/tmp/this_file_does_not_exist_com5413.log"])
    assert result.returncode != 0, "Script should exit non-zero for missing input file."
    assert (
        result.stderr.strip() != ""
    ), "Error message must be written to stderr, not stdout. result.stderr was empty."
    assert (
        result.stdout.strip() == ""
    ), "Nothing should be written to stdout when the input file is missing."


def test_no_input_function_used():
    """Script must not contain input() calls — this breaks automation.
    Comments and docstrings mentioning input() are excluded from this check.
    Only actual function call syntax triggers a failure."""
    import re

    source = SCRIPT.read_text()
    # Strip single-line comments and check for bare input( calls
    # Remove lines that are pure comments (start with optional whitespace then #)
    non_comment_lines = [
        line for line in source.split("\n") if not line.strip().startswith("#")
    ]
    # Also strip docstring content (anything inside triple quotes)
    non_comment_source = "\n".join(non_comment_lines)
    # Remove triple-quoted strings
    non_comment_source = re.sub(r'""".*?"""', "", non_comment_source, flags=re.DOTALL)
    non_comment_source = re.sub(r"'''.*?'''", "", non_comment_source, flags=re.DOTALL)
    assert (
        "input(" not in non_comment_source
    ), "input() found in script code. All input must use argparse. NO EXCEPTIONS."
>>>>>>> template/main
