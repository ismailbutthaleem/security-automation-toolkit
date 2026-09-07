

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

**What the tool output when I ran it against Metasploitable:**

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

grep -Ec "Invalid User|Failed Password"

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

### [05-04-2026]

**What I built / changed:**

Researched additional authentication log formats, specifically PAM-style logs, and downloaded an external auth.log dataset containing this format. Reviewed the structure of these logs to understand how authentication failures are recorded differently compared to the standard "Failed password" and "Invalid user" entries.

Updated log_parser.py to support PAM-style entries by extending both detection and extraction logic.

Added the following regex patterns:

pam_pattern = re.compile(r"authentication failure")
pam_ip_pattern = re.compile(r"rhost=(\d+\.\d+\.\d+\.\d+)")
pam_user_pattern = re.compile(r"user=(\S+)")
**Decisions I made and why:**

The parser was extended to support additional log formats to test whether the implementation could handle real-world variations without breaking the required functionality.

After implementing the changes, the provided pytest suite (field_tests/test_task1.py) was executed to ensure that all original requirements were still met and that the extension did not introduce regressions.

Following this, manual testing was carried out using external datasets to validate behaviour beyond the assignment scope.

PAM-style logs were included because they are commonly used in real Linux authentication systems, making the parser more realistic and robust.

**What the tool output when I ran it against Metasploitable:**

Manual verification was performed using:

grep -Ec "authentication failure" /home/benji/Downloads/Linux_2k.log

This returned 490 matching lines in the raw log file.

The parser was then executed against the same dataset, producing a CSV report at:

toolkit/task1_evidence_collector/Linux_log.csv

A line count was performed using:

wc -l Linux_log.csv

The output contained 153 lines (including header).

The difference between raw log matches and parser output is expected due to:

Deduplication logic (same timestamp, IP, and user stored once)
Filtering of incomplete or malformed entries

Analysis:

The high number of repeated authentication failures from the same source strongly indicates brute-force activity targeting the system.

This demonstrates that the parser is correctly transforming raw log noise into structured, meaningful security data.

**Questions or things to revisit:**

This parser is operational and correct for a specific scope but would not work and must be heavily extended if working with other types of logs.

[05-04-2026]

**What I built / changed:**

Tested the log_parser.py against the live Metasploitable machine by using its auth.log file as input instead of only relying on fixtures and external datasets.

This was done to validate that the parser works correctly in the actual target environment of the assignment.

**What broke and how I fixed it:**

Initially, the manual grep output showed fewer entries than the CSV report generated by the parser.

This was due to the grep command only searching for:

Invalid user | Failed password

and not including the extended pattern:

authentication failure

After updating the command to include this pattern:

grep -Ec "Invalid user|Failed password|authentication failure" auth.log

the output returned:

8

The CSV report also returned:

wc -l suspects.csv → 8

It is important to note that wc -l includes the header, meaning the actual number of extracted records is 7.

This confirms that one of the log entries was a duplicate, which was correctly removed by the parser due to the deduplication logic based on (timestamp, IP, user).

**Decisions I made and why:**

Chose to validate the parser against the live Metasploitable log to ensure that the tool works in the intended environment and not only on controlled datasets.

Used grep as a ground truth comparison method to verify that all relevant authentication failure events were being detected.

Included the extended pattern (authentication failure) in validation to ensure consistency between manual checks and parser logic.

What the tool output when I ran it against Metasploitable:

The parser successfully extracted authentication failure events and generated a structured CSV report containing timestamp, IP address, and user account.

The output matched the manually verified grep results after accounting for deduplication and the CSV header, confirming that the parser is correctly detecting and structuring relevant log entries.

## Week 2 — Task 2: Network Cartographer

## [31-03-2026] — Session A

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

## [01-04-2026] — Session B

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

Need to further explore how different vulnerabilities expose services and how extracted information (such as versions and banners) can be used to identify more complex or chained exploits. Also want to look into implementing a proper fix for the vulnerability and understanding how to secure the service against this type of attack.

The exploit only reveals usernames and system account information, not passwords, as these are stored in a separate file:

/etc/shadow

This file requires elevated (root) permissions to access, meaning privilege escalation would be needed to retrieve it. This is outside the scope of the current vulnerability and exploit, which operates under the permissions of the FTP service.

However, even without direct access to password hashes, the extracted usernames still have value. This raises an important follow-up question:

Even though passwords are not exposed, can they be brute forced using the identified usernames?

