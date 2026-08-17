# Windows Incident Surface — System Profiling & Live Investigation

## 1. Why do we profile the system first?

Before investigating a Windows machine, we should first understand:

- Which computer are we investigating?
- Which OS is running?
- What is its IP address?
- What time and timezone is the machine using?
- Which users exist?
- Who is currently logged in?
- Which network connections are active?
- Which services are running?
- Which programs start automatically?
- Which processes are running?

Think of it like this:

You enter a crime scene.

You do NOT immediately start opening random drawers.

First you understand:

> "Where am I? What is normal here? Who is present? What is running?"

The same idea applies to a Windows investigation.

---

# 2. System and Network Information

Command:

Get-CimInstance win32_networkadapterconfiguration -Filter IPEnabled=TRUE | ft DNSHostname, IPAddress, MACAddress

This gives us:

- DNS Hostname
- IP Address
- MAC Address

Example:

DNSHostname     : WIN-PC-01
IPAddress       : 192.168.1.20
MACAddress      : 02:49:XX:XX:XX:XX

## Why does SOC care?

Suppose the incident report says:

> "Investigate WIN-PC-01."

First we should confirm that the machine we are actually investigating is WIN-PC-01.

We also record its IP address.

Later we may see:

192.168.1.20 → 185.X.X.X

Now we know which machine made that connection.

## Important idea

During live investigation, write down:

- Hostname
- IP
- MAC
- Time
- Timezone

These become our reference points later.

---

# 3. OS Version and Installation Details

Command:

Get-CimInstance -ClassName Win32_OperatingSystem | fl CSName, Version, BuildNumber, InstallDate, LastBootUpTime, OSArchitecture

Important fields:

| Field | Meaning |
|---|---|
| CSName | Computer name |
| Version | Windows version |
| BuildNumber | Exact Windows build |
| InstallDate | When OS was installed |
| LastBootUpTime | Last time system booted |
| OSArchitecture | 32-bit or 64-bit |

## Why is this useful?

Suppose the company says:

> All Windows machines must have the latest approved security build.

But our machine has an old build.

That is worth investigating.

However:

Old Windows version ≠ automatically compromised.

It could simply be:

- Patch failure
- Misconfiguration
- Old machine
- Maintenance problem

So remember:

> An anomaly is not automatically malicious.

We need more evidence.

---

# 4. Date and Timezone

Command:

Get-Date ; Get-TimeZone

Example:

Monday, June 2, 2025 7:58:26 AM

Timezone information:

Id              : ...
StandardName    : ...
BaseUtcOffset   : ...

## Why is this VERY important?

Because almost every forensic investigation depends on time.

Imagine we find:

10:30 AM → PowerShell executed

10:32 AM → Suspicious file created

10:34 AM → External connection

10:35 AM → Account created

We need to know:

> "Are these times actually correct?"

If the system clock is wrong, our entire timeline can become confusing.

## SOC example

Company NTP time:

10:00 AM

Victim machine:

11:30 AM

There is a 1.5 hour difference.

Now we have to account for that while creating the incident timeline.

---

# 5. Reviewing System Policies

Attackers can modify Windows policies to weaken security or help themselves.

MITRE ATT&CK:

T1484.001 — Domain Policy Modification

Command:

Get-GPResultantSetOfPolicy -ReportType HTML -Path (Join-Path -Path (Get-Location).Path -ChildPath "RSOPReport.html")

This creates:

RSOPReport.html

RSOP = Resultant Set of Policy

It basically tells us:

> "Which Group Policies are actually being applied to this machine/user?"

## Why do we care?

Suppose a security policy normally says:

> PowerShell scripts are restricted.

But suddenly the machine has a policy allowing unrestricted script execution.

That is worth investigating.

Other suspicious policy changes could involve:

- Windows Defender
- Firewall
- PowerShell
- Security settings
- User privileges
- Script execution
- Logging

Again:

Policy change ≠ automatically malicious.

We compare it with the organization's baseline.

---

# 6. User Accounts

Attackers often create or modify accounts for persistence.

Important MITRE techniques:

T1136 — Create Account

T1098 — Account Manipulation

