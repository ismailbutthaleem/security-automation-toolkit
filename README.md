# Security Automation Toolkit

A Python-based security automation toolkit developed as part of my BSc Cyber Security coursework.

The project focused on building and testing security tools in an isolated lab environment using Kali Linux and Metasploitable. The tools were used across a workflow of log analysis, network reconnaissance, credential testing and web enumeration, followed by vulnerability investigation and remediation.

## Tools

### Evidence Collector — `log_parser.py`
Parses Linux authentication logs to identify failed authentication activity and outputs structured evidence to CSV. I extended and tested the parser against different log formats, including PAM authentication failures.

### Network Cartographer — `scan.py`
A threaded TCP port scanner that identifies reachable ports and attempts to collect service banners. Scan results were used to identify exposed service versions for further vulnerability research.

### Access Validator — `brute.py`
A credential testing tool supporting FTP and SSH, with wordlist processing, attempt logging, service checks and error handling.

### Web Enumerator — `web_enum.py`
Performs basic web reconnaissance by collecting HTTP headers, HTML comments and checking selected sensitive paths, with optional JSON output.

## Vulnerability Investigation

The toolkit was tested against Metasploitable in an isolated lab.

One investigation identified ProFTPD 1.3.5 through service banner information. I researched the exposed service, developed an exploit to validate the vulnerability and then tested a network-level mitigation by blocking FTP access with `iptables`.

The target was rescanned and manually tested with `netcat` to verify that port 21 was no longer reachable.

## Technologies

Python · Kali Linux · Metasploitable · Git · TCP/IP · FTP · SSH · HTTP · Regex · Pytest · CSV/JSON · iptables

## Documentation

A detailed development journal covering testing, troubleshooting, decisions and improvements made throughout the project is available in [`BUILD.md`](BUILD.md).

## Project Context

This project was completed as part of my BSc Cyber Security coursework and tested only within an isolated, authorised lab environment. Some coursework scaffolding was provided, while the implementation, extensions, testing and troubleshooting documented here represent the work I completed.