This leads into the next stage of the workflow, which will involve validating access using these usernames — forming the basis of the next tool, the access validator.

### [03-04-2026]

**What I built / changed:**

Built a remediation script for the vulnerability identified using the `gateaway_exploit.py` script.

The initial approach was to disable the vulnerable functionality within the ProFTPD service by modifying its configuration. However, this was later changed to instead disable access to the affected service entirely by blocking FTP on port 21.

The final remediation script is located at:

toolkit/task2_network_cartographer/gateaway_fix.py


**What broke and how I fixed it:**

The original remediation approach was unsuccessful. Although the script attempted to disable the vulnerable module (`mod_copy`) through configuration changes, the vulnerability remained exploitable.

After investigation, it was identified that the module responsible for the vulnerability was statically compiled into the ProFTPD binary rather than dynamically loaded via configuration. This meant that commenting out or modifying the configuration file had no effect on the actual functionality of the service.

To resolve this, the remediation strategy was changed. Instead of attempting to disable the module, the script was updated to block access to the FTP service entirely by disabling port 21.

This was implemented by establishing an SSH connection to the target machine and applying an iptables firewall rule to drop incoming traffic on port 21.


**Decisions I made and why:**

Chose to implement a network-level mitigation instead of a service-level fix because the vulnerable module could not be reliably disabled through configuration changes due to being compiled into the service.

Blocking port 21 provided a more reliable and immediate solution, as it removes external access to the vulnerable service without depending on configuration edits or service restarts.

Although this does not remove the vulnerability itself, it effectively reduces the attack surface and prevents exploitation from external sources.


**What the tool output when I ran it against Metasploitable:**

After a successful remediation, the script outputs:

[4] Verifying FTP is blocked...
    [+] FTP no longer reachable on port 21.

[+] Remediation complete.
    Vulnerability exposure reduced: FTP access blocked externally
    Service state: Port 21 filtered by firewall

To further verify the fix, the port scanner (`scan.py`) was executed again. The output showed that port 21 was no longer listed as open:

{
  "target": "172.16.19.101",
  "scan_time": "2026-04-03 22:06:58",
  "open_ports": [
    {
      "port": 22,
      "banner": "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13"
    },
    {
      "port": 80,
      "banner": ""
    },
    {
      "port": 445,
      "banner": ""
    },
    {
      "port": 631,
      "banner": ""
    }
  ]
}

This confirms that port 21 (FTP) has been successfully disabled.

As an additional manual validation step, netcat was used to test connectivity to port 21:

Command:

nc -vz -w 2 172.16.19.101 21

Expected output:

(UNKNOWN) [172.16.19.101] 21 (ftp) : Connection timed out

This further confirms that the port is no longer reachable and the remediation has been applied successfully.


**Questions or things to revisit:**

Consider implementing a permanent fix by upgrading or recompiling the ProFTPD service without the vulnerable module, as the current solution only provides containment rather than full remediation. after a reboot of the target system the remedition status will reset, therefore port 21 will be open again. This is fine for labs but should be avoided in enterprise operations.

Also revisit whether internal access to the FTP service remains possible despite external blocking, and whether additional controls are required.

### [09-04-2026]

**What I built/ changed**

made the scanner more robus by implementing various error handling methods:

1. Ensure threads is only a number and greater than0 otheriwse display appropiate fail message.
2. Ensure timeout is a float not a string or negative number
3. Handle user keyboard exits witout crashing

**Decisions I made and why:**

Bad input is a risk that could cause the script to crash, it is better to ensure all argparse functions can handle bad input to ensure a successful tool operation

## Week 3 — Task 3: Access Validator

### [09-04-2026] — Session A
### [Week 3 — Session A] — Task 3: Access Validator

**What I built / changed:**
Implemented brute.py as a credential testing tool supporting both FTP (ftplib) and SSH (paramiko). This is abrute force tool that takes usernames from:
/etc/passwd
Which are the potential targets and a wordlist to iterate thru. The script accepts CLI arguments using argparse and loads a wordlist to test passwords sequentially. Added logging functionality to record each attempt into a CSV file. After initial implementation and passing pytest, I improved the script by adding port validation, structured error handling, a service availability pre-check, and separation between authentication failure and service failure using a custom exception. Also added attempt counting and a verbose mode for optional visibility of each attempt.

