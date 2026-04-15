# AI Transparency Log — The Benji Protocol
**Student Name:** Ismail Butt Haleem
**Student ID:** 2433887
=======
**Student Name:**
**Student ID:**


---

## Policy Summary

You may use GenAI tools (ChatGPT, GitHub Copilot, etc.) to debug, explain,
or refactor code. You must document every substantive use in this log.

You may NOT paste the Vulnerability Hunt scenario into an AI tool and ask
for the solution. Code you cannot explain during the session will be flagged.

---

## Log Format

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
| Example | Task 1 | "Write a regex to extract IP addresses from auth.log" | Provided `\b(?:\d{1,3}\.){3}\d{1,3}\b` | Tested against fixture — missed IPs embedded mid-line. Added word boundary adjustment. |

---

## Entries

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

 Week 1 | Task 1 | "Explain how to extract timestamp, IP address, and username from the log file using regex; help debug parser test failures and deduplication logic." | Provided explained regex extraction, parser flow, match objects, CSV writing, and likely causes of unit test failures. Suggested corrections to username extraction for different log formats and deduplication approach. | I implemented and tested the parser manually in my own code. I verified fixes using the provided field tests, corrected syntax and parsing errors, adjusted regex to handle different username formats, and confirmed the final script produced valid CSV output. |

 | Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

 Week 1 | Task 1 | "Help debug why my parser only outputs one row when grep shows multiple matches; explain deduplication logic and how to fix it." | Explained that the issue was not with regex matching but with the deduplication logic being too broad. Identified that using only IP_Address and User_Account caused repeated failed attempts to be treated as duplicates. Suggested including Timestamp in the deduplication key and using grep to validate parser output against the actual log. | I verified the issue by comparing grep results with my CSV output and confirmed there were 3 matching lines before asking AI to explain to me why was my parser only identifying one line. I updated the deduplication key to include Timestamp, retested the parser, and confirmed all events were now correctly written to the CSV. I also validated the fix by checking the suspects.csv file again and running grep manually again. |

 | Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 1 | Task 1 | "Help me create and test a malformed/truncated auth log fixture and fix timestamp extraction for ISO and syslog formats." | Suggested creating a custom adversarial log file containing ISO 8601 timestamps, syslog timestamps, malformed and truncated lines. Identified that the parser assumed syslog timestamp format and recommended using regex patterns to support both formats while safely skipping malformed entries. | I created a local variant log file myself and tested the parser against it. I identified that the timestamp extraction was incorrect for ISO formatted lines due to using split-based logic. I updated the parser to use regex-based timestamp extraction for both syslog and ISO formats, retested the output, and confirmed the CSV was correctly structured and malformed lines were ignored without breaking the script. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 2 | Task 2 | "Explain how to implement a threaded TCP port scanner in Python using sockets, including banner grabbing and handling port ranges." | Suggested using socket.connect_ex() for safe TCP connection attempts, ThreadPoolExecutor for concurrency, and recv() to capture service banners. Also explained how to parse port ranges (1-1024) and lists (21,22,80) and highlighted the need for timeout handling to avoid the scanner hanging on unresponsive ports. | I implemented the scanner myself using the suggested approach and tested it against a live target. I verified that open ports were correctly identified by testing manually inside the live machine, and that banner data was captured where available. I also ensured port parsing handled both ranges and lists correctly by testing both scanning methods and added validation to prevent invalid input. During testing, I confirmed that some services do not return banners, which is expected behaviour and that some services the scanner does not list as they are open and listening but filtered by a firewall. I adjusted error handling and timeout settings to ensure the scanner remained stable and did not hang. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 2 | Task 2 | "Explain how to structure an exploit script using functions, validate service banners, and automate FTP command execution and file retrieval." | Suggested splitting the exploit into modular functions such as banner verification, FTP command handling, exploitation logic, and file retrieval. Also recommended validating the service version before exploitation and using HTTP to retrieve the copied file from a web-accessible directory. Provided guidance on structuring the workflow and improving reliability of the exploit. | I used this guidance to refactor my initial exploit into a structured script with separate functions for each stage. I implemented banner verification to confirm the target service (ProFTPD 1.3.5) before exploitation, created a reusable function to send FTP commands, and automated the retrieval of the file using HTTP. I tested the exploit manually using netcat and curl to confirm correctness, then validated that the automated script produced the same results. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 2 | Task 2 | "Why does disabling mod_copy in the configuration file not stop the vulnerability?" | Explained that some modules may be statically compiled into the service binary, meaning configuration changes (such as commenting out LoadModule) do not disable the functionality. | I attempted to disable the module through configuration changes, however the vulnerability remained exploitable. This confirmed that the module was compiled into the ProFTPD binary and not dynamically loaded. Based on this, I changed my remediation approach to a network-level solution instead of relying on configuration changes, I had to disable port 21 fully. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 1 | Task 1 | "Explain how to extend a log parser to support additional authentication log formats such as PAM-style entries, and how to safely modify regex without breaking existing functionality." | Suggested identifying differences in log structure (e.g. rhost= and user= instead of from and for), adding new regex patterns for detection and extraction, and implementing conditional logic to handle multiple formats. Also advised validating changes against existing pytest tests to ensure no regression. | I used this guidance to extend my parser to support PAM-style logs by adding detection for authentication failure and extracting IP and username using rhost= and user= patterns. I modified the processing logic to handle both original and new formats without affecting existing behaviour. After implementation, I ran the provided pytest tests to confirm nothing was broken, and then validated the parser manually using external datasets. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
