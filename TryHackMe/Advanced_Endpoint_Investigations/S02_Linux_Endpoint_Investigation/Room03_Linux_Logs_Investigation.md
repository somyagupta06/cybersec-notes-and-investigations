# Linux Logging - Part 1 (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Understand where Linux stores evidence and how to investigate it.

---

# Why Logs Matter

Think of a Linux system like a school.

Every important activity is written in a notebook.

For example,

- A student enters the school.
- A teacher opens a classroom.
- The principal changes a rule.
- The electricity goes off.

Everything is recorded.

Linux works in the same way.

Every important event is written into log files.

These logs help a SOC analyst answer questions like:

- Who logged in?
- What command was executed?
- Did someone fail to log in many times?
- Was a malicious service started?
- Did the kernel report an error?

Without logs, an investigation becomes much harder.

---

# Two Types of Logs

Linux has two major logging categories.

## 1. Kernel Logs

Kernel logs record everything happening inside the operating system.

Think of the kernel as the **brain** of Linux.

It controls:

- CPU
- Memory
- Drivers
- Hardware
- File system
- Process management

Whenever something important happens inside the operating system, the kernel records it.

Examples:

- USB device connected
- Disk failure
- Driver crash
- File system corruption
- Kernel module loaded
- Rootkit loaded

---

## 2. User Logs

User logs record activities performed by users and applications.

Examples:

- User login
- SSH login
- sudo command
- Cron job execution
- Apache request
- Service started

These logs are used most often during SOC investigations.

---

# Quick Comparison

| Kernel Logs | User Logs |
|-------------|-----------|
| Created by Linux Kernel | Created by Users and Applications |
| Hardware events | Login events |
| Driver messages | SSH logs |
| File system issues | sudo commands |
| Kernel module loading | Cron jobs |
| Used for deep system investigation | Used for security investigation |

---

# Log Severity Levels

Not every log is equally important.

Linux gives every log a severity level.

Think of it like a hospital.

---

## EMERGENCY

Meaning

The entire system is unusable.

Example

The operating system crashes.

SOC Priority

⭐⭐⭐⭐⭐ Highest

---

## ALERT

Meaning

Someone must immediately investigate.

Example

Critical security service stopped.

SOC Priority

⭐⭐⭐⭐⭐

---

## CRITICAL

Meaning

A serious problem happened.

Example

Hard disk failure.

SOC Priority

⭐⭐⭐⭐

---

## ERROR

Meaning

Something failed.

Example

Application crashed.

SOC Priority

⭐⭐⭐

---

## WARNING

Meaning

Not dangerous yet, but could become a problem.

Example

Disk space becoming low.

SOC Priority

⭐⭐⭐

---

## NOTICE

Meaning

An important event happened.

Example

System reboot.

SOC Priority

⭐⭐

---

## INFO

Meaning

Normal activity.

Example

User logged in successfully.

SOC Priority

⭐

---

## DEBUG

Meaning

Very detailed developer information.

Usually used while troubleshooting software.

SOC analysts normally ignore these unless debugging.

---

# Easy Trick to Remember

Imagine a fire.

EMERGENCY

🔥 Whole building burning

↓

ALERT

🚒 Call everyone

↓

CRITICAL

Major damage

↓

ERROR

Something broke

↓

WARNING

Smoke detected

↓

NOTICE

Someone reported smoke

↓

INFO

Everything normal

↓

DEBUG

Camera footage of every second

---

# Kernel Ring Buffer

This is one of the most important Linux concepts.

Imagine a whiteboard.

The kernel keeps writing messages on it.

But...

The whiteboard has limited space.

When it becomes full,

the oldest message is erased,

and the newest message is written.

This is exactly how the Kernel Ring Buffer works.

It stores kernel messages only in RAM.

Because RAM has limited space,

old logs are overwritten.

---

# Important Facts

Location

RAM (Memory)

Storage

Temporary

Survives reboot?

❌ No

Overwrites old logs?

✅ Yes

Stores

Kernel messages only

---

# Why SOC Analysts Care

If malware loads a kernel module,

the ring buffer may record it.

Example

A rootkit is loaded.

The kernel immediately creates messages.

If you investigate quickly,

you may still find those logs.

If you wait too long,

they may already be overwritten.

---

# dmesg

dmesg reads the Kernel Ring Buffer.

Think of it as

"A window to see kernel memory logs."

It does NOT create logs.

It only displays them.

Example information shown:

- Boot messages
- Hardware detection
- Driver loading
- USB devices
- Kernel modules
- File system events

---

# Easy Analogy

Kernel Ring Buffer

↓

Notebook in RAM

↓

dmesg

↓

Person reading the notebook

---

# What Can a SOC Analyst Find?

Example

A rootkit was loaded.

You may see messages like:

- Unknown kernel module loaded
- Module verification failed
- Kernel tainted

These are huge red flags.

---

# What Does "Kernel Tainted" Mean?

Imagine a teacher checking homework.

If the homework is signed,

the teacher trusts it.

If there is no signature,

the teacher says,

"I cannot fully trust this."

Linux behaves the same way.

When an unsigned kernel module is loaded,

the kernel becomes **tainted**.

It does NOT always mean malware.

But it tells investigators:

"Something outside the normal trusted kernel was loaded."

Always investigate.

---

# kern.log

Unlike the Kernel Ring Buffer,

kern.log is stored on disk.

Location

/var/log/kern.log

Think of it like this.

Kernel Ring Buffer

↓

Temporary notebook

↓

rsyslog copies important messages

↓

kern.log

↓

Permanent notebook on disk

---

# Difference

| dmesg | kern.log |
|--------|----------|
| Reads RAM | Stored on Disk |
| Temporary | Persistent |
| Old entries overwritten | Saved until rotated |
| Shows live kernel messages | Historical kernel logs |

---

# Which One Should a SOC Analyst Use?

Need live kernel messages?

Use dmesg.

Need historical investigation?

Use kern.log.

Need both?

Check both.

---

# Rootkit Investigation Example

Suppose you find:

Custom kernel module loaded

Module verification failed

Kernel tainted

SOC Thinking

Step 1

Someone loaded a kernel module.

Step 2

It is not trusted.

Step 3

It could be a legitimate driver.

OR

It could be a rootkit.

Step 4

Collect more evidence before concluding.

Never assume malware without evidence.

---

# SOC Investigation Flow

Alert

↓

Check dmesg

↓

Check kern.log

↓

Look for

- Kernel module loading
- Driver failures
- File system errors
- Kernel tainted
- Hardware issues

↓

Correlate with

- auth.log
- audit.log
- journalctl
- Running processes

↓

Build the attack timeline.

---

# Key Points for Interview

✔ Linux has two logging types:
- Kernel Logs
- User Logs

✔ dmesg reads the Kernel Ring Buffer.

✔ Kernel Ring Buffer exists only in RAM.

✔ Old kernel messages are overwritten.

✔ kern.log stores kernel logs on disk.

✔ Kernel tainted means an untrusted kernel module was loaded.

✔ Always correlate kernel logs with other evidence.

✔ Never conclude malware using only one log source.

---

# Linux Logging - Part 2 (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Learn how to investigate login activity and system events.

---

# auth.log

auth.log is one of the most important log files in Linux.

If someone asks,

"Who logged into the machine?"

"Who used sudo?"

"Who tried SSH?"

The first place a SOC analyst checks is **auth.log**.

Location