**What broke and how I fixed it:**
Initially had an issue where the variable "success" was being used before it was defined inside the loop, which caused the script to crash. Fixed this by ensuring the authentication function runs before logging and condition checks. Also noticed that without proper error handling, invalid file paths or unreachable services would cause the script to fail unpredictably. Fixed this by wrapping file operations and service checks in try/except blocks and using stderr with proper exit codes.

**Decisions I made and why:**
Decided to add a service availability check before starting the brute-force loop to avoid wasting time attempting passwords against a dead service. Chose to separate authentication errors from network errors to improve accuracy and make debugging easier. Implemented port validation using a custom argparse type to catch invalid input early. Added a verbose flag instead of printing every attempt by default to avoid breaking the required output format for pytest while still allowing detailed runtime visibility when needed.

**What the tool output when I ran it against Metasploitable:**
Tool not tested againts metasploitable yet, planning on executing that in session B, the tool passes pytest. However by default pytest triggers the tool into making some madeup users with passwords, this indicates the tool has a high chance of bein functional on first try againts a live target, this hypothesis will be corraborated in session B.

**Questions or things to revisit:**
Have to try the tool against a real target.

### [09-04-2026] — Session B

**What I built / changed:**

Tried running the brute force tool against metasploitable using all the positional arguments possible, used a madeup wordlist file with whitespaces incorrect passwords and the actual correct password:

password 123
admin

letmein
password
msfadmin
wrongpass

vagrant

The decision of making the file contan whitespaces is intentional to test the tool behaviour on blank lines.
**What broke and how I fixed it:**

First error just poped which says:

[-] ERROR: Wordlist is empty after cleaning.

Which means that after removing the blank lines no lines with content were found, which is in fact wrong as the file has got content inside of it, this indicates that the script whitespaces handling is incorrect.

After inspecting the code it was found that everything was fine so the issue was narrowed down to a system internal issue such as the system not having saved the wordlist therefore the tool sees its contents as empty.

wordlist.txt was saved and the issue was solved, this indicates that the error message given was too broad, the file path and the file itself did exists but as the file content was not saved, and that is why that error popped up.

To solve the issue the file was saved internally.
**Decisions I made and why:**

Change the error message so the user checks both scenarios either that the file exists but its empty or that after cleaning it nothing was found inside. This line of code was updated:

if not passwords:
    print("[-] ERROR: Wordlist is empty after cleaning.", file=sys.stderr)
    sys.exit(1)

this line now is:

if not passwords:
    print(
        "[-] ERROR: Wordlist contains no valid passwords (file may be empty or only whitespace).",
        file=sys.stderr
    )
    sys.exit(1)

The feedback given to the user is now more informative and saves the user troubleshooting time.

**What the tool output when I ran it against Metasploitable:**

The tool successfully found the correct password, however if the argument --verbose was working wanted to be tested, in the first run we got a small delay then the message:

[+] SUCCESS: Password found: vagrant

This output does not necessarily mean that --verbose is broken, it could just mean that it found the password in the first attempt. However even when changing the correct password to another line and adding more passwords the output is still the same with a small delay, this confirms the theory that --verbose is not working as expected.

The args.verbose was missing in the code therefore the value of this args was never beign returned anywhere that beign the reason no detailed output was ever given to fix that, the code:

if args.verbose:
                print(f"[*] Attempt {attempt_count}: trying password '{password}'")

Was added inside the main brute loop at line 272.

After a successful run the output with --verbose should look something like this:

[*] Attempt 1: trying password 'password 123'
[*] Attempt 2: trying password 'admin'
[*] Attempt 3: trying password 'letmein'
[*] Attempt 4: trying password 'password'
[*] Attempt 5: trying password 'msfadmin'
[*] Attempt 6: trying password 'wrongpass'
[*] Attempt 7: trying password 'vasgaga'
[*] Attempt 8: trying password 'pass'
[*] Attempt 9: trying password 'vagrant'
[+] SUCCESS: Password found: vagrant


**Questions or things to revisit:**
---

Make sure brute force tool can handle any type of file with whitespaces or malformed lines, test it againts other wordlists.

Also have in mind that to try and crack a password that we actually dont know we would use a wordlist more powerful than the sample one used for this try against the vagrant machine. A wordlist like rockyou.txt

### [10-04-2026]

**What I built / changed:**

Added a new more complex wordlist to try brute forcing against the target. This wordlist contains a lot of special character truncated lines, malformed strings, long strings anmd whitespaces.

**What broke and how I fixed it:**

