# The Benji Protocol — Mock Practice Report

**Student Name:** Ismail Butt
**Student ID:** 2433887
**Date:** 21-04-2026
**Target:** Metasploitable (172.16.19.101)

---

## 1. Diagnose

### Reconnaissance Summary
<!-- What did scan.py and web_enum.py reveal? Paste key JSON output here. -->
The scan.py tool identified multiple open ports on the target 172.16.19.101. The key results were:

Port 21 (FTP) — returned a service banner:

220 ProFTPD 1.3.5 Server (ProFTPD Default Installation)
Port 80 (HTTP) — open but did not return a banner through raw TCP connection
Port 3306 (MySQL) — returned an access restriction message
Port 6697 (IRC) — returned a notice banner

From this, ports 21 and 80 were identified as the most relevant attack surfaces.

Port 21 clearly exposed a service and version through its banner. Port 80 did not return a banner, which is expected because HTTP services require a proper request before responding with meaningful data.

To further investigate port 80, the web_enum.py tool was used:

{
    "target": "http://172.16.19.101",
    "headers": {
        "Server": "Apache/2.4.7 (Ubuntu)",
        "X-Powered-By": "Not present"
    },
    "comments": [],
    "sensitive_paths": {
        "/drupal": 301,
        "/drupal/CHANGELOG.txt": 200
    }
}

The output shows the server is running Apache/2.4.7 on Ubuntu.

The /drupal path returned a 301 redirect, confirming the application exists but is redirected internally. The path /drupal/CHANGELOG.txt returned a 200 response, meaning the file is publicly accessible.

This file is important because it can contain version information about the web application.

To inspect the file safely without using a browser, the following command was used:

curl -s http://172.16.19.101/drupal/CHANGELOG.txt | head -n 10

This command retrieves the file and prints only the first 10 lines, allowing quick identification of the most recent version without loading the entire file.

The output was:

Drupal 7.5, 2011-07-27

- Fixed security issue (Access bypass), see SA-CORE-2011-003.

From this, it can be confirmed that the application is running Drupal 7.5, released in 2011.

This version is significantly outdated, and the fact that the CHANGELOG.txt file is publicly accessible means version information is being exposed to any user. This is a misconfiguration that can assist an attacker in identifying potential weaknesses.
### Identified Vulnerability
<!-- Service name, version, CVE reference if applicable. -->
<!-- What does this vulnerability allow an attacker to do? -->

Two possible attack paths were identified during reconnaissance:

Port 21 — ProFTPD 1.3.5
Port 80 — Drupal application with exposed changelog

For this mission, the focus is on port 80, as it provides more direct application-level information.

The main issue identified is that:

A sensitive file (CHANGELOG.txt) is publicly accessible
This file reveals the exact Drupal version
The version identified (Drupal 7.5) is very outdated

Although the exposed file itself is not the core vulnerability, it creates an information disclosure issue that makes further exploitation easier. An attacker can use this information to research known weaknesses for that specific version and build a targeted exploit. This confirms the vulnerability to be so far a misconfiguration although as mentioned before this drupal version is outdated tso it has a very high risk chance of having a software vulnerability within it.

VE Reference:
SA-CORE-2018-002 / CVE-2018-7600

This vulnerability allows an attacker to perform unauthorised remote code execution (RCE) on affected Drupal systems.

The issue exists because Drupal does not properly validate user-supplied input in HTTP requests. An attacker can craft a malicious HTTP request containing specially structured payloads (render arrays) that the server processes incorrectly.

These render array properties are intended for internal use within Drupal’s rendering system, not for direct user interaction. However, in vulnerable versions (Drupal 6–8), the application processes these values even when they are supplied through external requests.

This means the server treats user input not just as data, but as executable instructions, which leads to unintended behaviour.

As a result, an attacker can force the system to execute functions that should only be triggered internally by the application, effectively bypassing normal security controls and authentication checks.

Impact of the Vulnerability

Successful exploitation can result in full site compromise. An attacker may be able to:

Read sensitive files (e.g. configuration files, credentials)
Modify website content
Upload backdoors or web shells
Create administrative accounts
Use the compromised system to pivot further into the network
Render Array Properties Involved

The vulnerability allows attackers to inject render array properties that should not be accessible through user input:

#access_callback
Used by Drupal to determine whether a user has access to an element.
If abused, this could potentially be used to bypass access controls.

#pre_render
Executes before the rendering process.
Can manipulate data before it is displayed.

#lazy_builder
Executes at the final stages of rendering.
Used to dynamically generate content.

#post_render
Executes after rendering is complete.
It can call functions on the output, making it particularly dangerous if controlled by an attacker.
Exploitation Approach

For this scenario, the most effective method is to use the #post_render property.

This is because it allows an attacker to control which function is executed on the server. By crafting a malicious HTTP request that includes a #post_render parameter and supplying a command as input, the attacker can trigger execution of system-level functions.

Due to the lack of proper input validation, Drupal processes these injected properties as part of its normal rendering workflow. This results in the execution of attacker-controlled code on the server.



### Evidence
<!-- Commit reference or paste of the recon_results.json entry that identified the target service. -->
The following output from web_enum.py confirms that the Drupal changelog file is publicly accessible:

"sensitive_paths": {
    "/drupal": 301,
    "/drupal/CHANGELOG.txt": 200
}

The 200 response code indicates that the file is accessible without authentication.

To confirm the version of Drupal running on the target, the following command was used:

curl -s http://172.16.19.101/drupal/CHANGELOG.txt | head -n 10

This returned:

Drupal 7.5, 2011-07-27

This provides direct evidence that the target is running an outdated Drupal version, which supports the identification of a potential software vulnerability.
---

## 2. Exploit

### Approach
<!-- Describe the exploitation logic in plain English before showing code. -->
<!-- What does the exploit do mechanically? Why does it work? -->

### Execution
<!-- Command used: -->
```
python exploit.py --target x.x.x.x --port xx
```

### Flag
```
FLAG: <paste flag here>
```

---

## 3. Remediate

### Approach
<!-- What change closes this vulnerability? -->
<!-- Why does this change work — what is the root cause you are addressing? -->

### Execution
<!-- Command used or configuration change applied: -->
```
python fix.py --target x.x.x.x
```

### Verification
<!-- How did you confirm the vulnerability is closed and the service is still running? -->

---

## 4. Reflection

<!-- 150-200 words. -->
<!-- What was the most significant technical obstacle you encountered? -->
<!-- What would you do differently if you had more time? -->
<!-- How does this exercise connect to your understanding of the broader vulnerability management lifecycle? -->
