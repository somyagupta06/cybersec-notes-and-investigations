# 🔍 Widget LLC Endpoint Investigation (Splunk | Deep-Dive SOC Analysis)

---

## 📌 Context

Widget LLC, a newly onboarded client under TryNotHackMe (MSSP), reported concerns regarding a **Finance Department endpoint (Finance01)**.

A critical security gap was identified:

* Endpoint protection (Defender/EDR) was **disabled in December 2021**
* No formal investigation was conducted during that period
* Complete endpoint telemetry was available via Splunk

At the beginning, there was **zero clarity** about:

* Where the attack started
* Whether the system was actually compromised
* What actions were performed
* Whether any sensitive data was accessed

---

## 🎯 Objective

The investigation aimed to:

* Identify if malicious activity occurred
* Determine the **initial infection vector**
* Track **process execution and malware behavior**
* Detect **credential theft or data exfiltration**
* Build a **complete attack chain purely from logs**

---

## 🧠 Initial Mindset & Challenge

When I opened Splunk:

* There were **too many logs**
* Too many fields
* No clear entry point

At that moment:

```text
I knew WHERE to look (Finance endpoint)
But I did NOT know WHAT to look for
```

This caused:

* Random exploration
* Confusion
* Lack of direction

---

# 🔎 Evidence-Based Investigation

---

# 🟥 Stage 1: Initial Exploration (Confusion + First Direction)

## 🔍 What I Did

I started with:

```spl
index=*
```

Then applied:

* Time filter → December 2021
* Tried identifying:

  * account name
  * username
  * computer name
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 14 54 AM" src="https://github.com/user-attachments/assets/df5e61c9-3890-4c6e-95ed-290cab492a07" />
---

## ⚠️ Problem Faced

* Multiple accounts appeared
* Could not identify correct entity initially
* Confusion due to noisy data
<img width="1104" height="692" alt="Screenshot 2026-03-31 at 9 18 41 AM" src="https://github.com/user-attachments/assets/39c89d5e-fa07-4acc-ac7a-538386462691" />
---

## 🔥 Breakthrough

I identified:

```text
User: Finance01
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 18 12 AM" src="https://github.com/user-attachments/assets/dfe4c6b4-6abf-47ca-92f0-9108ee3968c6" />
Then shifted focus to:

```spl
index=* user=Finance01
```

---

## 🧠 What Was Happening (Actual)

At this stage:

* I correctly scoped the investigation
* But I lacked a **structured analysis approach**

---

## 🔍 What I Explored (Randomly)

I started checking fields:

* destination IP
* destination port
* other visible metadata
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 19 38 AM" src="https://github.com/user-attachments/assets/9dc4b4b2-f254-4e3f-89d0-ee8db338e383" />
---

## 🔍 Observation 1: `127.0.0.1`
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 23 25 AM" src="https://github.com/user-attachments/assets/95a8a835-ae14-44cf-9498-efd6e19e69f7" />
* Did not understand initially
* Searched externally
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 23 49 AM" src="https://github.com/user-attachments/assets/8b607bcc-193c-4e95-b8a3-ef26bb07402c" />
### Learned:

* It is localhost
* Internal communication

➡️ Not directly useful for attacker identification

---

## 🔍 Observation 2: Port `8888`
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 27 29 AM" src="https://github.com/user-attachments/assets/8cc20475-46a6-4b63-a873-50330e6a2edc" />
* Heavy activity observed
* Not a standard port
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 28 34 AM" src="https://github.com/user-attachments/assets/00ea4a83-d564-4728-a10e-4eda8a70b20f" />
➡️ Marked as suspicious

---

## 🔍 Observation 3: Port `80`

* Standard HTTP
  ➡️ Ignored for now

---

## ⚠️ Mistake

At this stage:

```text
I was analyzing NETWORK FIRST instead of PROCESS EXECUTION
```

➡️ This delayed root cause discovery

---

## 🧠 Learning

```text
Attack investigation should start from PROCESS, not network
```

---

# 🟥 Stage 2: Suspicious File Activity (Pattern Recognition)

## 🔍 What I Did

I focused on port 8888 related logs and observed:

* Multiple `.exe` files
* Same directory
* Different random names
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 35 46 AM" src="https://github.com/user-attachments/assets/9bd97607-5d02-4fc8-a1e5-4e0905419b40" />
---

## 🔥 Key Observation

```text
Same path + multiple EXEs + random names
```

---

## 🧠 Interpretation (Without Guessing)

* Repeated file creation
* Random naming pattern

➡️ Indicates **automated/malicious behavior**
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 37 01 AM" src="https://github.com/user-attachments/assets/4d54055d-efd8-4d16-8c0e-79c3812d4b98" />

---

## 🔍 Directory Analysis

Files located in:

* AppData
* Temp
* Adobe directories

---

## 💣 Important Insight

```text
Trusted directories being abused
```

➡️ Malware hiding in legitimate paths

---

## 🔍 Next Step


I shifted focus to:

```text
Temp folder activity
```
First I changed the Time line to see when the first exe is created 
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 43 50 AM" src="https://github.com/user-attachments/assets/c600b6a0-3ca3-4ac7-941b-61fddc7a3507" />

---

## 🔥 Breakthrough

I identified in the image of first event :

```text
ionicLarge.exe
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 44 21 AM" src="https://github.com/user-attachments/assets/b18b9a36-878c-45d2-a145-d900a886ec0f" />

