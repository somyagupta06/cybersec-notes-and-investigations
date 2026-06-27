# Linux Incident Surface - Processes and Network Investigation

## What is Linux Attack Surface?

Linux Attack Surface is every place where an attacker can enter the system.

Think like a house.

- Doors
- Windows
- Roof

If there are more doors, the thief has more ways to enter.

A Linux system is the same.

Some common entry points are:

- Open ports
- Running services
- Vulnerable software
- Network communication

### Goal

Reduce the number of entry points before an attack happens.

---

## What is Linux Incident Surface?

Linux Incident Surface is every place where a SOC analyst can find evidence after the attack.

Think like a detective.

The thief already entered the house.

Now your job is not to stop the thief.

Your job is to find:

- Where did the thief enter?
- What did the thief change?
- What evidence did the thief leave?

### Common Incident Surfaces

- System logs
- Running processes
- Network connections
- Running services
- Files
- File integrity

### SOC Goal

- Detect the attack
- Find the evidence
- Understand what happened
- Stop the attack
- Recover the system

---

# Attack Surface vs Incident Surface

| Attack Surface | Incident Surface |
|---------------|------------------|
| Before attack | After attack |
| Used by attacker | Used by SOC analyst |
| Entry points | Evidence points |
| Goal is prevention | Goal is investigation |

---

# Why are Processes Important?

Everything running in Linux is a process.

Examples

- Browser
- SSH
- Python
- Apache
- Malware

If malware is running, it must run as a process.

That is why processes are one of the most important evidence sources.

---

# Activity 1 - Running a Process

A C program was compiled and executed.

The executable was placed inside:

/tmp/simple

The process kept running.

Now the SOC analyst investigates it.

---

# Why is /tmp Interesting?

The /tmp directory stores temporary files.

Attackers often use this directory because:

- Many users ignore it.
- Files can be deleted easily.
- It is commonly used for temporary data.

Important:

A process running from /tmp is NOT always malicious.

Always investigate the context before making a conclusion.

---

# Investigating Running Processes

Command

ps aux

This command shows all running processes.

It helps the SOC analyst answer:

- What is running?
- Who started it?
- When did it start?
- Which user owns it?

---

## Important Fields

### USER

Shows the owner of the process.

Example

www-data

This may suggest a web server process.

---

### PID

Unique Process ID.

Used to investigate the process further.

---

### CPU

Shows CPU usage.

Very high CPU may indicate:

- Crypto miner
- Infinite loop
- Malware

---

### MEM

Shows memory usage.

---

### TTY

Shows which terminal started the process.

"?" usually means the process is running in the background.

---

### STAT

Shows process state.

Examples

R = Running

S = Sleeping

Z = Zombie

---

### START

Shows when the process started.

Useful for building the attack timeline.

---

### COMMAND

Shows exactly what started the process.

This is one of the most useful fields.

---

# Finding One Process

Command

ps aux | grep simple

Shows only the process named "simple".

Useful when searching for one specific process.

---

# Investigating Open Files

Command

lsof -p PID

This command shows everything opened by the process.

Examples

- Files
- Libraries
- Network sockets
- Devices

SOC analysts use it to understand what the process is doing.

---

# Process with Network Connection

Some processes communicate with remote systems.

This is normal for:

- Browsers
- Web servers

But it can also be used by malware.

Example

Malware

↓

Reverse Shell

↓

Attacker's Server

---

# Investigating Network Connections

Command

lsof -i -P -n

This command shows network connections.

Useful information includes:

- Local IP
- Remote IP
- Local Port
- Remote Port
- Process using the connection

---

# Why Use -P and -n?

-P

Shows port numbers.

-n

Shows IP addresses.

This makes investigation faster.

---

# Using Osquery

Osquery allows analysts to search system information using SQL.

Example query

SELECT pid, fd, socket, local_address, remote_address
FROM process_open_sockets
WHERE pid = PID;

This helps identify which process is communicating with which IP address.

---

# Process Red Flags

A SOC analyst should investigate when seeing:

- Process running from /tmp
- Unknown parent-child process
- Unknown network connection
- Orphan process
- Process started by cron
- System binary running from a user directory

These are not always malicious.

They simply require investigation.

---

# SOC Investigation Flow

Alert

↓

Find suspicious process

↓

Check owner

↓

Check executable path

↓

Check parent process

↓

Check open files

↓

Check network connections

↓

Check logs

↓

Build the attack timeline

↓

Contain the incident

---

# Key Takeaways

- Attack Surface is where attackers enter.
- Incident Surface is where analysts find evidence.
- Every running malware is a process.
- A process running from /tmp is suspicious, but not automatically malicious.
- Always investigate the process owner, path, parent process, network connection, and logs.
- Never make conclusions without evidence.

---


# Linux Incident Surface - Persistence Investigation

## What is Persistence?