/var/log/auth.log

---

# What is Stored in auth.log?

auth.log records authentication-related activities.

Examples

- SSH login
- SSH login failure
- Password authentication
- sudo commands
- su command
- User session opened
- User session closed

Think of auth.log as the **security gate register** of a company.

Every person entering or leaving is recorded.

---

# Example

Suppose the log says

Accepted password for ubuntu

What does this mean?

It means

- Password was correct.
- Authentication was successful.
- The user logged into the system.

This is a FACT.

It does NOT mean the login was malicious.

---

# Failed Login

Suppose the log says

authentication failure

Meaning

Someone tried to log in but failed.

One failure is normal.

Hundreds of failures may indicate a brute-force attack.

---

# SSH Investigation

Imagine the SOC receives this alert:

"Possible SSH Brute Force"

Your investigation starts with auth.log.

Questions to answer:

- Which user was targeted?
- Which IP attempted login?
- How many failures occurred?
- Was there any successful login afterwards?

If many failures are followed by one successful login,

this becomes highly suspicious.

---

# Sudo Activity

Attackers often need administrator privileges.

When someone runs sudo,

auth.log records it.

Example

ubuntu executed:

systemctl enable backup.service

SOC Thinking

Question 1

Who executed the command?

Answer

ubuntu

Question 2

Did the command require root?

Yes.

Question 3

What command was executed?

Enable a service.

Question 4

Why?

Need more evidence.

Never assume malware.

---

# Session Opened

Example

session opened for user root

Meaning

Root access has started.

This only tells us

Root session exists.

It does NOT tell us

Why it was opened.

Always continue investigating.

---

# Session Closed

Example

session closed for user root

Meaning

Root session ended.

Useful for building timelines.

---

# SOC Investigation Flow

Alert

↓

Open auth.log

↓

Find

Accepted password

↓

Identify

User

↓

Identify

Source IP

↓

Find

sudo commands

↓

Find

session opened

↓

Correlate with

Processes

Services

Network Connections

---

# auth.log Alone is NOT Enough

Example

Accepted password for ubuntu

Can you conclude

"The attacker logged in"?

No.

Possible reasons

- Normal administrator
- System owner
- Automation
- Attacker

Need more evidence.

Always correlate.

---

# syslog

syslog is the main system log.

Think of it as

The system diary.

Unlike auth.log,

syslog stores many different system events.

Location

/var/log/syslog

---

# What Can syslog Store?

Examples

- Service started
- Service stopped
- Cron execution
- Network events
- Kernel messages
- Application logs
- System warnings

It collects information from many programs.

---

# Why SOC Analysts Use syslog

Suppose

An attacker creates persistence using Cron.

auth.log

may show

sudo used

But

syslog

shows

Cron actually executed.

This helps build the attack timeline.

---

# Cron Investigation

Suppose syslog says

CRON executed backup.sh

SOC Thinking

Question

Did the scheduled task actually run?

Yes.

Question

When?

The timestamp tells us.

Question

What script was executed?

backup.sh

Question

Need next step?

Read backup.sh

---

# Kernel Messages in syslog

syslog can also contain kernel events.

Example

EXT4 File System Error

SOC Thinking

Possibilities

- Disk problem
- Corruption
- Malware damaging files

Need more evidence.

---

# wtmp

Location

/var/log/wtmp

wtmp records

Successful logins and logouts.

Think of it as

Attendance Register.

---

# What Can You Learn?

- Who logged in
- Login time
- Logout time
- Reboots
- Session duration

---

# Example

ubuntu

Logged in

10:30

Logged out

13:30

Session lasted

3 hours.

Useful for timeline analysis.

---

# Why SOC Uses wtmp

Suppose auth.log says

Accepted password

wtmp confirms

The login actually became a session.

---

# btmp

Location

/var/log/btmp

Think of btmp as

Rejected visitors register.

It stores

Failed login attempts.

---

# Example

root

Failed

root

Failed

root

Failed

root

Failed

If this repeats hundreds of times,

it may indicate

Brute-force attack.

---

# Difference Between auth.log, wtmp and btmp

| Log File | Stores |
|----------|--------|
| auth.log | Authentication events |
| wtmp | Successful logins and logouts |
| btmp | Failed login attempts |

---

# Easy Way to Remember

auth.log

Everything about authentication.

wtmp

Who entered successfully.

btmp

Who failed to enter.

---

# SOC Example

Evidence

auth.log

Accepted password for ubuntu

↓

wtmp

ubuntu logged in

↓

syslog

Cron executed update.sh

↓

Network logs

Outbound connection created

SOC Conclusion

Do NOT conclude compromise yet.

Instead say

"There is evidence of successful login, scheduled task execution, and outbound communication. These events should be correlated with process activity, file analysis, and service configuration before determining whether the system is compromised."

This is professional DFIR language.

---

# Investigation Order

Step 1

Check auth.log

↓

Step 2

Check successful logins (wtmp)

↓

Step 3

Check failed logins (btmp)

↓

Step 4

Check syslog

↓

Step 5

Check running processes

↓

Step 6

Check persistence

- Cron
- Services

↓

Step 7

Check network connections

↓

Step 8

Build timeline

---

# Common Mistakes

❌ One successful login means attacker.

Correct

It could also be a normal administrator.

---

❌ One failed login means brute force.

Correct

One failure is normal.

Hundreds of failures are suspicious.

---

❌ sudo always means attacker.

Correct

Administrators use sudo every day.

Need context.

---

❌ Cron execution means malware.

Correct

Many legitimate jobs use Cron.

Always inspect the scheduled script.

---

# Interview Tips

✔ auth.log is the first place for authentication investigation.

✔ wtmp stores successful logins.

✔ btmp stores failed logins.

✔ syslog stores general system events.

✔ Always correlate multiple logs.

✔ Never conclude compromise from a single log.

✔ Build a timeline before making conclusions.

✔ Evidence first. Hypothesis second. Conclusion last.

---

# Linux Logging - Part 3 (Syslog Deep Dive)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Understand how logs travel from an application to a SIEM.

---

# What is Syslog?

Imagine a school.

Many people want to report something.

- Teacher reports a fight.
- Principal reports an event.
- Guard reports a visitor.
- Electrician reports a power failure.

Instead of everyone creating their own notebook,

they all report to one office.

That office records everything.

Linux works the same way.

Applications and services send their messages to **Syslog**.

Syslog records these messages and stores them in log files.

Think of Syslog as the **central post office for logs**.

---

# Why Do We Need Syslog?

Without Syslog,

every application would create logs in a different way.

That would make investigations very difficult.

Syslog provides one common logging system.

This makes log collection easier.

---

# Evolution of Syslog

Linux has used different logging daemons over time.

---

## 1. syslogd

The oldest logging daemon.

Features

- Basic logging
- Simple configuration

Think of it as

A small notebook.

---

## 2. syslog-ng

A better version.

New Features

- Better filtering
- Network logging
- TCP support

Think of it as

A notebook with folders.

---

## 3. rsyslog

The modern logging daemon.

This is used in most Linux systems today.

Features

- Very fast
- Secure
- Supports encryption (TLS)
- Can send logs to remote servers
- Can store logs in databases

Think of it as

A smart digital notebook.

---

# Easy Comparison

| syslogd | syslog-ng | rsyslog |
|----------|-----------|----------|
| Old | Improved | Modern |
| Basic | More Features | High Performance |
| Local Logs | Better Filtering | Remote Logging |
| No Encryption | Better Transport | TLS Support |