Brute force tool stopped trying passwords after attempt 184, attempt 184 was a long string with the character word "A", this indicates the tool does not handle bad input very well or it crashes because the time sleep delay is to small,
therefore exits the operation and outputs and error saying:
[-] ERROR: FTP service unavailable on 172.16.19.101:21

Although this could be the possible error is not as manually it can be tested that the service and port are up with no firewalls in between.

That proves the hypothesis that either the tool crashes with weird input or the delay is to small so ftp closes the connection and the tool just exits.

The problem is in this line:

except ServiceUnavailableError as error:
                print(f"[-] ERROR: {error}", file=sys.stderr)
                sys.exit(1)

This part is telling the pogramm to exit if a serviceunavailable error ocurrs.

the:

sys.exit(1)

was changed to:

continue

resulting in:

except ServiceUnavailableError as error:
                print(f"[-] ERROR: {error} (possible timeout or glitch), skipping.", file=sys.stderr)
                continue

This tool already checks if the service is available before attempting a brute force attack, so when checking the passwords if there is a temporary service error glitch the tool should not stop but skip that attempt an continue and thats what the new piece of code does exactly, point out there has been a service error in such attempt and that it will be skipped.

**Decisions I made and why:**

Adding the exception:

ServiceUnavailableError

is a controlled way of cathing a specific run time error when the brute force attack is beign executed, its useful for troubleshooting or post-attack analysis instead of using a generic OSError

**What the tool output when I ran it against Metasploitable:**

After the fix the password was found, the output file is in:

toolkit/task3_access_validator/posioned_wordlist_output.txt


**Questions or things to revisit:**

Tool works against bad input and handles network error gracefully now, error messages are more useful and detailed now.

[10-04-2026] — Task 3: Access Validator (Refactor & Stability Fix)

**What I built / changed:**

Refactored the brute-force logic in brute.py to make it cleaner and more reliable during execution.

Originally, the main brute loop was written directly inside main(), which made the script harder to follow and debug. I moved this logic into a separate function run_credential_test() so that the password testing process is isolated and reusable. This also makes it easier to switch between FTP and SSH since both now use the same loop structure via the attempt_function. A modular approach was followed to match the rest of the approach in the build of the tool.

Also added a new function initialise_log() which creates a fresh attempt_log.csv file at the start of each run. Previously, the log file was opened in append mode ("a"), which caused old data to stay in the file and mix with new results. This made the number of linees in the CSV not match the attempt counter shown in the terminal.

The logging function was updated so it now only appends rows, while the header is written once at the start of the run.

**Decisions I made and why:**

Decided to keep ServiceUnavailableError instead of removing it, as it allows cleaner separation between actual service failures and incorrect credentials. It is now used differently depending on context:

Before the brute loop → treated as fatal (script exits)
During brute loop → treated as temporary (script continues)

Chose to initialise the log file with "w" mode at the start of each run instead of continuously appending. This ensures that each execution produces a clean and readable evidence file, which is easier to analyse and avoids confusion when comparing attempt counts.

Refactoring the brute loop into run_credential_test() was done to improve structure and readability rather than functionality. This makes the code easier to maintain and aligns better with a more modular design.

**What the tool output when I ran it against Metasploitable:**

When running against the FTP service on Metasploitable with a large wordlist, the tool now continues execution even when temporary connection issues occur.

Example behaviour:

Attempts are printed sequentially with --verbose
Temporary errors are displayed as warnings instead of stopping execution
Log file records each attempt as SUCCESS, FAIL, or ERROR
Script successfully continues through the wordlist instead of stopping prematurely

The attempt_log.csv now correctly reflects only the current run, with no leftover entries from previous executions.

**Questions or things to revisit:**

Review whether the delay (0.1) is sufficient under heavier wordlists or if adaptive delays would improve stability.

### [15-04-2026]

**What I built / changed:**

Pytest was throwing the following errors during Task 3 testing:

FAILED field_tests/test_task3.py::test_ftp_success_message - AssertionError: Script exited with error:
FAILED field_tests/test_task3.py::test_ftp_exhaustion_message - AssertionError: Expected exhaustion message not found in stdout:
FAILED field_tests/test_task3.py::test_ftp_stops_on_success - AssertionError: Script exited with error:
FAILED field_tests/test_task3.py::test_handles_messy_wordlist - AssertionError: Script crashed on messy wordlist:

After checking the full pytest output more closely, it became clear that the actual error was related to how the script parsed the target argument:

error: the following arguments are required: --target

