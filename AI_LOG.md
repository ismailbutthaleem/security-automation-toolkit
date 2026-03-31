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

 Week 1 | Task 1 | "Help debug why my parser only outputs one row when grep shows multiple matches; explain deduplication logic and how to fix it." | Explained that the issue was not with regex matching but with the deduplication logic being too broad. Identified that using only IP_Address and User_Account caused repeated failed attempts to be treated as duplicates. Suggested including Timestamp in the deduplication key and using grep to validate parser output against the actual log. | I verified the issue by comparing grep results with my CSV output and confirmed there were 3 matching lines before asking AI to explain to me why was my parser only identifying one line. I updated the deduplication key to include Timestamp, retested the parser, and confirmed all events were now correctly written to the CSV. I also validated the fix by checking the suspects.csv file again and running grep manually again. |

| Week 1 | Task 1 | "Help me create and test a malformed/truncated auth log fixture and fix timestamp extraction for ISO and syslog formats." | Suggested creating a custom adversarial log file containing ISO 8601 timestamps, syslog timestamps, malformed and truncated lines. Identified that the parser assumed syslog timestamp format and recommended using regex patterns to support both formats while safely skipping malformed entries. | I created a local variant log file myself and tested the parser against it. I identified that the timestamp extraction was incorrect for ISO formatted lines due to using split-based logic. I updated the parser to use regex-based timestamp extraction for both syslog and ISO formats, retested the output, and confirmed the CSV was correctly structured and malformed lines were ignored without breaking the script. |

| Week 2 | Task 2 | "Explain how to implement a threaded TCP port scanner in Python using sockets, including banner grabbing and handling port ranges." | Suggested using socket.connect_ex() for safe TCP connection attempts, ThreadPoolExecutor for concurrency, and recv() to capture service banners. Also explained how to parse port ranges (1-1024) and lists (21,22,80) and highlighted the need for timeout handling to avoid the scanner hanging on unresponsive ports. | I implemented the scanner myself using the suggested approach and tested it against a live target. I verified that open ports were correctly identified by testing manually inside the live machine, and that banner data was captured where available. I also ensured port parsing handled both ranges and lists correctly by testing both scanning methods and added validation to prevent invalid input. During testing, I confirmed that some services do not return banners, which is expected behaviour and that some services the scanner does not list as they are open and listening but filtered by a firewall. I adjusted error handling and timeout settings to ensure the scanner remained stable and did not hang. |