Today,

most SOC analysts work with **rsyslog**.

---

# Main Parts of Syslog

Syslog has three important components.

---

## 1. Syslog Daemon

Example

rsyslogd

Think of it as

The office worker.

Its job is

- Receive logs
- Read logs
- Decide where to store logs
- Forward logs if needed

Without the daemon,

logs would not be managed properly.

---

## 2. Configuration File

Location

/etc/rsyslog.conf

or

/etc/rsyslog.d/

Think of this as

The office rule book.

Example rules

Authentication logs

↓

Store in auth.log

Kernel logs

↓

Store in kern.log

Cron logs

↓

Store in cron.log

The daemon simply follows these rules.

---

## 3. Log Files

These are the final destination.

Usually stored in

/var/log/

Examples

auth.log

kern.log

syslog

mail.log

cron.log

---

# How Logs Travel

Imagine this situation.

A user logs in using SSH.

The flow is

SSH Service

↓

Syslog Daemon

↓

Configuration Rules

↓

auth.log

↓

SOC Analyst investigates

This is exactly how Syslog works.

---

# Syslog Architecture

There are three important roles.

---

## Originator

Think of this as

The sender.

Examples

- SSH
- Apache
- Cron
- Kernel
- sudo
- FTP

These programs create log messages.

---

## Relay

Think of this as

The delivery truck.

Its job

Receive logs

↓

Forward logs

↓

Maybe add extra information

↓

Send to another server

Large companies use relays.

Why?

Because thousands of servers generate logs.

Instead of sending directly,

they first send logs to a relay.

---

## Collector

Think of this as

The warehouse.

Its job

Collect logs

Store logs

Search logs

Visualize logs

Examples

- Splunk
- Elastic
- Graylog
- QRadar

SOC analysts usually work here.

---

# Easy Picture

Application

↓

Originator

↓

Relay

↓

Collector

↓

SOC Analyst

---

# Real SOC Example

Suppose

Apache Web Server

detects

404 Error

Apache

↓

Syslog

↓

Relay

↓

Splunk

↓

SOC Alert

Everything follows this path.

---

# Syslog Message Format

Every log message follows a standard format.

Think of it as

An envelope.

The envelope has different sections.

---

# PRI

PRI means

Priority.

It tells

How important the message is.

PRI is created using

Facility

+

Severity

Example

Authentication Error

↓

Facility = auth

Severity = Error

↓

PRI is calculated.

SOC analysts usually don't calculate PRI manually.

They simply understand

Higher priority

=

More important event.

---

# Header

The header answers

"When?"

"Where?"

"Who?"

It contains

Timestamp

Hostname

Application Name

Process ID

Message ID

Example

Jul 3

Server01

sshd

PID 1500

---

# Message

This is the real event.

Example

Accepted password for ubuntu

Everything before it is metadata.

This is the actual information.

---

# Easy Example

Timestamp

↓

Jul 3

Hostname

↓

Server01

Application

↓

sshd

Process

↓

1522

Message

↓

Accepted password for ubuntu

---

# Why This Matters in SOC

Imagine you receive

Accepted password

Without the hostname,

you don't know

Which server.

Without timestamp,

you don't know

When.

Without application,

you don't know

Who generated it.

Metadata is just as important as the message.

---

# Configuration Example

Imagine this rule

Authentication Logs

↓

auth.log

Kernel Logs

↓

kern.log

Cron Logs

↓

cron.log

This is exactly what rsyslog configuration does.

It tells Linux

"Store this type of log in this file."

---

# SOC Investigation Example

Alert

↓

Multiple Failed SSH Logins

SOC checks

auth.log

↓

Finds

Source IP

↓

Checks

syslog

↓

Finds

Cron execution

↓

Checks

journal

↓

Finds

New service started

↓

Checks

Processes

↓

Finds

Python running

↓

Checks

Network

↓

Finds

Outbound connection

↓

Builds timeline

Notice

No single log proves compromise.

All logs together tell the complete story.

---

# Common Mistakes

❌ Syslog creates logs.

Correct

Applications create logs.

Syslog only collects and stores them.

---

❌ Syslog only stores authentication logs.

Correct

It stores many different types of logs.

---

❌ Collector generates logs.

Correct

Collector only stores and displays logs.

Applications generate logs.

---

# Interview Tips

✔ Syslog is the central logging system.

✔ rsyslog is the most common daemon today.

✔ The daemon manages logs.

✔ Configuration files decide where logs are stored.

✔ Originator creates logs.

✔ Relay forwards logs.

✔ Collector stores logs.

✔ Splunk and Elastic usually act as collectors.

✔ Always correlate logs from multiple sources.

✔ One log never tells the complete attack story.

---

# Linux Logging - Part 4 (SOC Cheat Sheet)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Know where to investigate during different security incidents.

---

# Syslog Severity Levels

Every log has a severity level.

Think of it as the importance of the message.

Higher severity

↓

Needs faster attention.

---

## Severity Table

| Level | Meaning | SOC Priority |
|---------|----------|--------------|
| Emergency | System is unusable | ⭐⭐⭐⭐⭐ |
| Alert | Immediate action needed | ⭐⭐⭐⭐⭐ |
| Critical | Serious problem | ⭐⭐⭐⭐ |
| Error | Something failed | ⭐⭐⭐ |
| Warning | Possible future problem | ⭐⭐⭐ |
| Notice | Important normal event | ⭐⭐ |
| Info | Normal activity | ⭐ |
| Debug | Developer troubleshooting | Usually ignored |

---

# Easy Story

Imagine a hospital.

Emergency

↓

Patient will die immediately.

Alert

↓

Doctor must come now.

Critical

↓

Serious injury.

Error

↓

Medicine could not be given.

Warning

↓

Patient may become sick.

Notice

↓

Patient entered hospital.

Info

↓

Temperature checked.

Debug

↓

Every heartbeat recorded.

---

# Syslog Facilities

Facilities tell us

**Who generated the log?**

Severity tells us

**How serious is the event?**

Example

Apache creates a log.

Facility

↓

daemon

Severity

↓

Error

Meaning

A daemon generated an error.

---

# Common Facilities

| Facility | Meaning |
|-----------|---------|
| kern | Kernel |
| user | User applications |
| auth | Authentication |
| authpriv | Secure authentication |
| daemon | Background services |
| cron | Scheduled tasks |
| mail | Mail server |
| ftp | FTP server |
| local0-local7 | Custom applications |

---

# Easy Trick

Facility answers

"WHO?"

Severity answers

"HOW BAD?"

---

# Real SOC Investigation

## Incident 1

Alert

Multiple failed SSH logins.

Where do you investigate?

✅ auth.log

Why?

Because SSH authentication events are stored there.

---

## Incident 2

Alert

Unknown user logged in.

Check

- auth.log
- wtmp

Why?

Need login evidence.

---

## Incident 3

Alert

Brute Force Attack.

Check

- auth.log
- btmp

Why?

Need failed authentication attempts.

---

## Incident 4

Alert

User became root.

Check

- auth.log
- sudo events

Need to know

Who executed sudo?

What command?

When?

---

## Incident 5

Alert

Unknown process running.

Check

- Running processes
- auditd
- journalctl

Need to know

Who started it?

When?

---

## Incident 6

Alert

Unknown service started.

Check

- journalctl
- systemd service
- auth.log