T1078 — Valid Accounts

Command:

Get-LocalUser | tee l-users.txt

This lists local users.

Example:

ADMIN123       True
Admin123       True
Admin124       True
DefaultAccount False
Guest           True

## What should we look for?

### 1. Unexpected accounts

Example:

Administrator
Admin123
BackupAdmin
SupportAdmin
HackerAdmin

An unexpected admin account is suspicious.

---

### 2. Similar-looking account names

Example:

Legitimate:

Admin01

Suspicious:

Admin0I

or

Admin01
Admin001

Attackers may create names that look similar to legitimate accounts.

This is called:

> Masquerading

---

### 3. Spelling mistakes

Suppose legitimate account:

AdminUser

But another account is:

AdminUesr

That typo is suspicious.

Why?

Because the attacker may hope that the analyst quickly reads the name and misses it.

---

# 7. Password Properties

Command:

Get-CimInstance -Class Win32_UserAccount -Filter "LocalAccount=True" | Format-Table Name, PasswordRequired, PasswordExpires, PasswordChangeable

Important fields:

| Field | Meaning |
|---|---|
| PasswordRequired | Does the account require a password? |
| PasswordExpires | Does its password expire? |
| PasswordChangeable | Can the password be changed? |

## Big red flag

Guest:

PasswordRequired = False

This means:

> The account does not require a password.

That does NOT automatically mean compromise.

But if:

- Guest account is enabled
- No password is required
- Guest is currently logged in

then the situation becomes much more suspicious.

---

# 8. User Group Membership

Command:

Get-LocalGroup | ForEach-Object { $members = Get-LocalGroupMember -Group $_.Name; if ($members) { Write-Output "`nGroup: $($_.Name)"; $members | ForEach-Object { Write-Output "`tMember: $($_.Name)" } } } | tee gp-members.txt

This tells us:

> Which users belong to which groups?

Most important group:

Administrators

Because members of this group usually have powerful privileges.

## Example

Administrators:

Admin01
Admin02
AdminTypo

If we expected only:

Admin01

then AdminTypo deserves investigation.

Also check powerful groups such as:

- Administrators
- Backup Operators
- Remote Desktop Users
- Power Users
- Remote Management Users

---

# 9. Current Sessions

A user account may exist but may not currently be logged in.

Therefore we also check:

> Who is actually using the machine right now?

Tool:

PsLoggedon64.exe

Command:

.\PsLoggedon64.exe | tee sessions.txt

Example:

Users logged on locally:

Admin01
Guest

## Why is this important?

Suppose we discover:

Guest account exists.

Normally that is already suspicious.

Then we discover:

Guest is CURRENTLY logged in.

Now our suspicion increases significantly.

Why?

Because an attacker could potentially be using that account.

But still:

> Suspicious ≠ confirmed attacker.

We need correlation.

---

# 10. Active Network Connections

This is one of the MOST important SOC checks.

Attackers may:

- Maintain C2
- Download payloads
- Exfiltrate data
- Move laterally
- Access the machine remotely

MITRE:

TA0011 — Command and Control

TA008 — Lateral Movement

Command:

Get-NetTCPConnection | select Local*, Remote*, State, OwningProcess, @{n="ProcName";e={(Get-Process -Id $_.OwningProcess).ProcessName}}, @{n="ProcPath";e={(Get-Process -Id $_.OwningProcess).Path}} | sort State | ft -Auto | tee tcp-conn.txt

The important information is:

| Field | Meaning |
|---|---|
| LocalAddress | Victim's IP |
| LocalPort | Victim's port |
| RemoteAddress | Other machine's IP |
| RemotePort | Other machine's port |
| State | Connection state |
| OwningProcess | PID responsible |
| ProcName | Process name |
| ProcPath | Location of executable |

---

# 11. How to investigate a network connection

Suppose you see:

Process:

INITIAL_LANTERN.exe

Path:

C:\Users\Administrator\AppData\SpcTmp\INITIAL_LANTERN.exe

Connection:

192.168.1.20 → 45.X.X.X

Ask:

