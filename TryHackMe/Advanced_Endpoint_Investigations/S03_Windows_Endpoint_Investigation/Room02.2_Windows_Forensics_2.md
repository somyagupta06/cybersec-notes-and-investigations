# Windows File-System Forensics — SOC Notes

## 1. What is a File System?

A hard disk is basically a collection of **bits (0 and 1)**.

Without a file system, these bits would be difficult to understand and manage.

A file system organizes the data into:

* Files
* Folders
* Metadata
* Storage locations

Think of it like a **map for the disk**.

```text
Raw Disk
   ↓
Bits (0 and 1)
   ↓
File System
   ↓
Files + Folders + Metadata
```

### SOC Point of View

A DFIR/SOC analyst wants to answer questions like:

```text
Did this file exist?
When was it created?
Was it opened?
Was a program executed?
Was the file copied?
Was it deleted?
Was a USB connected?
```

File-system artifacts help answer these questions.

---

# 2. FAT File System

FAT = **File Allocation Table**

FAT is a simple file system that organizes data using:

* Clusters
* Directories
* File Allocation Table

## Cluster

A cluster is a basic storage unit.

A file can use one or many clusters.

```text
report.pdf

Cluster 10
   ↓
Cluster 11
   ↓
Cluster 15
   ↓
Cluster 20
```

The actual file data is stored in these clusters.

## Directory

A directory stores information about files, such as:

* File name
* File size
* Starting cluster
* Other file information

## File Allocation Table

FAT keeps track of cluster chains.

Example:

```text
report.pdf

Cluster 20 → 21 → 25 → 30 → END
```

This tells the system where the next part of the file is located.

---

# 3. FAT12, FAT16 and FAT32

The main difference is the number of bits used for cluster addressing.

| File System | Addressable Bits | Maximum Clusters |
| ----------- | ---------------: | ---------------: |
| FAT12       |               12 |            4,096 |
| FAT16       |               16 |           65,536 |
| FAT32       |        28 actual |      268,435,456 |

Important practical point:

FAT32 is commonly found on removable storage such as:

* USB drives
* SD cards
* Older digital devices

FAT32 has an important limitation:

```text
Maximum single file size ≈ 4 GB
```

---

# 4. exFAT

exFAT was designed to overcome many FAT32 limitations.

It is commonly used on modern removable storage.

Think:

```text
FAT32
   ↓
Smaller/older removable storage

exFAT
   ↓
Modern removable storage
   ↓
Large SD cards / flash storage
```

Important point:

**exFAT supports much larger files and volumes than FAT32.**

For investigations, do not assume every USB is FAT32.

A USB can use:

* FAT32
* exFAT
* NTFS

---

# 5. NTFS

NTFS = **New Technology File System**

NTFS is the main Windows file system you should know for Windows forensics.

Compared with FAT, NTFS provides:

* Journaling
* Access controls
* Volume Shadow Copies
* Alternate Data Streams
* Master File Table
* Better reliability and recovery features

For DFIR, NTFS is very important because it leaves many useful forensic artifacts.

---

# 6. NTFS Journaling

NTFS keeps information about file-system transactions.

Two important structures are:

```text
$LogFile
$UsnJrnl
```

They are NOT the same thing.

---

# 7. $LogFile

Think of `$LogFile` as an NTFS transaction record.

It helps NTFS maintain file-system consistency, especially after crashes or interrupted operations.

### Important SOC point

Do NOT think:

```text
$LogFile = Program Execution Evidence
```

That is incorrect.

Instead:

```text
$LogFile
   ↓
NTFS transactions / file-system changes
```

It is mainly useful for understanding file-system operations.

---

# 8. USN Journal

USN = **Update Sequence Number**

The USN Journal is like a history of changes made to files.

It can contain reasons such as:

* File created
* File modified
* File renamed
* File deleted

Example:

```text
Salary.xlsx
   ↓
Created
   ↓
Modified
   ↓
Renamed
   ↓
Deleted
```

### SOC Point of View