Need to know

Who enabled it?

What file does it execute?

---

## Incident 7

Alert

System crashes.

Check

- dmesg
- kern.log

Need to know

Kernel errors

Driver failures

Hardware failures

---

## Incident 8

Alert

Cron malware.

Check

- syslog
- Cron configuration

Need to know

Which script executed?

When?

---

## Incident 9

Alert

Web server compromise.

Check

Apache access logs

Apache error logs

Need to know

Client IP

Requested URL

HTTP status

Errors

---

## Incident 10

Alert

Outbound connection.

Check

- Running processes
- Network connections
- auditd
- journalctl

Need to identify

Which process owns the connection?

---

# Evidence Correlation

Never trust only one log.

Example

auth.log

↓

Accepted password

Does this prove compromise?

❌ No.

Now check

wtmp

↓

Login session exists.

Now check

journalctl

↓

Service enabled.

Now check

Processes

↓

Python running.

Now check

Network

↓

Outbound connection.

Now the attack story becomes much stronger.

Always combine evidence.

---

# Investigation Mindset

Instead of asking

"Is this malware?"

Ask

"What evidence supports malware?"

Instead of saying

"The attacker created persistence."

Say

"Evidence suggests persistence through a systemd service because..."

Professional investigators always explain

**Why**

not just

**What**.

---

# Evidence vs Hypothesis

Example

Evidence

Accepted password for ubuntu.

Fact

Someone successfully authenticated.

---

Hypothesis

The attacker logged in.

Need more evidence.

Maybe

- Normal administrator
- Automation
- Attacker

Never jump to conclusions.

---

# Investigation Order

1. Contain the system (if required).

↓

2. Preserve evidence.

↓

3. Capture memory (if possible).

↓

4. Collect logs.

↓

5. Review authentication.

↓

6. Review processes.

↓

7. Review services.

↓

8. Review persistence.

↓

9. Review network activity.

↓

10. Build timeline.

↓

11. Remove malware.

↓

12. Recover system.

Never delete evidence before collecting it.

---

# Common Mistakes

❌ One failed login means brute force.

Correct

Many failures from the same source are suspicious.

---

❌ One successful login means compromise.

Correct

Need additional evidence.

---

❌ Python process always means malware.

Correct

Many legitimate applications use Python.

---

❌ Root user always means attacker.

Correct

Administrators also use root.

---

❌ Restart=always always means malware.

Correct

Many legitimate services restart automatically.

Need context.

---

# Golden Rules for SOC Analysts

Rule 1

One log never tells the whole story.

---

Rule 2

Always build a timeline.

---

Rule 3

Correlate multiple evidence sources.

---

Rule 4

Evidence first.

Hypothesis second.

Conclusion last.

---

Rule 5

Never assume.

Always verify.

---

# Linux Logging Quick Revision

| Log | Purpose |
|------|----------|
| dmesg | Live kernel messages from RAM |
| kern.log | Kernel logs stored on disk |
| auth.log | Authentication events |
| syslog | General system events |
| wtmp | Successful logins and logouts |
| btmp | Failed login attempts |
| journalctl | Systemd logs |
| audit.log | Detailed security events |
| Apache Access Log | Client requests |
| Apache Error Log | Server errors |

---

# 30-Second Interview Revision

Kernel logs

↓

Hardware and kernel events.

---

User logs

↓

Authentication and application events.

---

auth.log

↓

Authentication.

---

wtmp

↓

Successful logins.

---

btmp

↓

Failed logins.

---

syslog

↓

General system events.

---

journalctl

↓

Systemd logs.

---

auditd

↓

Detailed security monitoring.

---

Always

Correlate logs.

Build a timeline.

Collect evidence.

Never assume.

---

# Final SOC Mindset

The goal of a SOC analyst is not to prove an attack happened.

The goal is to collect evidence, verify facts, build a timeline, and explain what happened with confidence.

Good investigators do not guess.

They prove.

---

# Linux Journal & Journalctl (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Learn how to investigate Linux systems using Journal and Journalctl.

---

# Why Do We Need Journal?

Imagine a school.

There are many departments.

- Principal
- Teachers
- Security Guard
- Library
- Accounts

Everyone writes reports every day.

Now imagine someone collects ALL these reports into one smart notebook.

That notebook is called **Journal**.

---

# What is Journal?

Journal is the logging system used by Linux systems that use **systemd**.

Unlike normal log files,

Journal stores logs in a **binary format**.

Think like this.

Old Style

Application

↓

Text Log File

Modern Style

Application

↓

Journal Database

The Journal is much faster to search.

---

# Binary Log

A binary log is NOT normal text.

You cannot easily open it with a text editor.

Linux stores logs in a special format.

Why?

Because searching becomes much faster.

Think of it like this.

Text File

↓

Read line by line.

Journal

↓

Instant search.

---

# journalctl

journalctl is the tool used to read the Journal.

Think of it like this.

Journal

↓

Smart Database

↓

journalctl

↓

Search Tool

journalctl does NOT create logs.

It only reads them.

---

# What Can journalctl Show?

journalctl can show

- Kernel logs
- Service logs
- User logs
- Boot logs
- Authentication logs
- Application logs

Think of journalctl as

"Google Search for Linux Logs."

---

# Where are Journal Logs Stored?

Normally,

Journal logs are stored in memory.

That means

After reboot,

they are deleted.

This is called

Volatile Storage.

---

# Persistent Journal

If the administrator wants to keep logs after reboot,

Journal can save logs to disk.

Configuration file

/etc/systemd/journald.conf

Storage option

persistent

Now logs survive reboot.

---

# Easy Comparison

| Volatile Journal | Persistent Journal |
|-----------------|-------------------|
| Stored in RAM | Stored on Disk |
| Deleted after reboot | Kept after reboot |
| Temporary | Permanent |

---

# Why Does a SOC Analyst Care?

Imagine malware runs.

You investigate immediately.

Good.

Logs are still available.

Now imagine

The attacker reboots the machine.

If Journal was volatile,

all logs disappear.

Evidence is lost.

If Journal was persistent,

you can still investigate.

---

# Viewing Logs

journalctl shows all logs collected by the Journal.

It displays

- Kernel
- Services
- Applications
- Users

Everything together.

Think of it as

The master investigation notebook.

---

# journalctl Filters

journalctl becomes powerful because we can filter logs.

Instead of reading

100,000 logs,

we only read

what we need.

---

# Follow Mode

Imagine CCTV.

New events appear live.

Follow Mode works the same way.

It continuously shows new logs.

SOC Use

Watching a server during an attack.

---

# Kernel Filter

Need only kernel logs?

Use the kernel filter.

Now

Only kernel events appear.

SOC Use

Investigating

- Driver failures
- Kernel panic
- Rootkits
- Hardware issues

---

# Boot Filter

Suppose

A server has rebooted

20 times.

You only want

the previous boot.

Boot filter allows that.

SOC Use

Investigating

"What happened before the reboot?"

---

# Service Filter

Suppose

Apache is suspicious.

Instead of searching every log,

filter only Apache.

SOC Use

Investigate

- nginx
- apache
- ssh
- docker
- mysql

One service at a time.

---

# Priority Filter

Need only important logs?

Filter by priority.

Example

Critical

Now journalctl ignores

Normal messages

and only shows

Critical

Alert

Emergency

SOC Use

Quick investigation during incidents.

---

# Reverse Output

Normally

Logs are shown

