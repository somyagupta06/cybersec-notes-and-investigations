# 🔍 Conti Ransomware Investigation 

---

## 📌 Context

Employees were not able to access Outlook, and the Exchange admin also could not log in to the Exchange Admin Center.

When the server was checked, multiple `readme.txt` files were found across different directories.

From this, it was clear that ransomware activity had taken place.

However, at this point, I did not know:

* how the attacker entered the system
* what steps were performed before ransomware
* how different processes were connected

So the entire investigation was done step-by-step using only Splunk logs.

---

## 🎯 Objective

The goal of this investigation was to:

* Identify the initial access point
* Track execution of processes
* Understand process relationships
* Identify persistence activity
* Detect credential access
* Reconstruct the full attack chain

---

## 🧠 Investigation Approach

I did not start with any predefined query or assumption.

I followed a simple rule:

```text id="rule1"
Start from visible evidence → then move step-by-step using logs
```

So I started from the only confirmed indicator:

👉 `readme.txt`

---

## 🔎 Stage 1: Ransomware File Detection

I searched for:

```text id="q1"
readme.txt
```

---

### 🔍 What I found in logs

* Same file was created in multiple directories
* Around 18 file creation events
* All events had:

```text id="q2"
Image = cmd.exe
```

---

### 🧠 What I understood from logs

This was important:

* same file name
* same process
* multiple locations

➡️ this is not normal behavior

➡️ this indicates automated execution

➡️ consistent with ransomware file drop pattern

---

### ⚠️ My confusion

At this point, I was confused:

* cmd.exe is a normal Windows process
* so how is it related to ransomware?

---

### 🧠 What I did next

Instead of focusing on name, I focused on behavior:

➡️ process creating same file repeatedly

➡️ so I marked:

```text id="q3"
cmd.exe = suspicious process
```

---

## 🔎 Stage 2: Understanding cmd.exe Activity

Next, I explored cmd.exe in detail.

---

### 🔍 What I checked

* CommandLine
* process behavior

---

### 🔍 What I found

Commands executed:

* whoami
* ipconfig
* net user

---

### 🧠 Log-based interpretation

From logs only:

* whoami → checking current user
* ipconfig → checking system network
* net user → user-related operations

➡️ this shows:

👉 someone is actively executing commands manually or through script

---

### 🔍 Important observation

These commands appeared before ransomware execution

➡️ meaning attacker performed actions before encryption

---

## 🔎 Stage 3: Parent Process Analysis (Where I Got Stuck)

I checked:

```text id="q4"
ParentImage of cmd.exe
```

---

### 🔍 What I found

* powershell.exe
* unsecapp.exe

---

### ⚠️ Major confusion

This confused me a lot:

* how can one process have multiple parents?
* which one should I follow?

Initially I tried:

```text id="q5"
trace parent → then its parent → then next
```

➡️ but this approach did not work

---

### 🧠 Breakthrough

Then I changed my approach:

```text id="q6"
analyze each parent separately
```

➡️ this helped me move forward

---

## 🔎 Stage 4: EventCode 8 (CreateRemoteThread)

I was told to use EventCode 8, but initially I did not understand why.

Still, I searched:

```text id="q7"
EventCode = 8
```

---

### 🔍 What I found

Event showing:

* SourceImage: powershell.exe
* TargetImage: unsecapp.exe

---

### 🧠 What logs show

This event indicates:

➡️ one process is interacting with another process

➡️ this is recorded as CreateRemoteThread

---

### 🔍 More findings

I found another event:

* SourceImage: unsecapp.exe
* TargetImage: lsass.exe

---

### 🧠 Full chain from logs

```text id="q8"
powershell.exe → unsecapp.exe → lsass.exe
```

---

### 🧠 Interpretation (based on logs)

* processes are linked
* execution is moving across processes

➡️ attacker is shifting execution between processes

---

## 🔎 Stage 5: File Creation (Important Detail)

Now I went back to file creation events carefully.

---

### 🔍 What I observed

Although initial Image was cmd.exe, deeper analysis showed:

➡️ unsecapp.exe was also involved in activity

---

### 🧠 Important point

* cmd.exe was visible in execution
* but underlying activity linked to unsecapp

➡️ meaning attacker execution moved between processes

---

## 🔎 Stage 6: Using Timestamp for Correlation (VERY IMPORTANT)

At this point, I started using timestamps.

---

### 🔍 What I did

* matched timestamps between events
* aligned:

  * process execution
  * EventCode 8
  * file creation

---

### 🧠 What I understood

Using timestamps helped me:

➡️ see sequence of events

➡️ understand order:

```text id="q9"
PowerShell → unsecapp → lsass → cmd.exe → readme.txt
```

---

### ⚠️ Learning

Without timestamps, events looked disconnected

➡️ timestamps made the attack flow clear

---

## 🔎 Stage 7: Tracing Back to Entry Point

Now I focused on:

```text id="q10"
powershell.exe
```

---

### 🔍 What I checked

ParentImage of PowerShell

---

### 🔍 What I found

```text id="q11"
ParentImage = w3wp.exe
```

---

### ⚠️ My confusion

* what is w3wp?
* is it attacker process?

---

### 🧠 What I did

I did not assume anything

I only noted from logs:

```text id="q12"
w3wp.exe → powershell.exe
```

---

## 🔎 Stage 8: IIS and Web Activity

Since w3wp is involved, I checked web-related logs.

---

### 🔍 What I filtered

```text id="q13"
HTTP POST requests
```

---

### 🧠 Reason

From logs:

* POST requests contain data sent to server
* repeated POST = interaction

---

### 🔍 What I found

```text id="q14"
/owa/auth/i3gfPctK1c2x.aspx
```

---

### 🔍 Observations

* repeated POST requests
* same endpoint
* timestamps match PowerShell execution

---

### 🧠 Log-based conclusion

* this file is being accessed repeatedly
* execution follows this request

➡️ this endpoint is part of execution

---

## 🔎 Stage 9: Full Correlation

Now everything started connecting.

---

### 🔍 From logs

```text id="q15"
POST request
→ w3wp.exe
→ powershell.exe
→ unsecapp.exe
→ lsass.exe
→ cmd.exe
→ readme.txt
```

---

### 🧠 What I understood

* request triggers web process
* web process triggers PowerShell
* execution moves across processes
* finally file creation happens

---

## 🔎 Stage 10: Final Impact

From file creation logs:

* multiple readme.txt
* repeated execution

---

### 🧠 Final conclusion

➡️ ransomware executed

➡️ system impacted

---

## 💀 Final Attack Chain (Log-Based)

```text id="final"
POST request
→ w3wp.exe
→ powershell.exe
→ CreateRemoteThread (EventCode 8)
→ unsecapp.exe
→ lsass.exe
→ cmd.exe
→ readme.txt creation
```

---

## ⚠️ My Mistakes (Important)

* tried linear parent tracing
* got confused with multiple parents
* ignored timestamps initially
* did not understand EventCode 8 at first
* did not correlate web activity early

---

## 🧠 Key Learnings

* always follow logs, not assumptions
* timestamps are critical
* EventCode 8 shows process interaction
* multiple parents require branching analysis
* web activity and system execution must be correlated

---

## 🚀 Conclusion

This investigation started with confusion, but step-by-step log analysis helped me:

* identify execution flow
* correlate multiple processes
* track attacker activity
* and confirm ransomware behavior

Everything was derived only from logs without relying on assumptions.