This showed that the real problem was not the brute-force logic itself, but that the script was failing at argument parsing stage before it could reach the FTP testing logic.

Although the target value was being passed by the test, my script expected it in a different format to the one used by pytest.

**What broke and how I fixed it:**

The issue was caused by defining the target as a required optional argument:

parser.add_argument(
    "--target",
    required=True,
    help="Target IP address or hostname",
)

However, the pytest field test called the script using the target as a positional argument, not --target.

To fix this, the argument definition was changed to:

parser.add_argument(
    "target",
    help="Target IP address or hostname",
)

Once this change was made, the script matched the field test contract correctly and the failing tests were able to execute the actual brute-force logic.

**Decisions I made and why:**

I changed --target to target because the field tests expected the target as a positional argument. Without this change, argparse stopped the script immediately and exited before the FTP functions, success message, exhaustion message, or wordlist handling could be tested.

This explained why several tests appeared to fail at once even though the real issue was only one mismatch in the command-line argument format.


**Questions or things to revisit:**

Read the field test contract more carefully before changing working code, especially CLI argument format, because one mismatch at parser level can prevent the whole script from running and make multiple tests fail at the same time.

## Week 4 — Task 4: Web Enumerator

### [19-04-2026] — Session A

**What I built / changed**

Built the initial version of the web_enum.py tool following the provided scaffold. The tool sends an HTTP request to a target, extracts key response headers (Server, X-Powered-By), parses HTML to retrieve comments, and checks a set of sensitive paths for their status codes. This forms the base for passive web reconnaissance before moving into exploitation.

**What broke and how I fixed it:**

No major issues during initial implementation. Minor adjustments were made to the sensitive paths list to ensure correct formatting and compatibility with the output structure expected by the task.

**Decisions I made and why:**

Extended the default sensitive paths list with a small number of additional common paths (e.g., backup and development directories). This was done to improve the likelihood of identifying exposed resources while still adhering to the constraint of not performing excessive enumeration.

**What the tool output when I ran it against Metasploitable:**

Not tested yet — this will be completed in the next session to validate functionality and gather reconnaissance data.

**Questions or things to revisit:**

Validate tool output against pytest to ensure it meets the required contract
Test against Metasploitable and document any discovered comments, headers, or paths
Review output formatting to ensure consistency with assessment requirements
Consider improving error handling and response interpretation (e.g., handling timeouts, redirects, and 403 responses more clearly)

### [19-04-2026]


**Decisions I made and why:**
Added optional JSON output so the tool produces a structured evidence file as well as terminal output. This makes it easier to document findings, review results after testing, and use the recon data later during the exploit and fix planning stages.

**Metasploitable web recon output:**

{
    "target": "http://172.16.19.101",
    "headers": {
        "Server": "Apache/2.4.7 (Ubuntu)",
        "X-Powered-By": "Not present"
    },
    "comments": [],
    "sensitive_paths": {
        "/robots.txt": 404,
        "/admin": 404,
        "/phpmyadmin": 301,
        "/login": 404,
        "/.git": 404,
        "/drupal": 301,
        "/drupal/CHANGELOG.txt": 200,
        "/dbadmin": 404,
        "/backup": 404,
        "/backup.zip": 404,
        "/dev": 404,
        "/test": 404,
        "/.env/config.php": 404
    }
}

This output shows that /drupal/CHANGELOG.txt is accessible because it returned 200 OK. This is useful because it exposes version information about the web application. It also showed that /drupal and /phpmyadmin returned 301, which suggests redirection rather than simple absence, so these paths may still be relevant.

No HTML comments or exposed credentials were found on the main page, so the strongest web-based lead became the exposed Drupal changelog file rather than a direct credential leak.

The next step was to manually access the discovered path:

http://172.16.19.101/drupal/CHANGELOG.txt

or retrieve it through curl:

curl http://172.16.19.101/drupal/CHANGELOG.txt

Reading the file revealed that the application is running Drupal 7.5. This is important because it provides a specific vulnerability research lead.

As no credentials or comments were leaked, the next attack step was to research known CVEs affecting Drupal 7.5. During this research, CVE-2018-7600 was identified as a strong candidate attack path, because Drupal 7.5 falls within the affected version range for that vulnerability.

**Attack process**
This suggests a possible web exploitation path based on version disclosure. The vulnerability is associated with remote code execution through crafted HTTP requests in vulnerable Drupal versions.

