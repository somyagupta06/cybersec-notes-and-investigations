# Windows Enterprise Incident Investigation

## Reconstructing a Phishing-to-DNS Data Exfiltration Attack using Elastic Security

> **Platform:** Elastic Security  
> **Investigation Type:** Windows Incident Response (DFIR)  
> **Methodology:** Evidence-Driven Investigation

---

# Executive Summary

A Windows workstation belonging to a Senior Finance Director was compromised after the user opened a phishing email containing a malicious attachment.

The investigation reconstructed the complete attack chain by correlating process execution, PowerShell activity, Active Directory reconnaissance, file operations, network share access, and DNS activity.

The attacker executed a malicious PowerShell payload, performed enterprise reconnaissance using PowerView, collected sensitive financial documents from a network share, compressed the data into a ZIP archive, and exfiltrated the archive through DNS.

---

# Investigation Scope

This investigation focused on analysing a compromised Windows endpoint using Elastic Security.

Artifacts analysed during the investigation included:

- Process Creation Events
- PowerShell Activity
- File Creation Events
- Parent-Child Process Relationships
- DNS Activity
- Command Line Execution
- Network Share Access
- Active Directory Enumeration

---

# Investigation Objectives

- Identify the initial execution vector.
- Determine how the attacker gained code execution.
- Reconstruct attacker activity.
- Investigate Active Directory enumeration.
- Identify targeted files.
- Determine how data was collected and staged.
- Identify the exfiltration technique.
- Reconstruct the complete attack timeline.

---

# Investigation Methodology

Rather than searching randomly for suspicious processes, the investigation followed an evidence-driven approach.

Victim Identification
        ↓
Timeline Reconstruction
        ↓
Process Correlation
        ↓
PowerShell Analysis
        ↓
Discovery
        ↓
Collection
        ↓
Staging
        ↓
Compression
        ↓
DNS Exfiltration
        ↓
Attack Timeline Reconstruction

---

# Stage 1 — Victim Identification & Timeline Reconstruction

## Objective

Identify the compromised user and establish a reliable investigation timeline.

---

## Evidence

- Filtered events using the affected user (`michael.ascot`).
- Sorted events chronologically (Oldest → Newest).

---

## Analysis

Instead of searching directly for malware or PowerShell events, the investigation first reduced the scope to the compromised user. Sorting events chronologically transformed thousands of logs into a structured attack timeline, making behavioural correlation significantly easier.

---

## Findings

- Successfully identified the compromised user.
- Established a chronological investigation timeline.
- Reduced investigative noise before analysing attacker activity.

📷 **Screenshot:** User Filter & Timeline Reconstruction

---

# Stage 2 — Initial Access & PowerShell Execution

## Objective

Identify how the attacker gained code execution.

---

## Evidence

- Phishing email opened through Outlook.
- ZIP attachment downloaded.
- Malicious `.lnk` file executed.
- `OUTLOOK.EXE` spawned `powershell.exe`.
- PowerShell downloaded a remote payload.

---

## Analysis

The phishing attachment triggered PowerShell execution through a malicious LNK file. PowerShell then downloaded and executed a remote payload in memory using `IEX` and `DownloadString()`, establishing a reverse shell with Powercat.

---

## Findings

- Initial access achieved through phishing.
- Malicious PowerShell execution confirmed.
- Reverse shell established.

📷 **Screenshots**

- Phishing Email
- PowerShell Command
- Powercat Execution

---





































