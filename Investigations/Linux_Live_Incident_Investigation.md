# Linux Live Incident Investigation

## Scenario

A Linux server exposed to the internet was suspected to be compromised by a threat actor. Threat intelligence suggested that the attacker had established persistence using a backdoor account.

The objective of this investigation was to identify attacker activity, reconstruct the attack chain, and determine how persistence was established on the compromised host.

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

---

# Attack Timeline

| Stage | Evidence |
|--------|----------|
| Initial Access | SSH authentication attempts |
| Credential Attack | Multiple failed login attempts |
| Successful Authentication | Login to `mircoservice` |
| User Activity | Suspicious processes executed from hidden directory |
| Malware Discovery | `strokes.c` discovered |
| Persistence | `strokes.service` configured |
| Additional Persistence | `printer_app` scheduled for execution |

---

# Indicators of Compromise (IOCs)

## Users

```
mircoservice
badactor
```

## Files

```
/home/mircoservice/.tmp/strokes.c
/home/mircoservice/.tmp/.strokes
printer_app
```

## Services

```
strokes.service
```

## Network

```
SSH authentication activity
Python process on Port 80
```

---

# MITRE ATT&CK Mapping

| Tactic | Technique |
|---------|-----------|
| Initial Access | Valid Accounts |
| Credential Access | Brute Force |
| Persistence | Create Account |
| Persistence | Systemd Service |
| Persistence | Scheduled Task |
| Execution | Command and Script Execution |
| Discovery | Process Discovery |
| Discovery | System Information Discovery |

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