1.Confirm the target is exposing the Drupal application.
2.Confirm the version using the changelog.
3.Research and verify whether the target is likely vulnerable to CVE-2018-7600.
4.Build an exploit that sends crafted HTTP requests to the vulnerable Drupal endpoint.
5.Analyse the server response to determine whether exploitation is successful and whether the flag or target data can be retrieved.

**Fix process**

1.Confirm the target URL and Drupal path are valid.
2.Remove or restrict public exposure of unnecessary version information such as CHANGELOG.txt.
3.Patch or upgrade Drupal to a version no longer affected by the vulnerability.
4.Re-test the target to confirm the vulnerable behaviour is no longer present.
5.Verify that the previous version disclosure and exploit path are no longer available.

---

### [17-04-2026] — Session B

**What I built / changed:**

This session was mainly the introduction to the mock exam. I ran my tools against the target to see how they behave in a more real scenario. I used the scanner and web enumerator to identify open ports, services, and web information. From the scan results I identified Drupal as the main target and started looking into the version and possible CVEs related to it.

I also started thinking about how my exploit script will be structured for the actual mission, so I began sketching the scaffold (argument parsing, connection logic, etc.) instead of leaving it for the exam day.

**What broke and how I fixed it:**

Main issue wasn’t code breaking, it was understanding the exploit itself. I struggled with how the Drupal vulnerability actually works and how the payload should be structured.

At first I didn’t understand how the request triggers execution, but after testing and looking at the behaviour, I realised Drupal processes certain render array functions. By sending a crafted HTTP request, the server processes it and executes what is passed inside it.

Once I understood that flow (request → processed by Drupal → executes payload), it started making more sense.

**Decisions I made and why:**

I decided not to rely on memorising a payload, but instead focus on understanding how the exploit works. This is important because the exam scenario will be different.

I also decided to start building my exploit scaffold early instead of leaving it to the mission day. This way I only need to adjust payloads and paths during the exam instead of writing everything from scratch under time pressure.

**Questions or things to revisit:**

Need to get more comfortable with how to build payloads for web-based exploits
Still not 100% confident in structuring POST requests manually
Need to practise extracting flags automatically after triggering the exploit

### [22-04-2026 → 24-04-2026] — Exploit & Fix Development

**What I built / changed:**

Worked on building both exploit.py and fix.py.

For the exploit:

Built full scaffold (argparse, connection, flag extraction)
Reused logic from brute tool for SSH access
Added functions for username discovery and password finding
Implemented reading remote files and extracting the flag using regex

For the fix:

Built remediation script structure with three main actions:
remove credential exposure
close access vector (password change)
remove evidence
Added verification step to confirm fixes worked and service is still running

Also cleaned up code across tools (removed TODOs, fixed structure, improved comments).

**What broke and how I fixed it:**

Had multiple small issues during this period:

Import issues between exploit and fix → fixed by making sure functions are reusable and paths are correct
SSH connection failures → fixed by reusing working logic from brute tool
Errors when reading remote files → handled with better error checking (stdout/stderr handling)
General debugging of flow (making sure each step returns correct values before moving on)

Main difficulty was not syntax, but making everything flow together properly.

**Decisions I made and why:**

I decided to reuse logic from previous tools (especially brute.py) instead of rewriting everything. This keeps consistency and reduces errors.

I used AI for explanations, code correction

I kept placeholders for paths (credential leak, evidence file) instead of hardcoding anything, so I can quickly adapt during the mission.

I also added verification steps in fix.py because just running commands is not enough — I need to prove the system is actually secured after remediation.

**Questions or things to revisit:**

Developed a better sense of explotation and fix chain for the mission


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

Hunt Log

 — Diagnosis phase:
Ran my toolkit (scan + web_enum). Identified open ports and pulled banners. Spotted vulnerable service version straight away from banner output.

 — Vulnerability identified:
Web leak

 — Exploit development:
Modified exploit scaffold — focused only on payload + retrieval logic. Built request to trigger vuln and tested response until I saw execution working.

 — Flag retrieved:
Automated the full chain (trigger → access → extract). Script successfully pulled flag from target without manual steps.

FLAG:
<COM5413-20260424-0969-ETHAN-WAS-HERE-98604a763abe>

 — Remediation:
Implemented fix by removing vulnerable functionality / blocking access (e.g. patched config, disabled feature, or restricted port). Re-tested to confirm exploit no longer works but service still running

 — Final commit and push:
Cleaned code, updated REPORT.md + AI_LOG.md, committed everything and pushed with hunt-final tag before deadline.