1. Who owns this connection?
2. Which process created it?
3. Where is that process located?
4. Is that path normal?
5. Is the destination IP known?
6. Is this application approved?
7. What is the parent process?
8. Does the process have persistence?

This is how SOC investigation works.

We don't just say:

> "Unknown IP = malware."

We investigate the whole chain.

---

# 12. Port 3389 — RDP

Port:

3389

is commonly associated with:

Remote Desktop Protocol (RDP)

If we are ourselves connected through RDP, seeing port 3389 is expected.

So we don't immediately call it malicious.

This is an important SOC skill:

> Know what YOU are doing before investigating the machine.

Otherwise you may accidentally investigate your own activity as attacker activity.

---

# 13. SSH Connections

If we see several ssh.exe connections on a Windows machine, we should ask:

> Why is SSH being used here?

SSH can be completely legitimate.

But if we find:

ssh.exe

+

suspicious parent process

+

suspicious executable path

+

unknown external IP

then the combination becomes much more interesting.

This is called:

> Correlation

---

# 14. AnyDesk

AnyDesk is legitimate remote-access software.

It can be used by:

- IT administrators
- Employees
- Support teams

But attackers can also abuse legitimate remote-access software.

Therefore:

AnyDesk running ≠ malware

But:

AnyDesk service
+
Startup persistence
+
Firewall rule
+
External connection
+
Unknown user

would be much more suspicious.

This is why we never conclude from one artifact alone.

---

# 15. Temporary Paths

Example:

C:\Users\Administrator\AppData\Local\Temp\malware.exe

This deserves attention.

Why?

Windows normally stores legitimate system executables in places such as:

C:\Windows\System32

or

C:\Program Files

A random executable running from:

AppData
Temp
SpcTmp

is more suspicious.

But again:

> Temp path ≠ automatically malware.

Legitimate software also uses temporary folders.

So we correlate it with:

- Signature
- Hash
- Parent process
- Network connection
- Persistence
- Creation time

---

# 16. Network Shares

Network shares are folders/drives accessible through the network.

Command:

Get-CimInstance -Class Win32_Share | tee net-shares.txt

Example:

ADMIN$     C:\Windows
C$         C:\
IPC$

These are standard Windows administrative shares.

## Why are they important?

Attackers can use network shares for:

- Lateral movement
- Tool transfer
- Data collection
- Malware distribution

MITRE:

T1039 — Data from Network Shared Drive

T1570 — Lateral Tool Transfer

T1021 — Remote Services

T1080 — Taint Shared Content

---

# 17. Firewall

Firewall controls network traffic.

First check firewall profiles:

Get-NetFirewallProfile | ft Name, Enabled, DefaultInboundAction, DefaultOutboundAction | tee fw-profiles.txt

Example:

Domain   False
Private  False
Public   False

If firewall is completely disabled, ask:

> Is this normal for this organization?

It could be:

- Legitimate configuration
- Another security product is handling network security
- Misconfiguration
- Attacker disabling defenses

MITRE:

T1562 — Impair Defenses

---

# 18. Firewall Rules

Command:

.\fw-summary.ps1 | tee fw-rules.txt

We inspect:

- Port
- Protocol
- Direction
- Action
- Program
- Remote address

Example:

Inbound
TCP
Port 4444
Allow
malicious.exe

That would be highly suspicious.

But a rule like:

AnyDesk → Allow

could be legitimate.

So again:

> Rule + context = conclusion

---

# 19. Boot-Time Execution

Attackers love startup locations because they provide persistence.

Meaning:

> "Whenever the computer starts, execute my program."

MITRE persistence techniques can use:

- Services
- Registry
- Startup folders
- Scheduled tasks
- Boot execution

---

# 20. Autoruns

Tool:

Autoruns64.exe

Command:

.\autorunsc64.exe -a b * -h | tee boot.txt

Here:

-a b

means we are asking Autoruns for boot-related entries.

-h

means show hash information.

Example:

BootExecute

autocheck autochk

Path:

C:\Windows\System32\autochk.exe

This is legitimate Windows functionality.

So:

autochk.exe ≠ suspicious

We verify:

- Path
- Hash
- Signature
- Publisher

---

# 21. Startup Programs

Command:

Get-CimInstance Win32_StartupCommand | Select-Object Name, command, Location, User | fl | tee autorun-cmds.txt

Example:

RunWallpaperSetup
RunWallpaperSetup.cmd

AnyDesk
C:\PROGRA~2\AnyDesk\AnyDesk.exe --control

SecurityHealth
%windir%\system32\SecurityHealthSystray.exe

These programs can automatically execute when Windows starts/logs in.

## What should we ask?

- Is the program expected?
- Is the user expected?
- Is the path legitimate?
- Is the file signed?
- Was it recently created?
- Does it make network connections?

---

# 22. Boot vs Logon

Very important:

### Boot-time

Runs when the machine starts.

Example:

Services
BootExecute

### Logon-time

Runs when a user logs in.

Example:

Winlogon
Userinit
Startup programs

Think:

Computer ON

↓

Boot persistence

↓

Windows starts

↓

User logs in

↓

Logon persistence

---

# 23. Winlogon Userinit

Registry path:

HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit

Normally we expect something like:

C:\Windows\system32\userinit.exe

But investigation showed:

C:\Windows\system32\userinit.exe, cmd.exe

That means:

userinit.exe

↓

cmd.exe

is also executed during logon.

This is suspicious because an attacker may use it for persistence.

---

# 24. Why don't we stop at Userinit?

This is VERY important.

Finding:

Userinit modified

does NOT tell us the complete attack.

We ask:

> What is Userinit launching?

We find:

userinit.exe
    ↓
cmd.exe

Then:

> What is cmd.exe doing?

We find:

cmd.exe
    ↓
netsh.exe

Then:

> What is netsh.exe doing?

We find:

netsh.exe
    ↓
suspicious DLL

Now we have an actual execution chain.

This is the mindset of a SOC/DFIR analyst.

---

# 25. Winlogon Shell

Registry path:

HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell

Normally:

explorer.exe

If this value is changed to something suspicious, investigate it.

---

# 26. Netsh

netsh.exe is a legitimate Windows networking utility.

But attackers can abuse legitimate Windows tools.

This is called:

> Living-off-the-Land

Meaning:

> Instead of bringing their own obvious malware, attackers use trusted Windows tools.

The suspicious chain in this investigation was:

Userinit
   ↓
cmd.exe
   ↓
netsh.exe
   ↓
Suspicious DLL

This is much more powerful evidence than simply saying:

"Userinit was modified."

---

# 27. Services

Services are programs that run in the background.

They are loaded during the Windows boot process.

This makes services excellent persistence mechanisms.

Command:

"Running Services:"; Get-CimInstance -ClassName Win32_Service | Where-Object { $_.State -eq "Running" } | Select-Object Name, DisplayName, State, StartMode, PathName, ProcessId | ft -AutoSize | tee services-active.txt

Important fields:

| Field | Meaning |
|---|---|
| Name | Service name |
| DisplayName | Human-readable name |
| State | Running/Stopped |
| StartMode | Auto/Manual/etc. |
| PathName | Executable being launched |
| ProcessId | Process associated with service |

---

# 28. What makes a service suspicious?

Example:

Service:

LMVCSS

Path:

C:\Users\Administrator\AppData\Temp\something.exe

Immediately ask:

> Why is a Windows service running an executable from a temporary directory?

Then check:

- Hash
- Digital signature
- Creation time
- Parent process
- Network connections
- Service creation time
- Startup configuration

If the same executable is also making an external network connection:

suspicion increases.

---

# 29. Important: Don't conclude too early

Suppose:

AnyDesk service exists.

That alone does NOT prove compromise.

It could be:

> IT support software.

But if we find:

AnyDesk service
+
Startup entry
+
Firewall rule
+
External connection
+
Unknown user

then we have a stronger case.

This is:

> Correlation of multiple artifacts.

---

# 30. Stopped Services Can Also Be Important

Command:

Get-CimInstance -ClassName Win32_Service | Where-Object { $_.State -ne "Running" } | Select-Object Name, DisplayName, State, StartMode, PathName, ProcessId | Format-Table -AutoSize | Tee-Object services-idle.txt

Do not ignore stopped services.