USN Journal helps answer:

> "What happened to this file?"

But remember:

```text
USN Journal ≠ Direct Execution Evidence
```

It tells us about file-system activity, not necessarily whether a program was executed.

---

# 9. MFT — Master File Table

MFT = **Master File Table**

Think of the MFT as the main database of an NTFS volume.

It contains records for files and directories.

A record can contain information such as:

* File name
* Parent directory
* Timestamps
* File attributes
* Security information
* Data location information

Example:

```text
MFT
├── File A
├── File B
├── File C
├── File D
└── ...
```

### SOC Point of View

MFT can help answer:

```text
Did this file exist?
Where was it located?
What metadata does it have?
What timestamps are associated with it?
```

---

# 10. How Windows Finds a File

Suppose the user wants:

```text
C:\Users\Alice\Documents\resume.pdf
```

Conceptually:

```text
File Path
   ↓
Directory information
   ↓
Find MFT record
   ↓
Read metadata
   ↓
Find data location
   ↓
Read file data
```

Important advanced point:

A small file can sometimes be stored directly inside its MFT record.

This is called:

```text
Resident Data
```

So do not always assume:

```text
MFT → Cluster → File
```

---

# 11. FAT vs MFT

| FAT                            | MFT                               |
| ------------------------------ | --------------------------------- |
| Used by FAT file systems       | Used by NTFS                      |
| Simple structure               | Structured database               |
| Tracks cluster allocation      | Stores detailed file records      |
| Less metadata                  | Much richer metadata              |
| Basic file-system organization | Very useful for Windows forensics |

Easy memory trick:

```text
FAT = Simple Map

MFT = Detailed File Database
```

---

# 12. Windows Prefetch

Prefetch is one of the most important execution artifacts.

Default location:

```text
C:\Windows\Prefetch
```

Files usually have:

```text
.pf
```

extension.

Example:

```text
EVIL.EXE-12345678.pf
```

---

# 13. What Does Prefetch Tell Us?

Prefetch can provide information such as:

* Application execution
* Last run information
* Run count
* Files used by the application
* Device information associated with the application

Example:

```text
EVIL.EXE

Run Count: 5
Last Run: 10:30 AM
```

This is strong evidence that:

```text
EVIL.EXE was executed.
```

### Easy Memory Trick

```text
Prefetch = "Did this program run?"
```

---

# 14. Prefetch Does NOT Prove Malicious Activity

Suppose we find:

```text
PowerShell.exe

Last Run: 2:15 PM
Run Count: 1
```

We can say:

```text
PowerShell.exe was executed.
```

But we cannot automatically say:

```text
The attacker executed a malicious PowerShell script.
```

Why?

Prefetch does not tell us exactly what command or script was executed.

For that, we may need additional evidence such as:

* PowerShell logs
* Script Block Logging
* Command history
* EDR telemetry
* Other correlated artifacts

### Important SOC Rule

```text
Execution Evidence
        ≠
Malicious Execution Proof
```

---

# 15. PECmd

Eric Zimmerman's **PECmd** can parse Prefetch files.

Single file:

```text
PECmd.exe -f "<path-to-prefetch-file>" --csv "<output-folder>"
```

Whole directory:

```text
PECmd.exe -d "<path-to-Prefetch-directory>" --csv "<output-folder>"
```

SOC use:

```text
Prefetch File
     ↓
PECmd
     ↓
CSV / JSON / HTML
     ↓
Investigation
```

---

# 16. Windows Timeline

Windows Timeline stores activity information in an SQLite database.

A common location is:

```text
C:\Users\<username>\AppData\Local\ConnectedDevicesPlatform\<random-folder>\ActivitiesCache.db
```

Timeline can contain information about:

* Applications used
* Files involved in activity
* Focus/usage time

Think:

```text
Timeline = "What activity happened around this time?"
```

---

# 17. WxTCmd

Eric Zimmerman's **WxTCmd** can parse the Windows Timeline database.

Example:

```text
WxTCmd.exe -f "<path-to-ActivitiesCache.db>" --csv "<output-folder>"
```

### SOC Point of View

Timeline is useful for:

* Building a user activity timeline
* Correlating application usage
* Supporting execution analysis
* Connecting files and applications

But avoid saying:

```text
Timeline always proves execution.
```

Better:

```text
Timeline provides supporting evidence of application/user activity.
```

---

# 18. Jump Lists

Jump Lists show recently used files for applications.

Example:

```text
Right-click Excel

Recently opened:
----------------
Salary.xlsx
Budget.xlsx
Report.xlsx
```

Common location:

```text
C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations
```

Jump Lists can help identify:

* Applications used
* Recently opened files
* Application/file relationships
* Activity times

### Easy Memory Trick

```text
Jump List = "What files were recently used with this application?"
```

---

# 19. JLECmd

Eric Zimmerman's **JLECmd** can parse Jump Lists.

Example:

```text
JLECmd.exe -f "<path-to-JumpList-file>" --csv "<output-folder>"
```

For a directory:

```text
JLECmd.exe -d "<JumpList-directory>" --csv "<output-folder>"
```

---

# 20. Shortcut / LNK Files

Windows creates shortcut files for files that are opened.

Common locations:

```text
C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Recent\

C:\Users\<username>\AppData\Roaming\Microsoft\Office\Recent\
```

LNK files can contain information such as:

* Target file
* Target path
* Creation time
* Modification time
* Access information
* Volume information
* Removable-drive information

---

# 21. Very Important: Opened vs Executed

This is an important SOC distinction.

For example:

```text
evil.exe
```

was:

```text
Executed
```

But:

```text
Salary.xlsx
```

was:

```text
Opened / Accessed
```

Do not normally say:

```text
Salary.xlsx was executed.
```

Better:

```text
Salary.xlsx was opened using Excel.
```

The Excel application itself may have been executed.

---

# 22. LECmd

Eric Zimmerman's **LECmd** can parse LNK files.

Example:

```text
LECmd.exe -f "<path-to-LNK-file>" --csv "<output-folder>"
```

For a directory:

```text
LECmd.exe -d "<LNK-directory>" --csv "<output-folder>"
```

---

# 23. IE / Edge WebCache

A useful location is:

```text
C:\Users\<username>\AppData\Local\Microsoft\Windows\WebCache\WebCacheV*.dat
```

Interesting point:

Browser history can sometimes contain evidence of local files that were accessed.

You may see paths beginning with:

```text
file:///
```

Example:

```text
file:///C:/Users/Alice/Documents/report.pdf
```

This can help answer:

> "Was this local file accessed?"

Autopsy can be used to analyze WebCache data.

---

# 24. USB Forensics — SetupAPI.dev.log

When a new device is connected, Windows records device setup information.

Location:

```text
C:\Windows\inf\setupapi.dev.log
```

For USB investigations, this can provide information such as:

* Device ID
* Vendor information
* Serial number
* Device setup/connection information

Example:

```text
Kingston USB

Serial Number:
K123456

Time:
10:00 AM
```

### SOC Point of View

This helps answer:

```text
Was a USB device connected?
Which device was it?
What is its serial number?
```

---

# 25. USB Correlation

Suppose SetupAPI shows:

```text
Kingston USB
Serial: K123456
```

And an LNK contains:

```text
Target:
E:\Finance\Salary.xlsx

Volume:
KINGSTON

Serial:
K123456
```

Now we can correlate the artifacts.

```text
SetupAPI
    ↓
Kingston USB
Serial K123456
    ↓
LNK
    ↓
Salary.xlsx
    ↓
KINGSTON
Serial K123456
```

This is much stronger than looking at only one artifact.

---

# 26. Example: Possible USB Data Theft

Imagine:

```text
10:00 AM
Kingston USB connected

        ↓

10:03 AM
Excel.exe executed

        ↓

10:05 AM
Salary.xlsx opened

        ↓

10:07 AM
Salary.xlsx copied

        ↓

10:10 AM
Salary.xlsx deleted
```