| Week 3 | Task 3 (Access Validator) | "What improvements can I make to brute.py to make it more robust and aligned with the brief?" | Suggested improvements including input validation, better error handling, separating service errors from authentication failures, adding a service availability check, and improving control flow (e.g. handling interruptions, logging reliability, optional verbosity). | Reviewed suggestions and implemented changes step by step. Added port validation, improved logging with error handling, introduced a service pre-check, and used a custom exception to distinguish service failures from invalid credentials. Also added attempt counting and optional verbose mode. Verified all changes by running pytest to ensure the output contract was not broken and tested behaviour manually. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 3 | Task 2 (Network Cartographer Hardening) | "How can I harden scan.py with better validation and error handling?" | Suggested adding validation for timeout and threads, improving file write handling, using as_completed for safer threading, and handling interruptions cleanly. | Implemented validation for timeout and thread count, added error handling for output file writing, improved thread result handling, and added KeyboardInterrupt support. Tested
scanner against different inputs and verified JSON output remains correct. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
| Week 3 | Task 3 (Access Validator Debugging) | "Why is --verbose not showing all attempts?" | Explained that verbose output must be placed inside the loop before the authentication attempt and highlighted indentation issues affecting execution flow. | Identified incorrect indentation and placement of the verbose print statement. Fixed it by moving the print inside the loop before the attempt function and correcting indentation. Verified by rerunning the script and confirming all attempts were displayed before success. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
| Week 3 | Task 3 | Why does my FTP brute force stop early even though the service is still running? | Explained that temporary network issues (timeouts, connection resets, throttling) were being treated as fatal errors due to sys.exit() inside the brute loop. Suggested replacing exit with continue so the script continues testing passwords. | Tested tool against Metasploitable FTP service. Observed script stopped mid-wordlist before fix. After replacing sys.exit() with continue, tool continued execution despite connection issues. Verified correct brute-force behaviour. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 3 | Task 3 | Why does my attempt count not match the number of lines in my CSV log? | Identified that the CSV file was opened in append mode ("a"), causing previous run data to remain and inflate line count. Suggested resetting log file at start of each run using write mode ("w"). | Inspected attempt_log.csv and confirmed previous run entries were present. Implemented initialise_log() using "w" mode. After fix, CSV only contains current run and matches attempt count. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 3 | Task 3 | How should I structure my brute force loop to make it cleaner? | Suggested moving the brute-force loop into a separate function (run_credential_test) and passing the attempt function (FTP/SSH) as a parameter to improve modularity and reuse. | Refactored brute loop out of main() into run_credential_test(). Tested with FTP to confirm behaviour remained correct. Code is now cleaner and easier to manage. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |


| Week 3 | Task 3 | How should I manage logging so results are clean per run? | Suggested separating file initialisation from logging and using "w" once per run, then "a" for writing attempts. | Added initialise_log() and simplified log_attempt(). Verified CSV resets correctly each run and logs attempts accurately. |

| Week | Task | Prompt Used | AI Output Summary | My Verification / Changes Made |
|------|------|-------------|-------------------|-------------------------------|
|      |      |             |                   |                                |

| Week 3 | Task 3 | Why are multiple pytest tests failing even though my brute force logic looks correct? | Suggested checking the full pytest error output instead of focusing only on failing test names. Identified that the issue could be at argument parsing level rather than inside the brute-force loop. | Reviewed pytest output and found error related to missing `--target` argument. Compared script CLI with field test invocation and identified mismatch (positional vs optional argument). Updated parser to use positional `target`. Re-ran pytest and confirmed multiple failures were resolved as script now executes correctly. |
