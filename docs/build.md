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

Developed log_parser.py using the provided framework. The script parses Linux authentication logs to detect brute-force login attempts by identifying entries containing "Failed password" and "Invalid user".

Implemented regex patterns to extract:

    Timestamp
    IP Address
    User Account

Stored extracted records and ensured they are written to a CSV file (suspects.csv) with correct headers.

**What broke and how I fixed it:**

Encountered multiple issues during development:

    Syntax errors caused the script to fail execution (e.g. missing : in function definitions).
    CSV writing initially failed due to incorrect file handling syntax.
    The script was flagged for using input() — after checking, I realised this came from comments or incorrect structure and removed it to comply with argparse requirements.
    Username extraction failed for different log formats, so regex patterns were adjusted to correctly handle both:
        "Failed password for <user> from"
        "Invalid user <user> from"

Also faced issues with missing IP extraction in some cases, which was fixed by ensuring regex search and match checks were correctly implemented.

When testing log_parser.py againts the metasploitable auth_live.log only one match was found, to verify this was the only match present the command line tool grep was used manually inside the log file to verify if this outcome was correct, grep showcased three results so an investigation inside the parser code was started, after analyzing the grep outcome and the parser code it was identified that the problem was inside the deduplication key. This only contained: dedup_key = (IP_Address, User_Account) which resulted in matches that had the combination of same username and IP address to only appear once in the output file, this was fixed by adding the value Timestamp inside the deduplication key: dedup_key = (Timestamp, IP_Address, User_Account)

**Decisions I made and why:**

Used a set to store extracted records temporarily in order to remove duplicate entries efficiently before converting them into dictionaries.

Compiled regex patterns outside of loops to improve efficiency and avoid repeated processing.

Kept the parsing logic simple and readable to make debugging easier.

What the tool output when I ran it against Metasploitable:

Not yet tested against Metasploitable logs. Successfully tested using provided fixtures — script runs without errors and generates CSV output.

Questions or things to revisit:

Need to test the parser against the full log datasets provided in the assignment. Ensure deduplication works correctly across larger datasets.

---

## [18-03-2026]

**What I built / changed:**

Tested log_parser.py against an external auth.log dataset placed at field_tests/fixtures/auth.log to validate the parser on a larger authentication log than the live Metasploitable sample.

The parser output was written to toolkit/task1_evidence_collector/auth_log.csv.

---

**What broke and how I fixed it:**

While validating the parser output, the first manual count was taken using an incorrect command structure, which caused wc -l to count the whole file rather than only the matching grep results. After correcting the command, the proper manual count of lines containing Invalid user or Failed password was obtained.

---

**Decisions I made and why:**

Used grep as a manual validation method to compare the parser results against the source log.

---

**What the tool output when I ran it:**

The external auth.log returned 12,250 matching lines. The parser output contained 12,002 extracted records.

---

**Questions or things to revisit:**

Need to test malformed logs later.

---

## [18-03-2026]

**What I built / changed:**

Tested log_parser.py against a locally created adversarial log file:
field_tests/fixtures/local_variant_auth.log

---

**What broke and how I fixed it:**

Timestamp extraction failed for ISO format. Fixed using regex patterns.

---

**Decisions I made and why:**

Used regex instead of split for flexibility.

---

**What the tool output when I ran it:**

Correct structured output.

---

**Questions or things to revisit:**

Research log formats better.

---

## Week 2 — Task 2: Network Cartographer

[31-03-2026] — Session A

Metasploitable scan output (paste key results):

**What I Built / Changed**

Developed a TCP threaded port scanner that scans a range of ports or specific ports concurrently. The main purpose of the scanner is to find open ports, grab a service name/version banner if available, and attempt a TCP connection.

The purpose of this tool is to act as the first reconnaissance tool to find vulnerabilities in a system, as a vulnerability is often exposed through open ports or banners being displayed. These banners or open ports can then be exploited by searching for known vulnerabilities. This will be covered in Part B of this documentation.

The workflow of the scanner is as follows:

Read CLI arguments using argparse
Parse the port input into usable integers
Create worker threads to concurrently scan ports
Scan each port individually using TCP connections
If a port is open, attempt to grab a banner from the service
Collect raw results from each thread
Sort results cleanly in a readable structure
Build the JSON output file
Print the results to the terminal and save them to the JSON file
What broke and how I fixed it

No major logical errors were encountered during the development of the port scanner itself. However, when updating the repository with fixes and field_tests from the origin main/template, Git introduced merge conflict markers:


These corrupted the scanner as they are not valid Python syntax and caused execution failures.

The fix:

Manually removed all merge conflict markers and ensured only the correct version of the code remained. After this, the script executed correctly again.

**Decisions I made and why:**