Persistence means keeping access to a system after the first attack.

Think about a thief.

The thief enters a house.

Before leaving, the thief secretly makes another key.

Now even if the front door is locked, the thief can come back.

Attackers do the same thing in Linux.

### Attacker Goal

- Keep access
- Return later
- Survive system reboot
- Avoid losing access

### SOC Goal

- Find how the attacker kept access
- Remove every persistence method
- Prevent the attacker from coming back

---

# Common Persistence Methods

- Create a new user
- Add user to sudo group
- Create cron jobs
- Install malicious services

---

# Activity 1 - Backdoor User

The attacker creates a new account.

Example

useradd attacker -G sudo

passwd attacker

The attacker also gives the account sudo permission.

This allows the attacker to become root whenever needed.

---

# Why is This Dangerous?

The attacker no longer depends on the original exploit.

Even if the web vulnerability is fixed,

the attacker can simply log in using the new account.

---

# SOC Investigation

## Step 1 - Check Logs

Location

/var/log/

Many important logs are stored here.

Examples

- auth.log
- syslog
- kern.log

---

## auth.log

Command

cat auth.log | grep useradd

This log records user creation activities.

A SOC analyst can learn:

- Who created the user
- When the user was created
- Which command was used
- Which terminal started the command

---

## Example Investigation

Evidence

useradd attacker -G sudo

Questions

- Is this account expected?
- Who created it?
- Was there an approved request?
- Was it created during office hours?

Unknown users should always be investigated.

---

# /etc/passwd

Location

/etc/passwd

This file stores information about every user.

It does NOT store passwords.

Passwords are stored in:

/etc/shadow

---

## Information Inside /etc/passwd

- Username
- User ID (UID)
- Group ID (GID)
- Home directory
- Default shell

Example

attacker:x:1001:1001::/home/attacker:/bin/sh

---

## SOC Checks

Look for:

- Unknown users
- Unexpected shells
- Strange home directories
- Unusual User IDs

---

# Activity 2 - Cron Jobs

## What is Cron?

Cron is a task scheduler.

It automatically runs commands at a specific time.

Examples

- Daily backup
- Weekly cleanup
- Monthly report

---

## Why Attackers Use Cron

The attacker wants malware to run again automatically.

Even if the malware is stopped,

Cron starts it again.

This creates persistence.

---

## Common Malicious Examples

Run every reboot

@reboot script.sh

Run every minute

* * * * * script.sh

---

# SOC Investigation

Check user cron jobs.

Location

/var/spool/cron/crontabs/

Look for:

- Unknown scripts
- Python files
- Bash scripts
- Files running from /tmp
- Files running from user directories

Always ask:

"Should this task really exist?"

---

# Activity 3 - Services

## What is a Service?

A service is a background program.

Many services start automatically when Linux boots.

Examples

- SSH
- Apache
- MySQL

---

## Why Attackers Use Services

The attacker installs malware as a service.

Every reboot,

Linux automatically starts the malware.

This creates long-term persistence.

---

# Service Configuration

Location

/etc/systemd/system/

Every service has a configuration file.

Example

suspicious.service

---

## Important Fields

### Description

Simple name of the service.

---

### ExecStart

Shows which program will run.

This is one of the most important fields.

Always verify the executable path.

---

### Restart=on-failure

If the process crashes,

Linux starts it again automatically.

This makes persistence stronger.

---

### User

Shows which user runs the service.

Unexpected users should be investigated.

---

# Starting a Service

The service is:

- Loaded
- Enabled
- Started

After that,

it runs automatically.

---

# SOC Investigation

## Step 1

Check installed services.

Location

/etc/systemd/system/

Look for:

- Unknown service names
- Services with strange descriptions
- Services pointing to unusual files

---

## Step 2

Check syslog.

Command

cat /var/log/syslog | grep suspicious

This helps identify:

- Service start time
- Errors
- Restarts
- Failures

---

## Step 3

Check Journal Logs.

Command

journalctl -u suspicious

This shows logs for one specific service.

Useful information includes:

- When the service started
- Errors
- Restart attempts
- Failed executions

Sometimes attackers make mistakes.

Journal logs can reveal those mistakes.

---

# SOC Investigation Flow

Alert

↓

Check auth.log

↓

Check /etc/passwd

↓

Look for unknown users

↓

Check Cron Jobs

↓

Check Services

↓

Review syslog

↓

Review journalctl

↓

Build the attack timeline

↓

Remove persistence

---

# Key Takeaways

- Persistence allows attackers to return after the first attack.
- New users should always be verified.
- Unknown sudo users are high priority.
- Cron jobs can restart malware automatically.
- Malicious services can survive every reboot.
- auth.log, /etc/passwd, syslog, and journalctl are important evidence sources.
- Never assume an activity is malicious without evidence.
- Always investigate using context before making a conclusion.

---

