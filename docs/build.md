# The Benji Protocol — Build Log

**Student Name:** Ismail Butt Haleem
**Student ID:** 2433887
**GitHub Repository:**

---

> "Benji documents everything. Not because he is asked to. Because a tool with
> no history is a tool you cannot trust, and a mission with no record is a
> mission that never happened."

This is your running build log. Update it after every significant coding
session. It is not an essay — it is a technical journal. Short entries are
fine. No entry is not fine.

The build log serves three purposes:
1. It is evidence of your development process for the portfolio marker.
2. It is your own reference when something breaks at 23:00 the night before
   the Vulnerability Hunt.
3. It demonstrates that the code in your repository is yours.

---

## How to Use This Document

Add a new entry for each session using the template below. Commit this file
alongside your code — the build log and the code should tell the same story.

---

## Entry Template

### [DATE] — [TASK / SESSION]

**What I built / changed:**

**What broke and how I fixed it:**

**Decisions I made and why:**

**What the tool output when I ran it against Metasploitable:**

**Questions or things to revisit:**

---

## Week 1 — Task 1: Evidence Collector

### [13-03-2026] — Session A

**What I built / changed:**

Set up the full working environment for the assignment. Installed Kali Linux as the development machine and Metasploitable as the target machine. Configured networking between both virtual machines to ensure they could communicate properly.

Joined the GitHub Classroom repository and cloned the project locally. Created and configured a GitHub token to allow authentication and pushing changes to the repository.

Although a pre-built Kali machine was suggested, I chose to install and configure my own Kali VM to have more control over the environment and better understanding of the setup.

---

**What broke and how I fixed it:**

Initially had issues with networking between the VMs, which prevented communication. This was resolved by correctly configuring the network adapters (NAT and Host-Only) and verifying connectivity.

Also had some initial confusion with Git authentication, which was resolved by generating and using a GitHub token instead of password authentication.

---

**Decisions I made and why:**

Chose to manually install Kali instead of using a prebuilt version to gain better understanding of the system setup and configuration process.

Set up proper Git authentication early to avoid issues later when pushing work as evidence.

---

**What the tool output when I ran it against Metasploitable:**

No tools developed yet in this session — focus was on environment setup.

---

**Questions or things to revisit:**

Ensure networking remains stable when starting VMs again.
Revisit VM configuration if any connectivity issues appear during later stages.

---

### [15-03-2026] — Session B

What I built / changed:

Developed log_parser.py using the provided framework. The script parses Linux authentication logs to detect brute-force login attempts by identifying entries containing "Failed password" and "Invalid user".

Implemented regex patterns to extract:

    Timestamp
    IP Address
    User Account

Stored extracted records and ensured they are written to a CSV file (suspects.csv) with correct headers.

What broke and how I fixed it:

Encountered multiple issues during development:

    Syntax errors caused the script to fail execution (e.g. missing : in function definitions).
    CSV writing initially failed due to incorrect file handling syntax.
    The script was flagged for using input() — after checking, I realised this came from comments or incorrect structure and removed it to comply with argparse requirements.
    Username extraction failed for different log formats, so regex patterns were adjusted to correctly handle both:
        "Failed password for <user> from"
        "Invalid user <user> from"

Also faced issues with missing IP extraction in some cases, which was fixed by ensuring regex search and match checks were correctly implemented.

When testing log_parser.py againts the metasploitable auth_live.log only one match was found, to verify this was the only match present the command line tool grep was used manually inside the log file to verify if this outcome was correct, grep showcased three results so an investigation inside the parser code was started, after analyzing the grep outcome and the parser code it was identified that the problem was inside the deduplication key. This only contained: dedup_key = (IP_Address, User_Account) which resulted in matches that had the combination of same username and IP address to only appear once in the output file, this was fixed by adding the value Timestamp inside the deduplication key: dedup_key = (Timestamp, IP_Address, User_Account)

Decisions I made and why:

Used a set to store extracted records temporarily in order to remove duplicate entries efficiently before converting them into dictionaries.

Compiled regex patterns outside of loops to improve efficiency and avoid repeated processing.

