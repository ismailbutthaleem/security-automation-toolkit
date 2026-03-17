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


---

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

