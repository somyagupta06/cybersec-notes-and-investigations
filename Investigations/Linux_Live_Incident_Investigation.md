# Linux Live Incident Investigation

> **Note**
>
> This investigation was performed using a structured Linux Incident Response laboratory.
>
> The investigation methodology, evidence correlation, timeline reconstruction, analysis, findings, and documentation presented in this repository are entirely my own.

---

# Executive Summary

A Linux server exposed to the internet was suspected to be compromised by a threat actor. Threat intelligence indicated that the attacker had established persistence using a backdoor account.

The objective of this investigation was to determine:

- How the compromise occurred.
- Which artifacts were left behind by the attacker.
- Whether persistence mechanisms had been established.
- How the attack progressed after initial access.

Rather than relying on individual indicators, the investigation correlated authentication events, user accounts, running processes, network activity, and persistence artifacts to reconstruct the attack timeline.

---

# Investigation Scope

This investigation focused on live host analysis of a compromised Linux server.

The following areas were examined:

- Operating system information
- Authentication logs
- Local user accounts
- Running processes
- Active network connections
- Systemd services
- Scheduled tasks
- Persistence mechanisms

---

# Investigation Objectives

- Identify the initial access vector.
- Analyze authentication activity.
- Investigate suspicious user accounts.
- Analyze running processes and active network connections.
- Identify persistence mechanisms.
- Reconstruct the attack timeline.

---

# Investigation Methodology

The investigation followed an evidence-driven approach instead of searching randomly.

```
System Profiling
        ↓
Authentication Analysis
        ↓
User Account Investigation
        ↓
Process Investigation
        ↓
Persistence Analysis
        ↓
Attack Timeline Reconstruction
```
---

# Environment Overview

| Component | Details |
|-----------|---------|
| Operating System | Ubuntu 20.04 LTS |
| Architecture | x86_64 |
| Environment | AWS Virtual Machine |
| Investigation Type | Linux Live Incident Response |

---

# Stage 1 — System Profiling

The investigation started by collecting basic host information to understand the environment before analyzing attacker activity.

## Commands Used

```bash
uname -a
hostnamectl
lscpu
free -h
df -h
```
## Analysis

The objective of this stage was to understand the environment before analyzing attacker activity.

The collected information showed:

- The host was running Ubuntu 20.04 LTS.
- The system was deployed as a virtual machine.
- Memory utilization was within normal limits.
- Disk usage did not indicate ransomware activity or resource exhaustion.
- No removable media was mounted during the investigation.

At this stage, no direct evidence of compromise was identified. The information collected served as environmental context for the remaining investigation.

## Findings

- Ubuntu 20.04 LTS
- AWS Virtual Machine
- x86_64 Architecture
- Memory utilization within normal range
- No removable media mounted
- No immediate indication of resource exhaustion

> 📷 **Screenshot:** `System Information` <img width="935" height="532" alt="Screenshot 2026-07-05 at 2 05 01 PM" src="https://github.com/user-attachments/assets/6dfc39af-5bcd-48af-9604-cec8308f3b17" />
<img width="1090" height="528" alt="Screenshot 2026-07-05 at 2 05 32 PM" src="https://github.com/user-attachments/assets/e96d0e15-9bbe-419a-b5cc-279a0fad25b7" />


---

# Stage 2 — Authentication Analysis

The next objective was to determine whether unauthorized authentication had occurred.

Initially, `last` and `who` did not provide useful login history. Authentication logs were then examined.

<img width="297" height="135" alt="Screenshot 2026-07-05 at 2 07 27 PM" src="https://github.com/user-attachments/assets/b627e66a-e49e-49df-8ecb-ea3666360c9d" />


Authentication logs appeared abnormal because auth.log was detected as binary data rather than plain text. Instead of stopping the investigation, printable strings were extracted from the log.

## Commands Used

```bash
file /var/log/auth.log
strings /var/log/auth.log
```
## Analysis