Possible artifacts:

```text
SetupAPI
    ↓
USB connection

Prefetch
    ↓
Excel execution

LNK
    ↓
Salary.xlsx opened
    ↓
USB volume information

Jump List
    ↓
Excel + Salary.xlsx relationship

USN Journal
    ↓
File activity

MFT
    ↓
File metadata

Timeline
    ↓
User/application activity
```

---

# 27. Do Not Overclaim

This is one of the most important SOC rules.

Suppose you find:

```text
USB connected
+
Salary.xlsx opened
+
Salary.xlsx copied
+
Salary.xlsx deleted
```

Do not immediately write:

```text
The employee definitely stole the file.
```

Instead write:

```text
The observed activity is consistent with a possible data-exfiltration attempt involving a USB device.
```

Why?

Because forensic analysis must separate:

```text
FACT
```

from:

```text
INFERENCE
```

---

# 28. Facts vs Inference

### FACT

```text
SetupAPI shows a Kingston USB device with serial K123456.
```

### FACT

```text
Prefetch shows Excel.exe execution.
```

### FACT

```text
LNK references Salary.xlsx.
```

### FACT

```text
USN Journal shows file-system activity involving Salary.xlsx.
```

### INFERENCE

```text
The user may have copied Salary.xlsx to the connected USB.
```

### Strong Conclusion

Only make a strong conclusion when multiple independent artifacts support the same story.

---

# 29. Artifact Cheat Sheet

| Artifact         | Main Question                                      |
| ---------------- | -------------------------------------------------- |
| MFT              | Did the file exist? What metadata does it have?    |
| Prefetch         | Was an application executed?                       |
| Timeline         | What application/user activity happened and when?  |
| Jump Lists       | What files were recently used with an application? |
| LNK              | What file was opened and where was it located?     |
| USN Journal      | What happened to the file?                         |
| $LogFile         | What NTFS transactions occurred?                   |
| SetupAPI.dev.log | Was a device installed/connected?                  |
| WebCache         | What browser/local-file activity is recorded?      |

---

# 30. Best Artifact Based on the Question

## Question: "Did the program execute?"

Think:

```text
Prefetch
+
Timeline
+
Other execution artifacts
```

## Question: "Did the file exist?"

Think:

```text
MFT
```

## Question: "What happened to the file?"

Think:

```text
USN Journal
```

## Question: "Was the file opened?"

Think:

```text
LNK
+
Jump Lists
+
WebCache
```

## Question: "Was a USB connected?"

Think:

```text
SetupAPI.dev.log
```

## Question: "What happened internally in NTFS?"

Think:

```text
$LogFile
```

---

# 31. The DFIR Mindset

Do not memorize artifacts as separate things.

Instead, think about the **question first**.

```text
Question
   ↓
Which artifact can answer it?
   ↓
What exactly does that artifact prove?
   ↓
What does it NOT prove?
   ↓
Can another artifact confirm it?
   ↓
Build the timeline
   ↓
Make a careful conclusion
```

The most important rule:

```text
One artifact = One clue

Multiple correlated artifacts = Stronger evidence

Evidence + Correlation + Careful reasoning = Forensic conclusion
```

# Quick Revision

```text
MFT
→ File metadata / existence

Prefetch
→ Program execution

Timeline
→ User/application activity

Jump Lists
→ Recently used files + applications

LNK
→ Opened file + path + volume information

USN Journal
→ File-system changes

$LogFile
→ NTFS transactions

SetupAPI.dev.log
→ Device/USB setup information

WebCache
→ Browser + local file activity
```

## One-line Memory Trick

```text
MFT       = What is/was this file?
Prefetch  = Did this program run?
Timeline  = What activity happened?
Jump List = What was recently used?
LNK       = What file was opened?
USN       = What happened to the file?
$LogFile  = What did NTFS transact?
SetupAPI  = What device was connected?
WebCache  = What local/browser activity happened?
```
