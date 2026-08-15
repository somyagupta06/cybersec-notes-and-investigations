# Endpoint Detection and Response 

## 1. Why Endpoint Security is Important
Today, almost all work is done on **digital devices** like laptops, desktops, and mobiles.  
Because of this, **cyber attacks** are also increasing.

Earlier:
- Devices worked **inside office network**
- Network firewall was enough

Now (Remote Work):
- Devices work **from home, cafés, anywhere**
- They are **outside the company network**
- So, they are more **exposed to attacks**

That’s why we need **strong protection directly on the device itself**.

---

## 2. What is EDR?
**EDR (Endpoint Detection and Response)** is a security tool that:
- Is installed on endpoints (laptop, PC, server)
- **Continuously watches** what is happening on the device
- **Detects attacks**
- **Helps stop and fix** the attack from one central console

Simple meaning:
> EDR is like a smart security guard that never sleeps and watches every action on your device.

---

## 3. Main Features of EDR (3 Pillars)

### Pillar 1: Visibility (Seeing Everything)
EDR can **see very deep activity** on a device.

It records:
- Which programs are running
- Which program started which (parent–child)
- File changes
- Registry changes
- User actions
- Network connections

Why this matters:
- Analyst can see **full story of the attack**
- Past data is saved for **investigation later**

Example:
If a Word file starts PowerShell, EDR clearly shows:
Word → PowerShell → Download → Infection

---

### Pillar 2: Detection (Finding the Attack)
EDR detects threats using:
- Known signatures (like antivirus)
- **Behaviour analysis**
- Machine learning

It can detect:
- New malware
- Fileless malware (only in memory)
- Suspicious behavior
- Abnormal actions

Example:
- Normal Word file should not run PowerShell
- If it does → **EDR flags it**

---

### Pillar 3: Response (Stopping the Attack)
EDR allows security teams to **take action instantly**.

Possible actions:
- Kill a malicious process
- Quarantine a file
- Isolate the device from the network
- Connect remotely to the device
- Investigate live

Important:
> All actions are done from **one central dashboard**

---

## 4. Why EDR is Better Than Antivirus (AV)

### Simple Example (Airport Security)

**Antivirus (AV)**:
- Like passport checking at airport
- Blocks only **known criminals**
- New criminals can pass

**EDR**:
- Like security cameras + guards inside airport
- Watches **everyone’s behaviour**
- Stops suspicious activity even if person looks innocent

---

## 5. Antivirus vs EDR (Simple Comparison)

| Feature | Antivirus (AV) | EDR |
|------|---------------|-----|
| Detection | Signature-based | Behaviour + ML |
| Visibility | Limited | Very deep |
| Fileless attacks | Mostly missed | Detected |
| Investigation | Not possible | Full timeline |
| Response actions | Very limited | Powerful actions |

---

## 6. Real Attack Scenario (Easy Steps)

### Attack Steps and Responses

Step 1: User downloads malicious Word file  
- AV: Does nothing  
- EDR: Logs download  

Step 2: User opens Word file  
- AV: Does nothing  
- EDR: Monitors activity  

Step 3: Word runs PowerShell  
- AV: Misses it  
- EDR: Flags unusual behaviour  

Step 4: PowerShell downloads malware  
- AV: Misses obfuscated command  
- EDR: Detects suspicious script  

Step 5: Malware hides in svchost.exe  
- AV: Cannot see memory injection  
- EDR: Detects process injection  

Step 6: Attacker connects remotely  
- AV: No visibility  
- EDR: Detects abnormal network activity  

Final Result:
- AV: System looks clean  
- EDR: Alert + full attack chain + response options  

---

## 7. Important Points to Remember (Revision)
- EDR protects **devices, not just network**
- Works even **outside office**
- Records **everything**
- Helps **detect, investigate, and respond**
- Antivirus alone is **not enough**

---

## One-Line Summary
**EDR is advanced endpoint security that watches behaviour, detects smart attacks, and helps stop them fast.**

---

# How EDR Works 
## 1. Is EDR Magic?
EDR looks magical because:
- It **sees everything** on a device
- It **detects smart attacks**
- It **stops threats in a few clicks**

But actually, EDR works using **agents, telemetry, smart analysis, and response actions**.

---

## 2. EDR Architecture (Very Simple)

EDR has **two main parts**:

1. **EDR Agent (Sensor)** → Installed on device  
2. **EDR Console** → Central dashboard (brain)

Think like this:
> Agent = Eyes and ears  
> Console = Brain  