The authentication log was not stored as plain text and appeared as binary data during initial inspection. To continue the investigation, printable strings were extracted from the log.

Recovered authentication events showed:

- Multiple failed SSH authentication attempts.
- Enumeration of invalid usernames.
- Successful authentication using the `mircoservice` account.

The sequence of failed authentication attempts followed by a successful login is consistent with a credential attack.

Although the source IP became the primary investigation pivot, the available evidence does not conclusively determine whether it belongs to the attacker. Additional artifacts were required before attribution could be made.

## Findings

Authentication logs showed:

- Multiple failed SSH authentication attempts.
- Invalid username enumeration.
- Successful authentication for the `mircoservice` account.
- Repeated activity originating from the same source IP.

These events indicated a likely credential attack followed by successful authentication.

> 📷 **Screenshot:** `Authentication Log Analysis`
<img width="1096" height="537" alt="Screenshot 2026-07-05 at 2 08 23 PM" src="https://github.com/user-attachments/assets/4b1f22b3-c044-4cb9-97d2-a102c09f92ee" />

<img width="344" height="95" alt="Screenshot 2026-07-05 at 2 08 35 PM" src="https://github.com/user-attachments/assets/015a6987-61af-48f7-bd5b-099625d5d7f3" />

<img width="1061" height="532" alt="Screenshot 2026-07-05 at 2 08 54 PM" src="https://github.com/user-attachments/assets/79c55a8a-41c5-411e-98c0-6d858d278e1c" />

<img width="1253" height="379" alt="Screenshot 2026-07-05 at 2 09 15 PM" src="https://github.com/user-attachments/assets/6b68a80c-3833-4b1e-b217-92672e534080" />

---

# Stage 3 — User Account Investigation

After identifying the suspicious account during authentication analysis, local user information was examined.

## Commands Used

```bash
cat /etc/passwd
groups mircoservice
```
## Analysis

The investigation identified a local account named `mircoservice`.

The account was configured with:

- Interactive shell (`/bin/bash`)
- Dedicated home directory
- Standard user privileges

Authentication artifacts further indicated that:

- The account had been created on the system.
- A corresponding group had also been created.
- A previously existing account named `badactor` had been removed.

Although the available evidence does not identify who created these accounts, the account creation events, combined with the suspicious authentication activity observed earlier, justified using `mircoservice` as the primary investigation pivot.

At this stage, the account was considered suspicious but not yet conclusively attributed to the attacker.

## Findings

A local account named **mircoservice** was identified.

Additional authentication artifacts indicated:

- Creation of the `mircoservice` account.
- Creation of an associated group.
- Evidence of a previously deleted account named `badactor`.

The `mircoservice` account became the primary investigation pivot.

> 📷 **Screenshot:** `User Account Investigation`
<img width="733" height="524" alt="Screenshot 2026-07-05 at 2 09 45 PM" src="https://github.com/user-attachments/assets/fad63344-c7ae-453d-b3fc-ce12f3776e3b" />

<img width="297" height="61" alt="Screenshot 2026-07-05 at 2 10 09 PM" src="https://github.com/user-attachments/assets/55319e14-5ced-4d86-9f13-bd6fb943517f" />

<img width="1083" height="379" alt="Screenshot 2026-07-05 at 2 10 24 PM" src="https://github.com/user-attachments/assets/e7e3c476-ab30-4a2f-8f02-fa7f4d1963d9" />

---

# Stage 4 — Process & Network Investigation

The next objective was to determine what activity was being performed by the suspicious account.

## Commands Used

```bash
ss -antp
ps aux
```
<img width="1076" height="523" alt="Screenshot 2026-07-05 at 2 11 03 PM" src="https://github.com/user-attachments/assets/ce9ce8b2-ac3e-4c9b-bda2-870619e0a54d" />

## Analysis

The process list showed activity associated with the `mircoservice` account.

One process was executing from a hidden directory located inside the user's home directory.

Hidden directories are common on Linux systems; however, execution of custom binaries from an uncommon hidden location justified additional investigation.