Oldest

↓

Newest

Reverse mode

Newest

↓

Oldest

SOC analysts usually prefer

Newest first

because recent activity is often most important.

---

# Number of Lines

Suppose

Journal contains

500,000 logs.

You only need

20.

Limit output.

Much faster.

---

# No Pager

Normally

journalctl opens

a scrolling window.

No Pager

prints everything directly.

Useful for scripting.

---

# SOC Investigation Example

Alert

Unknown Service Started.

Investigation

Open journal

↓

Filter

Only that service

↓

Read

When it started

↓

Who started it

↓

Errors

↓

Failures

↓

Success

This quickly tells the attack story.

---

# Journal vs Syslog

Many beginners confuse these.

Think like this.

Journal

Smart database.

Syslog

Text files.

Journal

Fast searching.

Syslog

Easy manual reading.

Both are useful.

Many Linux systems use both together.

---

# Journal vs dmesg

dmesg

Shows only kernel ring buffer.

journalctl

Shows

Kernel

+

Services

+

Applications

+

Users

journalctl gives a much bigger picture.

---

# Easy Comparison

| Tool | Shows |
|-------|-------|
| dmesg | Kernel only |
| auth.log | Authentication |
| syslog | General system logs |
| journalctl | Almost everything collected by systemd |

---

# Real DFIR Example

Evidence

journal shows

backup.service started

↓

Process list

python running

↓

Network

Outbound connection

↓

auth.log

sudo systemctl enable backup.service

Now we can build a timeline.

Notice

One log alone is not enough.

Multiple logs together explain the incident.

---

# Investigation Flow

SOC Alert

↓

Open Journal

↓

Filter by

Service

↓

Filter by

Time

↓

Filter by

Priority

↓

Correlate with

auth.log

↓

Correlate with

Processes

↓

Correlate with

Network

↓

Build Timeline

---

# Interview Tips

✔ Journal is the logging system used by systemd.

✔ journalctl reads Journal logs.

✔ Journal stores logs in binary format.

✔ Binary logs are faster to search.

✔ Journal can be temporary or persistent.

✔ journalctl supports filtering by

- Service
- Time
- Priority
- Boot
- Kernel

✔ Journal is one of the most important tools during Linux incident response.

✔ Never investigate using only Journal.

Always correlate with

- auth.log
- audit.log
- syslog
- Processes
- Network connections

---

# Linux Auditd (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Understand how Auditd records security events.

---

# What is Auditd?

Imagine a school.

The Principal says

"I want to know every time someone enters the Principal's office."

So,

A security guard is placed outside the office.

Every time someone enters,

the guard writes

- Who entered
- When
- What they did

Linux Auditd works exactly like this.

Auditd watches important files and activities.

Whenever someone performs an action,

Auditd records it.

---

# Why Do We Need Auditd?

Normal logs answer

"What happened?"

Auditd answers

"Who did it?"

Example

A file was modified.

Normal log

File changed.

Auditd

- Who changed it?
- Which process changed it?
- When?
- Which user?
- Which program?

Auditd gives much deeper information.

---

# Think Like a SOC Analyst

Suppose

An attacker modifies

/etc/passwd

Without Auditd

You only know

The file changed.

With Auditd

You know

- User
- Process
- Program
- Time
- Current directory
- Command

This is why Auditd is extremely valuable.

---

# Auditd Components

Linux Audit System has four important parts.

---

## 1. Auditd

The service.

It collects audit events.

Think of it as

The security guard.

---

## 2. auditctl

Used to create rules.

Think of it as

Instructions given to the security guard.

Example

"Watch this file."

---

## 3. ausearch

Used to search audit logs.

Think of it as

Searching the guard's notebook.

---

## 4. aureport

Creates reports.

Think of it as

Summary of all security events.

---

# Easy Picture

Audit Rule

↓

Auditd watches

↓

Event happens

↓

Audit Log

↓

ausearch

↓

aureport

---

# Audit Rules

Auditd only watches

what you tell it to watch.

Example

Watch

/etc/passwd

Now,

every read,

write,

or modification

is recorded.

---

# Why Watch /etc/passwd?

Because attackers often

- Create users
- Modify users
- Change account information

This file is very important.

A SOC analyst should always monitor it.

---

# Another Example

Monitor every executed program.

Now

Whenever someone runs

python

bash

wget

curl

vim

Everything is recorded.

Very useful during investigations.

---

# Temporary vs Permanent Rules

Created using

auditctl

↓

Temporary

Disappear after reboot.

---

Created inside

/etc/audit/audit.rules

↓

Permanent

Remain after reboot.

---

# Easy Trick

auditctl

↓

Temporary

audit.rules

↓

Permanent

---

# Audit Log Location

Audit logs are stored here.

Location

/var/log/audit/audit.log

Think of it as

The security notebook.

---

# ausearch

Suppose

Audit log contains

1 million events.

You only need

Events related to

/etc/passwd

ausearch searches only those events.

Think of it as

Google Search for Audit Logs.

---

# Search by Key

When creating a rule,

we give it a name.

Example

users

Later

Search

users

Only those events appear.

Very useful during investigations.

---

# What Information Can Auditd Show?

Suppose

Someone edits

/etc/passwd

Auditd records

Time

↓

Who

↓

Program

↓

Process ID

↓

Working Directory

↓

File Name

↓

Success or Failure

↓

User ID

↓

Group ID

Everything needed for DFIR.

---

# Important Audit Fields

## PROCTITLE

Shows

The command executed.

Sometimes stored in Hex.

Can be decoded.

---

## SYSCALL

Shows

Which system call happened.

Very useful for investigators.

---

## PATH

Shows

Which file was accessed.

---

## CWD

Shows

Current Working Directory.

Very useful because

Attackers may execute the same file

from different locations.

---

# Example Investigation

Evidence

vim

↓

Modified

/var/www/html/tests.sh

SOC Thinking

Question

Which program changed the file?

Answer

vim

Question

Which file?

tests.sh

Question

When?

Check timestamp.

Question

Where?

Check Current Working Directory.

---

# Why Hex?

Sometimes

PROCTITLE

is stored in Hex.

Linux does this

because commands may contain

special characters.

Investigators simply decode it.

After decoding,

you see the real command.

---

# aureport

Reading thousands of logs

takes time.

aureport creates

a summary.

Think of it as

Audit Dashboard.

Example

Top modified files

Top executed commands

Top users

Very useful for managers.

---

# Real-Time Monitoring

Imagine

Someone modifies

/etc/shadow

Right now.

Auditd records it.

Now

Audit Dispatch Daemon

(audispd)

can immediately

send that event

to

Splunk

Elastic

SIEM

SOC Dashboard

The SOC analyst gets an alert

within seconds.

---

# Easy Picture

Attacker

↓

Changes File

↓

Auditd

↓

audispd

↓

SIEM

↓

SOC Alert

---

# Why SOC Analysts Love Auditd

Auditd provides

Very detailed evidence.

Examples

Who executed wget?

Who executed python?

Who changed passwd?

Who modified Apache?

Who executed bash?

Who deleted a file?

Auditd can answer all these questions.

---

# Investigation Flow

SOC Alert

↓

Open audit.log

↓

Search relevant rule

↓

Find user

↓

Find process

↓

Find command

↓

Find file

↓

Find timestamp

↓

Correlate with

auth.log

journalctl

Processes

Network

↓

Build Timeline

---