Kept the parsing logic simple and readable to make debugging easier.

What the tool output when I ran it against Metasploitable:

Not yet tested against Metasploitable logs. Successfully tested using provided fixtures — script runs without errors and generates CSV output.

Questions or things to revisit:

Need to test the parser against the full log datasets provided in the assignment. Ensure deduplication works correctly across larger datasets.

**What I built / changed:**

Developed `log_parser.py` using the provided framework. The script parses Linux authentication logs to detect brute-force login attempts by identifying entries containing **"Failed password"** and **"Invalid user"**.

Implemented regex patterns to extract:
- Timestamp
- IP Address
- User Account

Stored extracted records and ensured they are written to a CSV file (`suspects.csv`) with correct headers.

---

**What broke and how I fixed it:**

Encountered multiple issues during development:

- Syntax errors caused the script to fail execution (e.g. missing `:` in function definitions).
- CSV writing initially failed due to incorrect file handling syntax.
- The script was flagged for using `input()` — after checking, I realised this came from comments or incorrect structure and removed it to comply with argparse requirements.
- Username extraction failed for different log formats, so regex patterns were adjusted to correctly handle both:
  - "Failed password for \<user\> from"
  - "Invalid user \<user\> from"

Also faced issues with missing IP extraction in some cases, which was fixed by ensuring regex search and match checks were correctly implemented.

When testing log_parser.py againts the metasploitable auth_live.log only one match was found, to verify this was the only match present the command line tool grep was used manually inside the log file
to verify if this outcome was correct, grep showcased three results so an investigation inside the parser code was started, after analyzing the grep outcome and the parser code it was identified that the
problem was inside the deduplication key. This only contained:
dedup_key = (IP_Address, User_Account)
which resulted in matches that had the combination of same username and IP address to only appear once in the output file, this was fixed by adding the value Timestamp inside the deduplication key:
dedup_key = (Timestamp, IP_Address, User_Account)

---

**Decisions I made and why:**

Used a **set** to store extracted records temporarily in order to remove duplicate entries efficiently before converting them into dictionaries.

Compiled regex patterns outside of loops to improve efficiency and avoid repeated processing.

Kept the parsing logic simple and readable to make debugging easier.

---

**What the tool output when I ran it against Metasploitable:**

Not yet tested against Metasploitable logs.
Successfully tested using provided fixtures — script runs without errors and generates CSV output.

---

**Questions or things to revisit:**

Need to test the parser against the full log datasets provided in the assignment.
Ensure deduplication works correctly across larger datasets.

## [18-03-2026]

**What I built / changed:**

Tested `log_parser.py` against an external `auth.log` dataset placed at `field_tests/fixtures/auth.log` to validate the parser on a larger authentication log than the live Metasploitable sample.

The parser output was written to `toolkit/task1_evidence_collector/auth_log.csv`.

---

**What broke and how I fixed it:**

While validating the parser output, the first manual count was taken using an incorrect command structure, which caused `wc -l` to count the whole file rather than only the matching `grep` results. After correcting the command, the proper manual count of lines containing `Invalid user` or `Failed password` was obtained.

This made it possible to compare the raw log matches against the parser CSV output correctly.

---

**Decisions I made and why:**

Used `grep` as a manual validation method to compare the parser results against the source log. This was done to confirm that the parser was not missing a significant number of suspicious entries and that the regex patterns were working as expected on a larger dataset.

Kept the same parser logic and used the comparison to validate behaviour rather than changing code without evidence of failure.

---

**What the tool output when I ran it:**

The external `auth.log` returned 12,250 matching lines for `Invalid user` and `Failed password`.

The parser output file `auth_log.csv` contained 12,003 lines in total, including the header, meaning 12,002 extracted records.

The difference was small relative to the total dataset size and indicated that the parser was functioning correctly. The likely reason for the difference is that `grep` counts all raw matching lines, while the parser only writes structured records and removes duplicates.

---

**Questions or things to revisit:**

Need to test the parser against a fixture containing malformed or truncated lines and non-syslog timestamp formats once available, as the Session B `variant_auth.log` file was not present in the repository at the time of testing.