---

## 🧠 Why This Was Important

* This process was:

  * creating files
  * linked to suspicious activity

➡️ Became **central investigation point**

I check it using Table, There I saw most of the exes are created by this process
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 9 48 46 AM" src="https://github.com/user-attachments/assets/cd45e256-cb2a-4d0a-923f-42a507d4c473" />

---

# 🟥 Stage 3: Root Cause Tracing (Reverse Analysis)

## 🔍 What I Did

I traced:

```text
ionicLarge.exe → Parent
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 09 42 AM" src="https://github.com/user-attachments/assets/481a9112-25d9-4cfa-ac91-ee18853d4915" />

---

## 🔍 Finding

```text
Parent: setup.exe
```

---

## 🧠 Interpretation

```text
Malware origin = setup.exe
```

---

## 🔍 Next Step

Traced further:

```text
setup.exe → Parent
```

---

## 🔍 Finding

```text
Parent: explorer.exe
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 13 08 AM" src="https://github.com/user-attachments/assets/ab84d3b2-1410-42e1-8ffb-a6078f850aec" />

---

## ⚠️ Confusion

Did not understand why explorer.exe appeared

---

## 🧠 Clarification

```text
explorer.exe = user interaction
```

➡️ Means:

💣 **User manually executed setup.exe**

---

## 🔍 Further Investigation

I analyzed explorer.exe activity and found:
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 26 11 AM" src="https://github.com/user-attachments/assets/ebe9eb37-1fee-4059-98fa-82b49955459c" />
```text
7z2107-x64.exe (7-Zip installer)
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 28 36 AM" src="https://github.com/user-attachments/assets/b60183bc-a816-4bd9-b919-c2274d6aa4f8" />
Then for better clarity I searched about it 
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 29 05 AM" src="https://github.com/user-attachments/assets/c414d665-31b2-4534-a6fc-22bcb564d833" />

---

## 🔍 Supporting Evidence

* DNS query → `www.7-zip.org`
* Installation behavior:

  * file creation
  * registry changes
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 40 17 AM" src="https://github.com/user-attachments/assets/ea86c9c4-5ad5-4faa-8061-6d56c1124adf" />

---

## 💣 Root Cause

```text
User downloaded 7-Zip
↓
Executed installer
↓
Malicious setup.exe dropped
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 42 16 AM" src="https://github.com/user-attachments/assets/9df2f329-6950-44f3-ab4e-0e140a44b514" />

➡️ **Initial Access = User Execution**

---

## ⚠️ Important Confusion

I initially questioned:

```text
Is 7-Zip malicious?
```

---

## 🧠 Resolution

```text
Software = Legit
Behavior = Malicious
```

---

# 🟥 Stage 4: Execution Phase (DLL + Payload Deployment)

## 🔍 What I Observed

Inside setup.exe execution:

* DLL loading events
* New executable creation