# Auditd vs auth.log

auth.log

Shows

Authentication.

Auditd

Shows

Detailed security activity.

Example

auth.log

User logged in.

Auditd

User logged in

↓

Executed sudo

↓

Ran python

↓

Modified passwd

↓

Created service

↓

Executed bash

Auditd provides much deeper visibility.

---

# Auditd vs Journal

Journal

General logs.

Auditd

Security-focused logs.

Journal

"What happened?"

Auditd

"Who did it?"

Both are important.

---

# Real SOC Example

Alert

Suspicious Python Process

Step 1

Check auth.log

Who logged in?

↓

Step 2

Check Journal

Did a service start?

↓

Step 3

Check Auditd

Who executed python?

↓

Step 4

Check Process

Still running?

↓

Step 5

Check Network

Is there a C2 connection?

↓

Build attack timeline.

---

# Common Mistakes

❌ Auditd logs everything automatically.

Correct

Auditd only records

what rules tell it to record.

---

❌ One Audit event proves malware.

Correct

Need multiple evidence sources.

---

❌ auth.log and Auditd are the same.

Correct

Auditd is much more detailed.

---

# Interview Tips

✔ Auditd is the Linux Auditing System.

✔ auditctl creates audit rules.

✔ ausearch searches audit logs.

✔ aureport creates summaries.

✔ audispd forwards audit events.

✔ Audit logs are stored in

/var/log/audit/audit.log

✔ Rules can be temporary or permanent.

✔ Auditd records

- User
- Process
- Command
- File
- Time
- Working Directory

✔ Auditd is one of the most valuable sources during Linux DFIR.

---

# Final SOC Mindset

Normal logs tell you

"What happened."

Auditd tells you

"Who did it, how they did it, and when they did it."

Always correlate Auditd with

- auth.log
- journalctl
- syslog
- Processes
- Network
- File system

Never investigate using only one source.

---

# Linux Auth Logs (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Learn how to investigate user authentication events.

---

# What are Auth Logs?

Imagine a school.

Every student enters through the main gate.

The security guard writes

- Who entered
- Who failed to enter
- Who used a special key
- What time they entered

Linux Auth Logs work exactly the same.

They record every authentication event.

---

# What is Authentication?

Authentication means

"Proving your identity."

Examples

- SSH login
- sudo
- su
- Login screen
- Password verification

Whenever Linux checks a user's identity,

an Auth Log is created.

---

# Why are Auth Logs Important?

Most attacks start with

someone trying to log in.

Examples

- SSH Brute Force
- Password Guessing
- Stolen Credentials
- Privilege Escalation

Auth Logs help us answer

- Who logged in?
- Was login successful?
- Which IP?
- Which user?
- When?
- Did someone use sudo?

---

# Where are Auth Logs Stored?

Location

/var/log/auth.log

Think of it as

The Security Register of Linux.

---

# What Information Does One Log Contain?

Every log usually contains

- Date
- Time
- Computer Name
- Service Name
- User
- Event Description

Example

Jun 19

↓

19:07

↓

sudo

↓

ubuntu

↓

Opened root session

This tells the complete story.

---

# Common Services Found

sshd

SSH login

sudo

Commands executed as root

su

Switch user

passwd

Password change

systemd-logind

User login sessions

---

# Easy Example

Suppose

Someone logs in using SSH.

Auth Log records

Time

↓

Username

↓

IP Address

↓

Success or Failure

Very useful during investigations.

---

# Why SOC Analysts Love Auth Logs

Suppose

A malware alert appears.

First question

Who logged in before the attack?

Auth Logs answer that.

---

# Reading Auth Logs

Auth Logs are normal text files.

You can search them easily.

Useful tools

- cat
- less
- tail
- grep
- awk

---

# Tail

Think of a CCTV screen.

You only want the newest events.

Tail shows

Recent authentication activity.

Useful during

Live Incident Response.

---

# Example Investigation

Alert

Someone became root.

SOC analyst

↓

Read latest auth logs.

↓

See

sudo session opened.

↓

Find

Which user became root.

---

# Log Rotation

Auth Logs cannot grow forever.

Imagine a notebook.

Once full,

you start a new notebook.

Linux does the same.

Old logs become

auth.log.1

Later

auth.log.2.gz

Then

auth.log.3.gz

and so on.

Newest logs stay inside

auth.log

Older logs move to archives.

---

# Why is Log Rotation Important?

Suppose

An attacker entered

three weeks ago.

Today's auth.log

may not contain those events.

You must also search

auth.log.1

auth.log.2.gz

etc.

Otherwise,

you may miss important evidence.

---

# Searching All Auth Logs

Instead of searching only

auth.log

search

auth.log*

Now Linux checks

Current Log

+

Old Logs

+

Compressed Logs

This is much better during investigations.

---

# Failed Login Investigation

Suppose

100 password attempts happen.

Auth Logs record

Failure

Failure

Failure

Failure

Failure

SOC Thinking

Possible

Brute Force Attack

---

# Successful Login Investigation

Now suddenly

One login succeeds.

Immediately ask

Was this expected?

Questions

Was it normal office hours?

Did the IP belong to the company?

Did this user usually log in?

If not,

investigate further.

---

# Session Opened

Sometimes

You only want users

who successfully entered Linux.

Search

Session Opened

Now you only see

Successful sessions.

Very useful.

---

# sudo Investigation

One of the most important investigations.

Suppose

User

ubuntu

runs

vim /etc/hosts

using sudo.

Auth Log records

User

↓

Working Directory

↓

Target User

↓

Exact Command

SOC now knows

exactly what happened.

---

# Example

User

ubuntu

↓

Used sudo

↓

Opened root

↓

Executed

vim /etc/hosts

Now we know

who changed the system.

---

# Why sudo Logs Matter

Attackers almost always need

higher privileges.

Common actions

- Install malware
- Create users
- Disable security
- Modify services
- Change cron jobs

Most of these require

sudo.

---

# Time-Based Investigation

Suppose

SOC receives an alert.

Alert Time

3:30 PM

No need to read

one month of logs.

Only investigate

around 3:30 PM.

Much faster.

---

# Absolute Time

Suppose

Incident happened

4 June

3:30 PM

Search only

that time period.

Very useful for

Timeline Analysis.

---

# Relative Time

Sometimes

SOC only wants

recent activity.

Example

Last 2 hours

Now Linux shows

only recent authentication events.

Useful during

Live Incident Response.

---

# Investigator Workflow

Alert

↓

Open auth.log

↓

Look for

Failed Logins

↓

Successful Logins

↓

sudo Usage

↓

User Creation

↓

Password Changes

↓

Privilege Escalation

↓

Build Timeline

---

# Common Attacker Activities Found

SSH Brute Force

Repeated failures

↓

Credential Theft

Successful login

↓

Privilege Escalation

sudo

↓

Persistence

New user

↓

Password Change

passwd

↓

Privilege Assignment

usermod

Everything leaves traces.

---

# Correlation

Never trust only one log.

Always compare

Auth Log

+

Journal

+

Auditd

+

Processes

+

Network Connections

One log tells

part of the story.

All logs together

tell the full attack.

---

# Easy Comparison

| Evidence | Where to Look |
|-----------|---------------|
| SSH Login | auth.log |
| Failed Password | auth.log |
| sudo | auth.log |
| User Creation | auth.log |
| Password Change | auth.log |
| Service Started | journalctl |
| File Modified | auditd |