<img width="986" height="426" alt="Screenshot 2026-05-26 at 10 05 30 AM" src="https://github.com/user-attachments/assets/3bab06b5-eed7-4e04-8309-de8384d1e715" /><img width="1152" height="448" alt="Screenshot 2026-05-26 at 10 00 27 AM" src="https://github.com/user-attachments/assets/67dad5de-aedb-4a36-b903-d751d55e63ff" /><img width="1470" height="956" alt="Screenshot 2026-05-26 at 9 56 07 AM" src="https://github.com/user-attachments/assets/8ad5d9ad-6ee5-4a8f-a2e1-6da6cc5328e2" />
timestamp - <img width="705" height="519" alt="Screenshot 2026-05-26 at 9 35 12 AM" src="https://github.com/user-attachments/assets/952a8086-a09c-499c-8ca8-8aad538cbfba" />
usser.name <img width="1470" height="956" alt="Screenshot 2026-05-26 at 9 39 10 AM" src="https://github.com/user-attachments/assets/d691d2b2-ac61-4a95-9721-3f977855755a" />
queries kam - <img width="495" height="277" alt="Screenshot 2026-05-26 at 9 39 47 AM" src="https://github.com/user-attachments/assets/afc63355-2d8c-4c32-ae58-97735dad0ca2" />
outlook - <img width="1470" height="956" alt="Screenshot 2026-05-26 at 9 45 55 AM" src="https://github.com/user-attachments/assets/2041c5f0-8aa7-4582-a40f-a7f4e5c06c78" />
process.name <img width="1166" height="578" alt="Screenshot 2026-05-26 at 9 49 04 AM" src="https://github.com/user-attachments/assets/fe05be4a-b20f-441d-bc89-4725e6e75279" />
table <img width="1470" height="956" alt="Screenshot 2026-05-26 at 9 51 48 AM" src="https://github.com/user-attachments/assets/860eeadb-2875-4ab6-ae26-e78bda2dc4a0" />
rundll <img width="1470" height="956" alt="Screenshot 2026-05-26 at 9 56 13 AM" src="https://github.com/user-attachments/assets/9de1fb27-d8c1-4dea-86bb-ab8816272ee8" />
invoice <img width="1138" height="457" alt="Screenshot 2026-05-26 at 10 00 42 AM" src="https://github.com/user-attachments/assets/487c704f-d913-4868-80fc-371d86494e9a" />
http <img width="1142" height="414" alt="Screenshot 2026-05-26 at 10 04 00 AM" src="https://github.com/user-attachments/assets/cae77efe-a196-4a10-943c-bb2631f27f12" />
payload <img width="881" height="392" alt="Screenshot 2026-05-26 at 10 05 44 AM" src="https://github.com/user-attachments/assets/fbd3d097-78c1-47d7-a53e-374b3194bac9" />

file created <img width="1154" height="604" alt="Screenshot 2026-05-26 at 10 12 01 AM" src="https://github.com/user-attachments/assets/2a833244-44ae-4e1e-ad37-a22ca8888cd3" />
attachment - <img width="608" height="460" alt="Screenshot 2026-05-26 at 10 11 33 AM" src="https://github.com/user-attachments/assets/971c0b2e-7884-4b58-9b00-205cc70fc8e4" />

 anoother file <img width="1470" height="956" alt="Screenshot 2026-05-26 at 10 24 21 AM" src="https://github.com/user-attachments/assets/b4ef3c21-8f7a-4bb8-8eba-4a8e3b633de8" />
conhost <img width="1470" height="956" alt="Screenshot 2026-05-26 at 10 22 45 AM" src="https://github.com/user-attachments/assets/efcd2162-f57b-4e91-8c13-28850a1a9171" />

process table <img width="1470" height="956" alt="Screenshot 2026-05-26 at 6 25 21 PM" src="https://github.com/user-attachments/assets/0268b718-dd62-4e73-a781-ccd92ae6d1b0" />

nslookup  <img width="1470" height="956" alt="Screenshot 2026-05-26 at 6 35 08 PM" src="https://github.com/user-attachments/assets/62974aaf-e89e-4c8c-8be4-0506243b5548" />

robocopy <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 03 59 PM" src="https://github.com/user-attachments/assets/8d940fe7-1f5c-4f16-b05f-2226b85a8225" />

robocopy file <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 06 13 PM" src="https://github.com/user-attachments/assets/ea695dff-5bd1-4ea8-bc5a-f04b3a8eba21" />
file 2 <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 06 37 PM" src="https://github.com/user-attachments/assets/ba35a980-31f3-4929-aea9-d6d10e8aa539" />


share folder <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 01 30 PM" src="https://github.com/user-attachments/assets/fbc34c7c-3a2d-48e2-bdc8-a4d9b4bb8367" />

noise filter <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 26 16 PM" src="https://github.com/user-attachments/assets/2ea0fb2a-3709-433a-ae0c-250503f7b279" />
write verbose <img width="1123" height="434" alt="Screenshot 2026-05-26 at 7 29 49 PM" src="https://github.com/user-attachments/assets/783fc7a8-0b7c-4e90-bc9e-9f634e092c8e" />
whoami <img width="1470" height="956" alt="Screenshot 2026-05-26 at 7 37 52 PM" src="https://github.com/user-attachments/assets/1b1a0a96-1038-4467-b5ca-d2465201b669" />