The Python process listening on Port 80 was noted as an artifact of interest.

Based on the available evidence alone, its relationship to the compromise could not be conclusively established.

Additional process inspection, parent process analysis, executable verification, and network correlation would be required to determine whether it was legitimate or malicious.

The investigation therefore focused on examining the contents of the hidden directory.

## Findings

A process owned by **mircoservice** was executing from:

```text
/home/mircoservice/.tmp/
```
<img width="1096" height="258" alt="Screenshot 2026-07-05 at 2 11 20 PM" src="https://github.com/user-attachments/assets/1fe61d2a-d0b1-480f-ba40-9a217148a7ed" />

Further inspection of the directory revealed a source code file named:

```text
strokes.c
```
<img width="542" height="530" alt="Screenshot 2026-07-05 at 2 11 34 PM" src="https://github.com/user-attachments/assets/fef57740-ace6-44e2-8e01-93e5fa6a4524" />


Static analysis of the source code showed functionality consistent with a keylogging utility.

The combination of:

- Hidden directory
- Executable process
- Suspicious source code

indicated potentially malicious activity associated with the account.



---

# Stage 5 — Persistence Investigation

Since the scenario suggested attacker persistence, common persistence locations were examined.

## Systemd Services

A custom service named:

```text
strokes.service
```

was configured to execute:

```text
/home/mircoservice/.tmp/.strokes
```

during system startup.

This provided a persistent execution mechanism.

> 📷 **Screenshot:** `Systemd Service`

<img width="1020" height="415" alt="Screenshot 2026-07-05 at 2 13 27 PM" src="https://github.com/user-attachments/assets/27a354e4-f344-4e26-ab80-6190bb34ba85" />


---

## Cron Analysis

Cron jobs were reviewed to identify scheduled execution.

A startup task executing `printer_app` was identified.

Static analysis of the binary revealed references related to:

- systemd
- service creation
- Netcat
- persistence-related functionality

Although static strings alone cannot confirm runtime behavior, they significantly increased suspicion that the binary was designed to establish or maintain persistence.

> 📷 **Screenshot:** `Cron Persistence`
<img width="939" height="534" alt="Screenshot 2026-07-05 at 2 14 08 PM" src="https://github.com/user-attachments/assets/b40d0d5e-7664-4090-b656-50ca9364f754" />

<img width="506" height="538" alt="Screenshot 2026-07-05 at 2 14 20 PM" src="https://github.com/user-attachments/assets/dc3b0801-f0d7-4ae0-ba79-0f9c5b13b126" />

## Analysis

A custom systemd service named `strokes.service` was identified.

The service was configured to execute a binary located inside the previously identified hidden directory.

This established a direct relationship between:

- suspicious user account
- hidden directory
- executable
- persistence mechanism

The service was configured to start automatically during system boot, providing a persistent execution mechanism.

---

# Attack Timeline

| Phase | Evidence | Finding |
|--------|----------|---------|
| Initial Activity | Multiple SSH authentication attempts | Unauthorized authentication activity observed |
| Authentication | Successful login using `mircoservice` | Suspicious account became investigation pivot |
| User Investigation | Newly created local account identified | Account creation events recovered |
| Process Execution | Process running from `/home/mircoservice/.tmp/` | Activity associated with hidden directory |
| Malware Discovery | `strokes.c` identified | Source code contained keylogging functionality |
| Persistence | `strokes.service` | Binary configured to execute during system startup |
| Additional Persistence | `printer_app` | Startup execution identified through scheduled task |

---

# Indicators of Compromise (IOCs)

## Users

```text
mircoservice
badactor
```

---

## Files

```text
/home/mircoservice/.tmp/strokes.c

/home/mircoservice/.tmp/.strokes

printer_app
```

---

## Services

```text
strokes.service
```

---

## Directories

```text
/home/mircoservice/.tmp/
```

---

## Network

```text
SSH Authentication Activity

Python process listening on Port 80
```

---

# MITRE ATT&CK Mapping