---

# Interview Tips

✔ Auth Logs record authentication events.

✔ Location

/var/log/auth.log

✔ Records

- SSH
- sudo
- su
- Password changes
- Login sessions

✔ Old logs are stored as

auth.log.1

auth.log.2.gz

✔ grep filters logs.

✔ awk performs advanced filtering.

✔ tail shows recent events.

✔ Always investigate

Failed Login

↓

Successful Login

↓

sudo

↓

Privilege Escalation

↓

Persistence

---

# SOC Mindset

Never ask

"Did someone log in?"

Ask

Who logged in?

From where?

When?

Was it successful?

Did they become root?

What command did they execute next?

That is how a SOC analyst thinks.

---

# Linux Apache Logs (SOC Notes)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Learn how to investigate attacks using Apache Logs.

---

# What are Application Logs?

Until now we studied

- Kernel Logs
- Auth Logs
- Journal
- Auditd

Now we study

Application Logs.

Application logs record

"What happened inside one application."

Example

Apache

↓

Stores web requests.

MySQL

↓

Stores database queries.

Docker

↓

Stores container activity.

Every application has its own logs.

---

# Why are Application Logs Important?

Think about a shopping mall.

Security Guard

knows

who entered the mall.

But

A shop owner knows

who entered his shop.

Apache is like the shop owner.

It records

every visitor coming to the website.

---

# Apache Web Server

Apache is software that serves websites.

Browser

↓

Sends Request

↓

Apache receives request

↓

Apache returns webpage

Every request is recorded.

---

# Apache Creates Two Logs

1.

Access Log

Records every request.

2.

Error Log

Records every error.

Think like this.

Access Log

"What happened?"

Error Log

"What went wrong?"

---

# Where are Logs Stored?

Directory

/var/log/apache2/

Important files

access.log

error.log

---

# Access Log

Access Log records

every request reaching the web server.

Even if the request fails,

it is usually recorded.

---

# Think Like This

Attacker

↓

Opens Website

↓

Apache receives request

↓

Writes Access Log

Everything starts here.

---

# Information Stored

Access Log records

- Client IP
- Date
- Time
- HTTP Method
- Requested File
- HTTP Version
- Status Code
- Browser (User-Agent)

Almost everything needed for investigation.

---

# Easy Example

One log may look like

Client IP

↓

10.10.24.106

Request

↓

GET /

Status

↓

200

Browser

↓

Firefox

This means

User from IP

10.10.24.106

opened the homepage successfully.

---

# Understanding Every Field

Imagine

10.10.24.106

↓

GET

↓

/index.php

↓

200

↓

Firefox

Now understand each part.

---

## Client IP

Who visited?

Very important.

SOC asks

Which IP attacked us?

---

## Date & Time

When did it happen?

Needed for timeline.

---

## HTTP Method

What action was requested?

Examples

GET

Read a webpage.

POST

Send data.

PUT

Upload data.

DELETE

Delete something.

---

# GET vs POST

GET

Normally used

to view pages.

Example

Open homepage.

POST

Normally used

to submit data.

Example

Login forms

File upload

Password submission

---

# SOC Tip

Most users

mostly perform

GET requests.

Many attacks

use POST requests.

Because attackers send data.

---

# Requested URL

Example

/index.php

/login.php

/upload.php

/admin.php

This tells us

which page the attacker tried to access.

---

# HTTP Status Code

One of the most important fields.

---

## 200

Success.

Request worked.

---

## 301

Page moved.

Redirect.

Usually normal.

---

## 302

Temporary redirect.

Usually normal.

---

## 403

Forbidden.

Permission denied.

Interesting during attacks.

---

## 404

File not found.

Very important.

Suppose attacker tries

shell.php

and gets

404

This means

the file does not exist.

Many repeated

404 requests

can indicate

directory brute forcing.

---

## 500

Internal Server Error.

Application crashed.

May indicate

server problem

or exploit attempt.

---

# User-Agent

Shows

which browser sent the request.

Example

Firefox

Chrome

curl

wget

Python Requests

PowerShell

SOC analysts love User-Agent.

---

# Why?

Imagine

Normal users

↓

Chrome

Firefox

Edge

Attacker

↓

curl

python

wget

Custom Script

Immediately suspicious.

---

# Error Log

Error Log records

application errors.

Example

PHP Error

Permission Error

Configuration Error

Module Crash

Connection Failure

Everything goes here.

---

# Difference

Access Log

Every request.

Error Log

Only errors.

---

# Example

PHP cannot connect

to another machine.

Apache writes

Connection Failed

inside Error Log.

SOC now knows

something unusual happened.

---

# Why Error Logs Matter?

Suppose

Attacker uploads

reverse shell.

Reverse shell fails.

Error Log records

Connection Failed.

That tells us

someone attempted

Command and Control.

---

# Investigation Workflow

Alert

↓

Open Access Log

↓

Find suspicious IP

↓

Check requested URLs

↓

Check response codes

↓

Open Error Log

↓

Look for failures

↓

Correlate with

Auth Logs

Journal

Auditd

---

# Filtering by IP

Suppose

SOC alert says

10.10.24.106

is malicious.

Filter only

that IP.

Now

all activity

from that attacker

appears together.

Very useful.

---

# Filtering by Status Code

Suppose

You only want

404 errors.

Now you can see

all failed requests.

Useful for

Scanning Detection

Directory Bruteforce

Missing Files

Web Shell Guessing

---

# Counting Requests

Suppose

One IP

visited

5000 times.

Another IP

visited

3 times.

Which one looks suspicious?

Obviously

5000.

Counting requests

helps detect

scanners

bots

bruteforce attacks.

---

# Counting Status Codes

Suppose

Server returns

1000

404 errors.

Question

Why?

Maybe

Attacker

is searching

hidden files.

---

# Real Attack Example

Attacker

↓

GET

/cmd.php

↓

200

Interesting.

Next

↓

GET

/cmd.php?ip=10.x.x.x

↓

200

Very suspicious.

Why?

Normal users

never pass

IP

and

Port

inside URL.

This may indicate

a reverse shell.

---

# Reverse Shell Clue

Suppose URL

contains

cmd.php

↓

ip=

↓

port=

SOC Thinking

Maybe

attacker uploaded

a web shell

which creates

a reverse connection.

Immediately investigate.

---

# Correlation

Apache tells

How attacker entered.

Auth Log tells

Who logged in.

Auditd tells

What attacker modified.

Journal tells

Which service started.

Together

they build

the attack timeline.

---

# Apache Investigation Flow

Access Log

↓

Find attacker IP

↓

Find first request

↓

Find exploited page

↓

Check HTTP code

↓

Open Error Log

↓

Look for failures

↓

Check Auth Logs

↓

Check Auditd

↓

Check Journal

↓

Build Timeline

---

# Easy Comparison

| Log | Answers |
|------|----------|
| Access Log | Who visited the website? |
| Error Log | What failed inside Apache? |
| Auth Log | Who logged into Linux? |
| Auditd | What files changed? |
| Journal | Which services started? |

---

# Interview Tips

✔ Apache stores logs inside

/var/log/apache2/

✔ Important logs

access.log

error.log

✔ Access Log records

- Client IP
- Time
- Method
- URL
- Status Code
- Browser

✔ Error Log records

Application errors.

✔ Important HTTP Codes

200 → Success

403 → Forbidden

404 → Not Found

500 → Internal Error

