# AI Transparency Log — The Benji Protocol

**Student Name:** Ismail Butt Haleem
**Student ID:** 2433887

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