---

## ⚠️ Confusion

* DLL sideloading concept unclear
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 10 53 03 AM" src="https://github.com/user-attachments/assets/2e831422-419e-4380-8c47-c89103a4a03c" />

---

## 🧠 Behavior-Based Interpretation

Without relying on theory:

```text
setup.exe → loads DLL → creates new EXE
```

---

## 🔥 Key Finding

```text
setup.exe → ionicLarge.exe
```
<img width="1470" height="956" alt="Screenshot 2026-03-31 at 11 08 17 AM" src="https://github.com/user-attachments/assets/ec4ac53a-da84-4537-b94a-f449db2eb063" />

---

## 🧠 Conclusion

```text
setup.exe = dropper
ionicLarge.exe = main malware
```

---

## 💣 Important Transition

```text
Infection → Active Malware Execution
```

---

# 🟥 Stage 5: Malware Activity (Maximum Confusion Stage)

## 🔍 What I Did

Focused on:

```text
ionicLarge.exe
```

---

## ⚠️ Major Challenge

* Too many logs
* Too many events
* Could not correlate events
* Did not know next step

---

## 🧠 Root Problem

```text
I was seeing events, not behavior patterns
```

---

## 🔍 Observations (Step-by-Step)

---

## 🔹 1. File Creation

* Multiple EXEs
* `.txt` files

➡️ Interpretation:

```text
Data collection + staging
```

---

## 🔹 2. Process: `11111.exe`

* Created `.txt` files
* Contained password-related data

➡️ Conclusion:

```text
Credential Dumping Tool
```

---

## 🔹 3. Process: `install.exe`

Observed:

* cmd.exe execution
* powershell.exe execution
* taskkill commands

---

## 🧠 Breakdown

### cmd.exe

```text
taskkill → processes terminated
```

➡️ Security tools disabled

---

### PowerShell

```text
Defender modifications
```

➡️ Protection disabled

---

## 💣 Conclusion

```text
install.exe = defense evasion + system control
```

---

## 🔹 4. Process: `easycalc.exe`

## ⚠️ Confusion

* Unknown purpose
* Could not understand

---

## 🧠 Resolution

Based on behavior:

* spawned in malicious chain
* not standard execution

➡️ Conclusion:

```text
Disguised malware module
```

---

## 🔹 5. Network Activity

* Outbound connections
* Port 8888 usage

---

## 🧠 Interpretation

```text
Data leaving system
```

➡️ Possible exfiltration

---

## 🔥 Critical Realization

Instead of guessing:

```text
I should have asked:
“What did ionicLarge.exe DO?”
```

---

## 🧠 Behavior Summary

```text
ionicLarge.exe:
- creates files
- spawns processes
- executes commands
- disables security
- communicates externally
```

---

## 💣 Final Conclusion

```text
Malware performing:
- credential theft
- system compromise
- data exfiltration
```

---

# 💀 Full Attack Chain

```text
User downloads 7-Zip
↓
Executes installer (explorer.exe)
↓
setup.exe dropped
↓
DLL sideloading
↓
ionicLarge.exe executed
↓
install.exe disables security
↓
cmd + PowerShell used
↓
11111.exe dumps credentials
↓
TXT files store sensitive data
↓
Network communication (port 8888)
↓
Data exfiltration
```

---

# ⚠️ Challenges & Mistakes

* No initial direction
* Overwhelmed by logs
* Focused on network instead of process
* Random field exploration
* Could not correlate events initially
* Depended on hints/questions
* Confusion in:

  * DLL sideloading
  * command execution
  * tool behavior

---

# 🧠 Key Learnings

```text
Start with process, not network
Trace full lifecycle of suspicious process
Ignore names, focus on behavior
Ask: “What did this process DO?”
Avoid over-filtering early
Investigation is non-linear
Clarity comes from correlation
```

---

# 🚀 Final Insight

```text
Logs show events
Behavior reveals intent
Correlation builds the attack story
```

---

# 💯 Personal Growth Insight

At the beginning:

```text
I was lost in logs
```

At the end:

```text
I was building an attack narrative
```

➡️ This shift defines a real SOC Analyst 🔥

---



