# Linux Incident Surface - Disk and Logs Investigation

## What is Linux Incident Surface on Disk?

Attackers do not only leave evidence in memory.

They also leave evidence on the disk.

A SOC analyst investigates these disk locations to understand:

- What changed?
- When did it change?
- Who changed it?
- Is it normal or suspicious?

---

# Important Files

These files contain important security information.

---

## /etc/passwd

This file stores information about every user.

It does NOT store passwords.

Information stored:

- Username
- User ID (UID)
- Group ID (GID)
- Home directory
- Default shell

### SOC Checks

Look for:

- Unknown users
- Unexpected home directories
- Strange login shells
- Recently created accounts

---

## /etc/shadow

This file stores password hashes.

Passwords are NOT stored in plain text.

### Why is it Important?

If an attacker steals this file,

they may try to crack the password offline.

### SOC Checks

- Verify file permissions.
- Check if the file was modified unexpectedly.
- Investigate unauthorized access.

---

## /etc/group

This file stores Linux groups.

Groups control user permissions.

Example

A user added to the sudo group can run administrative commands.

### SOC Checks

Look for:

- Unknown users inside privileged groups.
- Users added to sudo without approval.

---

## /etc/sudoers

This file controls sudo permissions.

It decides who can become root.

### Why is it Important?

Attackers may modify this file to gain permanent administrator access.

### SOC Checks

Look for:

- Unknown users
- Unexpected sudo permissions
- Unauthorized changes

---

# Malicious Debian Package

Attackers may create a fake Debian package.

The victim installs the package,

and malicious code runs automatically.

The package may:

- Install malware
- Create new users
- Start a reverse shell
- Create persistence

---

# How a Malicious Package Works

## Step 1

Create a package directory.

---

## Step 2

Create a control file.

The control file stores package information.

Example

- Package name
- Version
- Description
- Maintainer

Think of it as the package identity.

---

## Step 3

Create a post-install script.

File name

postinst

This script automatically runs after installation.

This is where attackers place malicious commands.

---

## Step 4

Make the script executable.

Now Linux can execute the script.

---

## Step 5

Build the package.

The folder becomes a .deb package.

---

## Step 6

Install the package.

The post-install script runs automatically.

The attacker now has code execution.

---

# SOC Investigation

## Check Installed Packages

Command

dpkg -l

This command lists every installed package.

### SOC Questions

- Is this package expected?
- Is it company approved?
- Was it recently installed?
- Does the name look suspicious?

Unknown packages should always be investigated.

---

## Check Installation History

Location

/var/log/dpkg.log

This log records package installation activities.

### Example Information

- Package name
- Installation time
- Package version

This helps build the attack timeline.

---

# Why is dpkg.log Important?

Example

Timeline

09:00 User login

↓

09:10 Unknown package installed

↓

09:11 Malware starts

This strongly suggests the package may be related to the attack.

---

# Linux Logs

Logs record everything happening inside Linux.

Think of logs as the system diary.

If something happens,

there is often a log entry.

SOC analysts use logs to reconstruct the attack.

---

# Important Logs

## Syslog

Location

/var/log/syslog

Contains

- System events
- Service activity
- Warnings
- Errors
- Kernel messages

### SOC Use

Use syslog to identify:

- Service failures
- System problems
- Unexpected application activity
- Timeline of events

---

## Messages

Location

/var/log/messages

Contains

- General system activity
- Kernel messages
- Hardware events

### SOC Use

Look for:

- Hardware errors
- Repeated kernel errors
- System instability
- Possible denial-of-service activity

---

## Authentication Log

Location

/var/log/auth.log

Contains

- Successful logins
- Failed logins
- SSH authentication
- sudo activity
- User creation
- Password changes

### SOC Use

Look for:

- Brute-force attacks
- Unknown logins
- New users
- Unexpected sudo commands
- Login at unusual times

---

# Common Incident Examples

A SOC analyst should investigate when seeing:

- Multiple failed login attempts
- Successful login at unusual hours
- Unknown network connections
- System errors
- New user on a sensitive server
- Outbound traffic from a web server
- Recently installed unknown package

---

# SOC Investigation Flow

Alert

↓

Check auth.log

↓

Check syslog

↓

Check installed packages

↓

Review dpkg.log

↓

Check users

↓

Check sudo permissions

↓

Correlate all evidence

↓

Build the attack timeline

↓

Contain the incident

---

# Key Takeaways

- Attackers leave evidence on the disk.
- Configuration files are important forensic artifacts.
- /etc/passwd stores user information.
- /etc/shadow stores password hashes.
- /etc/group stores group membership.
- /etc/sudoers controls administrator access.
- Unknown Debian packages should always be investigated.
- dpkg.log helps identify when a package was installed.
- Logs help answer who, when, what, and how.
- Never trust a single artifact. Always correlate multiple pieces of evidence before reaching a conclusion.