Example:

Aurora-Agent

State:

Stopped

StartMode:

Auto

This is interesting.

Why?

Because:

Auto + Stopped

could mean:

1. Legitimate service failure
2. Security agent is broken
3. Attacker disabled it

If the executable behind it is also malicious:

suspicion becomes much stronger.

This can indicate:

T1562 — Impair Defenses

---

# 31. Scheduled Tasks

Scheduled tasks allow Windows to automatically execute something:

- At a specific time
- At startup
- At logon
- When an event happens
- Under a specific account

Attackers love them for persistence.

Example:

Scheduled Task

Name:

malicious-update

Author:

SYSTEM

Execute:

C:\Users\Public\malware.exe

This deserves investigation.

---

# 32. Scheduled Task Investigation

Command:

$tasks = Get-CimInstance -Namespace "Root/Microsoft/Windows/TaskScheduler" -ClassName MSFT_ScheduledTask

The investigation output showed:

141 scheduled tasks found.

We don't need to manually memorize every task.

Instead:

> Look for unusual tasks.

Especially:

- Running tasks
- SYSTEM tasks
- Unknown names
- Suspicious paths
- Temp/AppData executables
- Recently created tasks
- Tasks executing PowerShell
- Tasks executing scripts

---

# 33. Important Correlation Example

We found:

Aurora-Agent service

↓

Suspicious executable

Then scheduled tasks also show:

aurora-agent-program-update

↓

same executable

Now our confidence increases.

Why?

Because two independent persistence/execution mechanisms point to the same file.

This is extremely valuable during investigation.

---

# 34. Processes

Processes are programs currently running in memory.

Attackers may use processes for:

- Execution
- C2
- Credential theft
- Process injection
- Defense evasion
- Persistence

MITRE:

T1055 — Process Injection

T1036.009 — Break Process Trees

Command:

Get-WmiObject -Class Win32_Process | ForEach-Object {$owner = $_.GetOwner(); [PSCustomObject]@{Name=$_.Name; PID=$_.ProcessId; P_PID=$_.ParentProcessId; User="$($owner.User)"; CommandLine=if ($_.CommandLine.Length -le 60) { $_.CommandLine } else { $_.CommandLine.Substring(0, 60) + "..." }; Path=$_.Path}} | ft -AutoSize | tee process-summary.txt

Important fields:

| Field | Meaning |
|---|---|
| Name | Process name |
| PID | Process ID |
| P_PID | Parent Process ID |
| User | Account running it |
| CommandLine | How it was executed |
| Path | Location of executable |

---

# 35. Process Tree

This is VERY important.

Suppose:

aurora-agent.exe
       ↓
ssh.exe

This means:

> aurora-agent.exe started ssh.exe.

Now imagine:

WINWORD.EXE
       ↓
powershell.exe
       ↓
download.exe

That is much more interesting.

Why?

Because the parent-child relationship tells us:

> How the execution actually happened.

---

# 36. Suspicious Process Names

Attackers may name malware:

svchost.exe
explorer.exe
lsass.exe
services.exe

to look legitimate.

But don't trust the name.

Always check:

> Process name + Path + Signature + Parent + Network

Example:

svchost.exe

Legitimate:

C:\Windows\System32\svchost.exe

Suspicious:

C:\Users\Administrator\AppData\Temp\svchost.exe

The second one deserves investigation.

---

# 37. Temporary Directories

Command:

Get-ChildItem -Path "C:\Users" -Force | Where-Object { $_.PSIsContainer } | ForEach-Object { Get-ChildItem -Path "$($_.FullName)\AppData\Local\Temp" -Recurse -Force -ErrorAction SilentlyContinue | Select-Object @{Name='User';Expression={$_.FullName.Split('\')[2]}}, FullName, Name, Extension } | ft -AutoSize | tee temp-folders.txt

This checks temporary directories for different users.

Why?

Attackers may leave:

- Malware
- Scripts
- Payloads
- Tools
- Stolen data

inside temporary locations.

---

# 38. Suspicious SpcTmp Directory

Investigation found:

C:\Users\Administrator\AppData\SpcTmp\INITIAL_LANTERN.exe

and:

C:\Users\Administrator\AppData\SpcTmp\Invoke-SocksProxy.psm1

This is VERY interesting.

Why?

We have:

INITIAL_LANTERN.exe
+
Invoke-SocksProxy.psm1

A file named:

Invoke-SocksProxy.psm1

suggests a PowerShell module related to SOCKS proxy functionality.

A SOCKS proxy can be used to route traffic through the compromised machine.

So this path deserves deeper investigation.

---

# 39. Disk Volumes

Command:

Get-CimInstance -ClassName Win32_Volume | ft -AutoSize DriveLetter, Label, FileSystem, Capacity, FreeSpace | tee disc-volumes.txt

This tells us:

- Drive letter
- Volume label
- File system
- Capacity
- Free space

Example:

C:   NTFS   33 GB

and another:

No drive letter
NTFS
1 GB

A volume without a drive letter can be completely legitimate.

Windows has hidden/system partitions.

But during an investigation:

> Unexpected hidden volumes deserve investigation.

Never automatically call them malicious.

---

# 40. The MOST Important Investigation Rule

Never investigate one artifact in isolation.

Bad investigation:

"AnyDesk exists → malware."

Better investigation:

AnyDesk service
+
AnyDesk startup entry
+
AnyDesk firewall rule
+
AnyDesk network connection
+
Unknown account

↓

Higher suspicion

↓

Investigate further

---

# 41. How a SOC Analyst Thinks

When you find something suspicious, ask:

## Question 1

What is it?

Example:

LMVCSS.exe

## Question 2

Where is it?

C:\Users\...\AppData\Temp\LMVCSS.exe

## Question 3

Who started it?

Service

## Question 4

When does it start?

At boot

## Question 5

What does it connect to?

Unknown external IP

## Question 6

What does it spawn?

ssh.exe

## Question 7

Is there another persistence mechanism?

Scheduled task

## Question 8

Is there another execution chain?

Userinit
→ cmd
→ netsh
→ suspicious DLL

Now we have a story.

---

# 42. Example Attack Story

Possible investigation chain:

Initial Access
      ↓
Attacker gets access
      ↓
Malicious executable placed in AppData/Temp
      ↓
LMVCSS service created
      ↓
Service starts automatically
      ↓
External network connection
      ↓
SSH activity
      ↓
Scheduled task provides additional persistence
      ↓
Winlogon Userinit modified
      ↓
cmd.exe executes
      ↓
netsh.exe executes
      ↓
Suspicious DLL loaded

This is much stronger than saying:

> "I found a suspicious file."

---

# 43. Final SOC Checklist

When performing Windows live investigation, remember:

### System

- Hostname
- IP
- MAC
- OS version
- Build
- Last boot
- Architecture
- Timezone

### Policies

- Group Policy
- Security policies
- Firewall policies
- PowerShell policies

### Users

- New accounts
- Admin accounts
- Disabled/enabled accounts
- Password settings
- Group memberships
- Current sessions

### Network

- Listening ports
- Established connections
- Remote IPs
- Remote ports
- Owning process
- Process path
- Network shares
- Firewall rules

### Persistence

- Services
- Scheduled tasks
- Startup entries
- Boot entries
- Winlogon
- Userinit
- Shell
- PowerShell profiles

### Processes

- Process name
- Path
- PID
- Parent PID
- User
- Command line
- Network connections

### Files

- Temp directories
- AppData
- Suspicious executables
- Scripts
- DLLs
- Hashes
- Digital signatures

### Storage

- Disk volumes
- Hidden volumes
- Unusual partitions

---

# 44. Golden Rule

The biggest lesson from this entire Windows Incident Surface task is:

> NEVER stop at the first suspicious artifact.

Instead:

Suspicious artifact
        ↓
Ask WHY?
        ↓
Find what launched it
        ↓
Find what it launched
        ↓
Check network activity
        ↓
Check persistence
        ↓
Check file/path/signature
        ↓
Correlate timestamps
        ↓
Build the attack story
        ↓
Then make a conclusion

That is the difference between:

"Finding suspicious things"

and

"Performing a SOC investigation."