Used socket.connect_ex() instead of connect() to safely attempt connections without crashing the script
Implemented threading using ThreadPoolExecutor to improve performance, as scanning ports sequentially would be too slow
Included a timeout value to prevent the scanner from hanging on unresponsive ports
Ensured that every open port always includes a "banner" field, even if empty, to match the required output contract
Sorted results by port number to improve readability and consistency in output
What the tool output when I ran it against Metasploitable:

The output located at:

toolkit/task2_network_cartographer/recon_results.json

shows that ports 21, 22, 80, 445, and 631 are open and listening for traffic.

A clear distinction that can be made from looking at the JSON output is that port 21 (FTP) and port 22 (SSH) display banners that provide useful information which can later be searched for known vulnerabilities and therefore exploited.

Example:

"port": 21,
"banner": "220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [172.16.19.101]"

This exposes that the server running FTP is ProFTPD and its version is 1.3.5. This information can be very useful when trying to exploit the vulnerability or finding a fix to secure and harden it.

Similar scenario with SSH on port 22:

"port": 22,
"banner": "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13"

Here the banner displays the SSH version and the operating system the service is running on, in this case Ubuntu.

Ports such as 80, 445, and 631 did not return banners. This is expected behaviour, as some services do not send data immediately upon connection and require protocol-specific interaction before responding.

Inside the live target machine used to command:

ss -tln

to view actually which tcp ports were actually open, open does not automatically mean working as some ports could be filtered by a firewall therefore they do appear as open on the local machine but will refuse some types of connections such as the one requested by scan.py tool, to test this theory after identifying all open ports (=0) a manual tcp connection was reauested from the kali machine to the target machgine using netcat, command:

nc -vz -w 2 <ip> <port>

example:

port open identified manually that did not appear in the JSON output, port 139 (NetBIOS Session Service)

result:
172.16.19.101: inverse host lookup failed: Host name lookup failure : Resource temporarily unavailable
(UNKNOWN) [172.16.19.101] 139 (netbios-ssn) : Connection timed out

here connection timed out usually suggests there is a firewall blocking the tcp connection.


**Questions or things to revisit:**

Next step is to research and understand how banner information can be used to exploit and secure services, and what can be done with the open ports identified.

It is important to remember that some services have their ports open but do not display banners because they require a request interaction (for example port 80 HTTP). However, this does not mean the open port cannot be exploited. This is something very important to consider and test later on.

[01-04-2026] — Session B

**What I built / changed:**

Based on the initial scanner output (scan.py), Analysed the banner information and immediately searched for relevant CVEs related to the FTP service. After researching and understanding the vulnerability, I developed an automated exploit targeting the service.

Created an exploit script that connects to the FTP service and sends specific commands to copy a sensitive file (/etc/passwd) on the target system to a web-accessible directory. The script then retrieves the file via HTTP and prints the output, proving successful exploitation.

**What broke and how I fixed it:**

The first exploit draft was too basic. It worked at a very simple level but lacked structure and important validation steps, such as verifying the service banner before exploitation and handling output properly.

Fix:

Refactored the exploit into a modular structure using functions. Each function was designed to handle a specific task, such as banner verification, sending FTP commands, and retrieving the file. Also replaced hardcoded values with variables to improve flexibility and automation. Added proper output handling to make results clearer and more usable.

**Decisions I made and why:**

Compared the exploit results with the actual file on the target machine by manually connecting to the FTP service. Used netcat to send the same commands and verified that the copied file matched the retrieved output. This was done to confirm the exploit was working correctly and not producing false results.

Also ensured the file was copied to a web-accessible path (/var/www/html) so it could be reliably retrieved using HTTP, instead of using temporary directories that are not accessible externally.

What the tool output when I ran it against Metasploitable:

The exploit successfully identified the vulnerable service, copied the /etc/passwd file to the target system, and retrieved it via HTTP. The output displayed system user entries such as:

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...

This confirms that the exploit worked as intended and that sensitive data can be accessed due to the vulnerability.

**Questions or things to revisit:**

Need to further explore how different vulnerabilities expose services and how the extracted information (such as versions and banners) can be used to identify more complex exploits. Also want to look into implementing a proper fix for the vulnerability and understanding how to secure the service against this type of attack.


## Week 3 — Task 3: Access Validator

### [DATE] — Session A

### [DATE] — Session B

---

## Week 4 — Task 4: Web Enumerator

### [DATE] — Session A

**Metasploitable web recon output:**

**HTML comments found:**

**Sensitive paths found:**

---

### [DATE] — Session B

---

## Week 5 — Vulnerability Hunt

### Pre-Hunt Checklist

- [ ] All four toolkit tools pass their field tests locally
- [ ] requirements.txt is up to date
- [ ] AI_LOG.md is current
- [ ] exploit.py ready
- [ ] fix.py ready
- [ ] REPORT.md ready
- [ ] Git push works
- [ ] Tags in place

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