---

## 3. EDR Agent (Sensor)

### What is an Agent?
- Small software installed on laptop / PC / server
- Runs silently in background
- Monitors **everything happening on the device**

### What does it do?
- Watches processes, files, registry, network, commands
- Sends data to EDR console **in real time**
- Can do basic detection by itself
- Triggers alerts if something looks suspicious

Simple line:
> Agent sits on the endpoint and keeps reporting every activity.

---

## 4. EDR Console

### What is the Console?
- Central place where **all endpoint data comes**
- Used by SOC analysts
- Applies logic, rules, ML, threat intelligence

### What happens here?
- Data from agents is **correlated**
- Threat intelligence is matched
- Alerts are generated
- Severity is assigned

Severity levels:
- Critical
- High
- Medium
- Low
- Informational

Simple line:
> Console connects the dots and decides what is dangerous.

---

## 5. What Happens After Detection?

When an alert appears:
1. Analyst opens the alert
2. Checks severity
3. Sees full details:
   - Processes
   - Files
   - Network activity
   - Registry changes
4. Decides:
   - False Positive (safe)
   - True Positive (attack)
5. Takes action directly from EDR

---

## 6. EDR with Other Security Tools

EDR does not work alone.

Other tools:
- Firewall
- Email Security
- DLP
- IAM
- EDR
- etc.

All tools send logs to **SIEM**
- SIEM = central investigation platform
- Helps analysts see full attack picture

---

## 7. What is Telemetry?

### Telemetry = Collected Data
Telemetry is **raw activity data** collected by EDR agents.

Think:
> Telemetry is like a black box of an endpoint.

More telemetry = Better detection

---

## 8. Types of Telemetry Collected

### 1. Process Activity
- Process start / stop
- Parent–child relationship
- Suspicious process chains

Example:
Word → PowerShell → Malware

---

### 2. Network Connections
- Outbound connections
- C2 server connections
- Unusual ports
- Data exfiltration

---

### 3. Command Line Activity
- CMD commands
- PowerShell commands
- Obfuscated scripts

Very important because:
- AV usually misses this
- EDR catches it

---

### 4. File and Folder Changes
- File creation
- File deletion
- Ransomware activity
- Malware dropping files

---

### 5. Registry Modifications
- Auto-start entries
- Persistence keys
- Configuration changes

---

## 9. Why Telemetry is Powerful?
- Single action may look normal
- Full chain looks malicious
- EDR sees **complete story**
- Analysts can:
  - Rebuild timeline
  - Find root cause
  - Understand attacker method

---

## 10. Advanced Detection Techniques

### 1. Behavioral Detection
- Looks at **what a program does**
- Not just what it is

Example:
Word starting PowerShell → suspicious

---

### 2. Anomaly Detection
- Learns normal behavior
- Flags abnormal activity

Example:
A system suddenly modifying startup registry keys

Note:
- Can cause false positives
- Full context helps analyst decide

---

### 3. IOC Matching
- Matches hashes, IPs, domains
- Uses threat intelligence feeds

Example:
Downloaded file hash matches known malware

---

### 4. MITRE ATT&CK Mapping
- Maps attack to:
  - Tactic (goal)
  - Technique (method)

Example:
Scheduled task creation  
Tactic: Persistence  
Technique: Scheduled Task  

Helps analysts understand attack stage.

---

### 5. Machine Learning
- Trained on huge data
- Detects complex attack chains
- Very useful for:
  - Fileless attacks
  - Multi-stage attacks

---

## 11. Response Capabilities of EDR

### 1. Isolate Host
- Cuts endpoint from network
- Stops lateral movement
- Very effective containment

---

### 2. Terminate Process
- Kills malicious process
- Used when isolation is not possible
- Must be done carefully

---

### 3. Quarantine File
- Moves file to safe location
- Cannot execute
- Analyst can delete or restore

---

### 4. Remote Access (RTR)
- Analyst opens remote shell
- Runs commands
- Collects data
- Runs scripts

---

### 5. Artefact Collection
Used for forensics and reporting.

Collected items:
- Memory dump
- Event logs
- Registry hives
- Folder contents

No physical access needed.

---

## 12. Final Revision Summary
- Agent collects telemetry
- Console analyzes data
- Detection uses behavior, ML, IOC
- Analyst investigates alerts
- EDR provides powerful response actions

---

## One-Line Final Note
**EDR works by continuously collecting endpoint data, analyzing behavior smartly, and giving analysts full control to detect and stop advanced attacks.**