---
[18-03-2026]

**What I built / changed:**

Tested log_parser.py against a locally created adversarial log file:
field_tests/fixtures/local_variant_auth.log
 to simulate the missing Session B fixture. The file included ISO 8601 timestamps, standard syslog timestamps, malformed lines, and truncated entries to check how the parser behaves under different formats.

**What broke and how I fixed it:**

During testing, the parser successfully detected the correct lines, but the timestamp extraction was incorrect for ISO formatted entries.

For lines such as:

2026-03-14T10:11:04Z sshd[123]: Invalid user admin from 192.168.1.10

the parser output included extra parts of the line in the timestamp, for example:

2026-03-14T10:11:04Z sshd[123]: Invalid

This was caused by the logic:

Timestamp = " ".join(line.split()[0:3])

which assumes all timestamps follow the syslog format (Mar 14 10:11:06). This assumption does not hold for ISO timestamps, where the timestamp is only the first element of the line.

To fix this, the timestamp extraction was updated to use regex patterns for both formats:

syslog timestamps (Mar 14 10:11:06)

ISO 8601 timestamps (2026-03-14T10:11:04Z)

The parser now matches the correct timestamp format and extracts only the relevant portion of the line. Additionally, lines that do not contain a valid timestamp are safely skipped instead of causing incorrect output.

**Decisions I made and why:**

Used regex-based timestamp extraction instead of relying on string splitting, as it allows the parser to handle multiple log formats more reliably.

Did not attempt to force parsing of malformed or truncated lines, as the requirement is to produce structured and valid CSV output. Lines that do not contain all required fields (timestamp, IP, username) are ignored.

Created a local variant log file because the provided variant_auth.log fixture was not present in the repository, allowing similar edge cases to be tested without assuming unseen data.

What the tool output when I ran it:

After applying the fix, which was changing the timestamp regex by adding one for sys log types and another one for ISO log types:
syslog_timestamp_pattern = re.compile(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}")
iso_timestamp_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

 the parser correctly extracted timestamps for both formats and produced clean CSV output such as:

2026-03-14T10:11:04Z,192.168.1.10,admin
2026-03-14T10:11:05Z,192.168.1.10,admin
Mar 14 10:11:06,10.0.0.5,root
Mar 14 10:11:09,192.168.1.10,admin

Malformed and truncated lines were ignored as expected, and the script completed execution without errors.

**Questions or things to revisit:**

For next time do not assume log patterns but research what patters look like so the parser captures all output.

## Week 2 — Task 2: Network Cartographer

### [DATE] — Session A

**Metasploitable scan output (paste key results):**
```json

```

**Observations — what services did you find? What do the banners tell you?**



### [DATE] — Session B



---

## Week 3 — Task 3: Access Validator

### [DATE] — Session A



### [DATE] — Session B



---

## Week 4 — Task 4: Web Enumerator

### [DATE] — Session A

**Metasploitable web recon output:**


**HTML comments found:**


**Sensitive paths found:**



### [DATE] — Session B



---

## Week 5 — Vulnerability Hunt

> This section is your mission log. Update it in real time during the session.
> Benji does not write the mission log after the mission. He writes it during.

### Pre-Hunt Checklist

- [ ] All four toolkit tools pass their field tests locally
- [ ] `requirements.txt` is up to date (`pip freeze > requirements.txt`)
- [ ] `AI_LOG.md` is current
- [ ] `vulnerability_hunt/exploit.py` — argument parsing in place
- [ ] `vulnerability_hunt/fix.py` — argument parsing in place
- [ ] `vulnerability_hunt/REPORT.md` — headings populated, ready to fill
- [ ] Git remote confirmed, can push
- [ ] Tags w1, w2, w3, w4 in place

### Hunt Log

**[TIME] — Diagnosis phase:**


**[TIME] — Vulnerability identified:**


**[TIME] — Exploit development:**


**[TIME] — Flag retrieved:**
```
FLAG:
```

**[TIME] — Remediation:**


**[TIME] — Final commit and push:**