✔ Always investigate

IP

↓

URL

↓

Status Code

↓

User-Agent

↓

Timeline

---

# SOC Mindset

Never ask

"Did someone visit the website?"

Ask

Who?

When?

From which IP?

Which page?

Which HTTP method?

Did it succeed?

Did the request look normal?

That is how a SOC analyst investigates web attacks.

---

# Linux DFIR Case Study (Anna Investigation)

> Level: Beginner
> Perspective: SOC Analyst / DFIR
> Goal: Learn how to investigate a compromised Linux web server.

---

# Incident

Company

Deer Inc.

One Linux server

↓

Connected to Internet

↓

Running Apache Web Server

↓

May be compromised.

Question

Was the server hacked?

If yes,

How?

---

# Rule Number One

Never start randomly.

Many beginners immediately check

Processes

or

Running services.

Wrong.

Always ask

"How did the attacker enter?"

First find

Initial Access.

Everything starts there.

---

# Step 1

Find Initial Access

Question

How can attackers reach this server?

Think.

Server is connected to Internet.

Apache is running.

Therefore,

Most likely attack surface

↓

Web Server.

So the first log we investigate is

Apache Access Log.

---

# Why Access Log First?

Imagine

A thief enters a shopping mall.

The first CCTV camera

is at the entrance.

Apache Access Log

is that entrance camera.

---

# Step 2

Read Apache Access Log

We notice

Many requests.

Most are normal.

Suddenly,

we see

POST requests.

Question

Why is POST interesting?

Because POST sends data.

Attackers often use POST

to

- Upload web shells
- Exploit forms
- Send payloads

Not every POST is malicious,

but every suspicious POST deserves investigation.

---

# Step 3

Notice the HTTP Status Code

POST

↓

404

Question

Did the attack succeed?

No.

404 means

Requested file

does not exist.

The attacker tried,

but this request failed.

---

# Important Lesson

Never stop here.

Many beginners think

404

↓

Attack Failed

↓

Investigation Finished.

Wrong.

Attackers rarely stop after one attempt.

Continue reading the logs.

---

# Step 4

Continue Reading

Later,

Apache logs show

cmd.php

↓

ip=

↓

port=

Question

Does a normal website work like this?

No.

Very suspicious.

Why?

Normal users

do not open

cmd.php?ip=10.x.x.x&port=5000

This strongly suggests

a web shell

or

reverse shell.

---

# SOC Thinking

Evidence

cmd.php

↓

IP parameter

↓

Port parameter

↓

HTTP 200

Question

What does 200 mean?

Success.

The request worked.

Now

our confidence increases

that the attacker gained code execution.

---

# Step 5

Now Change Focus

Initial Access

is confirmed.

Next question

Did the attacker change files?

How do we answer that?

Use

Auditd.

---

# Step 6

Auditd Investigation

Anna already created

an Audit Rule

to monitor

/var/www/html

Excellent idea.

Why?

Because

that directory contains

the website.

If attackers upload

web shells,

backdoors,

PHP files,

everything happens there.

---

# Auditd Answers

Auditd tells us

- Which file changed
- Which process changed it
- Which user changed it
- When it happened

This is much stronger evidence

than only looking at Apache logs.

---

# Step 7

Privilege Escalation

Auditd shows

a script

was executed

using sudo.

Question

Why is this suspicious?

Because

Attackers usually

need root privileges

to continue attacking.

Possible goals

- Create users
- Install malware
- Create services
- Disable security

Now we suspect

Privilege Escalation.

---

# Important Lesson

Access

≠

Root.

Getting inside

is only

the first step.

Attackers usually

want Administrator access.

---

# Step 8

Persistence

Question

What happens

if the attacker loses access?

They need

Persistence.

Anna investigates

system services.

Good choice.

Why?

Services start

automatically.

Perfect persistence method.

---

# Step 9

Journal Investigation

Anna opens

Journal logs

for

tests.service

Now we see

Service Started

↓

Script Executed

↓

Runs as Root

Huge red flag.

---

# Why?

Normal services

usually

start

normal applications.

This one

starts

a custom script.

Very suspicious.

---

# Step 10

Follow the Script

Never investigate

only the service.

Always investigate

what the service executes.

Question

What file does the service run?

Read

the service file.

Then

open

that script.

This is where

malicious code often hides.

---

# Step 11

New User Created

Now

Anna checks

Auth Logs.

Question

Why Auth Logs?

Because

creating users

requires authentication.

Auth Logs record

user creation

password changes

sudo activity

group changes

Exactly what we need.

---

# Evidence Found

Auth Log shows

useradd

↓

passwd

↓

usermod

↓

Added to sudo group.

Question

What does this tell us?

The attacker

created

a new Administrator account.

This is persistence.

Even if

the original exploit

is removed,

the attacker

can simply log in

using the new account.

---

# Step 12

Was the New User Used?

Question

Creating a user

does not prove

the attacker logged in.

Need more evidence.

Anna now searches

Session Opened.

If

the new account

opened a session,

the attacker

actually used it.

Very important distinction.

---

# Timeline

Now

combine

all evidence.

Apache

↓

Initial Access

↓

Auditd

↓

Website Modified

↓

sudo

↓

Privilege Escalation

↓

Journal

↓

Service Created

↓

Auth Logs

↓

New User Created

↓

Session Opened

↓

Persistence Confirmed

Now we know

the complete attack story.

---

# Why Correlation Matters

Imagine

only reading

Apache logs.

You only know

someone attacked.

Now read

Auditd.

You know

files changed.

Now read

Auth Logs.

You know

a user was created.

Now read

Journal.

You know

a malicious service exists.

One log

shows one chapter.

All logs together

tell the complete story.

---

# MITRE ATT&CK Mapping

Initial Access

↓

Web Exploit

Execution

↓

Script executed

Privilege Escalation

↓

sudo

Persistence

↓

Service

Persistence

↓

New User

Credential Access

↓

Password Change

Command and Control

↓

Reverse Shell

---

# Final Incident Response

SOC receives alert

↓

Isolate server

↓

Preserve evidence

↓

Collect logs

↓

Investigate Apache

↓

Investigate Auditd

↓

Investigate Auth Logs

↓

Investigate Journal

↓

Build Timeline

↓

Identify Persistence

↓

Remove attacker

↓

Reset credentials

↓

Reimage system

↓

Write Incident Report

---

# Common Beginner Mistakes

❌ Kill the process immediately.

Correct

Collect evidence first.

---

❌ Delete the web shell immediately.

Correct

Preserve forensic evidence first.

---

❌ Trust one log.

Correct

Always correlate multiple logs.

---

❌ Stop after finding Initial Access.

Correct

Always continue until

Persistence

is found.

---

# Investigation Mindset

SOC analysts never ask

"Was the server hacked?"

They ask

How?

When?

From where?

Which vulnerability?

Which file?

Which process?

Which user?

Did they become root?

Did they create persistence?

Did they leave?

Could they return?

Only after answering all of these,

the investigation is complete.

---

# Final Rule

Remember this order.

1.

Apache Logs

↓

Find Initial Access

2.

Auditd

↓

Find File Changes

3.

Auth Logs

↓

Find Authentication Activity

4.

Journal

↓

Find Services

5.

Processes

↓

Find Running Malware

6.

Network

↓

Find C2 Connection

7.

Timeline

↓

Tell the Complete Story

This is exactly how a Linux SOC Analyst thinks.