| Tactic | Technique | Justification |
|----------|-----------|---------------|
| Credential Access | Brute Force (T1110) | Multiple failed SSH authentication attempts followed by successful authentication |
| Persistence | Create Account (T1136) | Local account creation artifacts recovered |
| Persistence | System Services (T1543) | Custom systemd service configured to execute automatically |
| Persistence | Scheduled Task / Cron (T1053) | Startup execution configured using scheduled task |
| Execution | Command and Scripting Interpreter (T1059) | Executable launched through Linux binaries |
| Discovery | Process Discovery (T1057) | Running processes examined during investigation |
| Discovery | System Information Discovery (T1082) | Host information collected during initial profiling |

> **Note**
>
> The initial access vector could not be conclusively determined using the available evidence.
>
> Although authentication artifacts showed successful login activity, the evidence does not prove how the attacker initially obtained valid credentials.

# Detection Opportunities

## Detect Multiple Failed SSH Logins

### Splunk

```spl
index=linux sourcetype=syslog "Failed password"
| stats count by src_ip
| where count > 10
```

---

### Elastic (KQL)

```kql
event.dataset:"system.auth" AND message:"Failed password"
```

---

## Detect New Local User Creation

### Splunk

```spl
index=linux ("useradd" OR "new user")
```

---

### Elastic

```kql
message:"new user"
```

---

## Detect New Systemd Services

### Splunk

```spl
index=linux "systemctl" "enable"
```

---

### Sigma (Example)

```yaml
title: Linux Systemd Service Creation

logsource:
  product: linux

detection:
  selection:
    process_name: systemctl

condition: selection
```

---

# Containment Recommendations

If this were a real production incident, the following containment actions would be recommended:

- Isolate the compromised host from the network.
- Disable the `mircoservice` account.
- Stop and disable `strokes.service`.
- Remove unauthorized scheduled tasks.
- Reset potentially compromised credentials.
- Acquire forensic images before removing malicious artifacts.
- Review additional hosts for similar persistence mechanisms.
- Investigate the originating source IP for related activity.

---

# Investigation Limitations

The following limitations were identified during the investigation:

- The initial access vector could not be conclusively determined.
- The Python process listening on Port 80 could not be fully attributed using the available evidence.
- Static string analysis suggested persistence-related functionality but did not confirm runtime behavior.
- Authentication logs appeared in a binary format, limiting direct log analysis.

These limitations were documented to avoid drawing conclusions beyond the available evidence.

---

# Lessons Learned

This investigation reinforced several important incident response principles:

- Follow evidence instead of assumptions.
- Use suspicious artifacts as investigation pivots.
- Correlate evidence from multiple system components before drawing conclusions.
- Document uncertainty whenever evidence is insufficient.
- Persistence mechanisms should always be investigated after successful authentication.
- Multiple independent artifacts provide stronger confidence than isolated indicators.

---



# Skills Demonstrated

- Linux Live Incident Response
- Linux Authentication Log Analysis
- User Account Investigation
- Process Analysis
- Network Connection Analysis
- Systemd Service Analysis
- Cron Job Analysis
- Static Malware Analysis
- IOC Identification
- Attack Timeline Reconstruction
- MITRE ATT&CK Mapping

---

# Key Findings

- Multiple SSH authentication attempts were identified.
- Successful authentication occurred using the `mircoservice` account.
- Suspicious activity was associated with a hidden directory inside the user's home directory.
- Source code consistent with a keylogging utility was discovered.
- Persistence was established using a custom systemd service.
- Additional startup execution was configured through scheduled tasks.
- Multiple independent artifacts correlated to the same user account, strengthening the overall findings.

---

# Conclusion

This investigation reconstructed the compromise of a Linux server by correlating authentication logs, user account artifacts, running processes, network activity, and persistence mechanisms.

Rather than relying on isolated indicators, multiple independent artifacts were correlated to build an evidence-based attack timeline and identify how persistent access was maintained on the compromised host.
