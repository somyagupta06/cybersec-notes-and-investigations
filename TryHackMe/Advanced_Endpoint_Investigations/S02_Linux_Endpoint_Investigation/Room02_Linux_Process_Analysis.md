# Linux Processes and Cronjobs

## Why Should a SOC Analyst Learn This?

Attackers rarely leave malware sitting on the disk.

Instead, they make it **run**, **repeat**, and **stay alive**.

To understand how an attacker works, we must understand:

- Processes
- Parent-child relationships
- Cronjobs

---

# What is a Process?

A process is simply a **running program**.

Example:

Firefox installed on the system is a program.

When you open Firefox, Linux creates a process.

Every running program has its own Process ID (PID).

Example:

Firefox
↓
Running
↓
PID = 2540

---

# Process ID (PID)

PID means Process ID.

It is a unique number given to every running process.

Example:

PID 101 -> bash

PID 205 -> python

PID 330 -> sshd

The operating system uses the PID to manage running programs.

---

# Parent and Child Process

One process can start another process.

Example:

cron
↓

backup.sh
↓

bash
↓

python

Here,

cron is the parent.

backup.sh is the child.

bash is the child of backup.sh.

python is the child of bash.

This is called a **process tree**.

---

# Why Parent-Child Relationships Matter?

SOC analysts do not only check **what is running**.

They also check **who started it**.

Example:

Normal

systemd
↓

sshd
↓

bash

This is expected.

Example:

Apache
↓

bash

This is suspicious.

A web server normally serves web pages.

It should not start a shell.

Possible reasons:

- Command Injection
- Web Shell
- Remote Code Execution (RCE)

---

# Process Investigation Workflow

When you find a suspicious process, ask these questions:

- What is the process name?
- What is its PID?
- Who started it?
- Which user owns it?
- What command was executed?
- Is it connected to the network?
- Is it normal for this system?

Never trust only the process name.

Always verify.

---

# Useful Process Commands

ps

Shows running processes.

Useful to quickly identify suspicious programs.

---

ps -u username

Shows processes belonging to one user.

Useful when investigating a suspicious account.

---

ps -eFH

Shows:

- All processes
- Parent-child relationships
- Full command line

This is one of the most useful commands during live response.

---

lsof

Shows files and network connections opened by a process.

Useful to answer:

"What is this process using?"

Example:

- Open files
- Network sockets
- Named pipes
- Deleted files

---

pstree

Shows the process family tree.

Useful to answer:

"Where did this process come from?"

---

top

Shows live running processes.

Useful to monitor:

- CPU usage
- Memory usage
- New processes appearing

---

# Example Investigation

You find:

cron
↓

backup.sh
↓

cat /tmp/f

sh -i

nc -l 4444

This is suspicious.

Why?

Because:

Netcat is listening.

A shell is running.

A named pipe exists.

This combination is commonly used for a bind shell.

---

# Named Pipe (FIFO)

A FIFO is not a normal file.

It is a communication channel between processes.

Example:

Process A writes commands.

↓

FIFO

↓

Process B reads commands.

Attackers often use FIFO files in bind shell one-liners.

How to identify one?

Run:

ls -l /tmp/f

If permissions start with:

p

It means the file is a FIFO (named pipe).

---

# Netcat Listener

Example:

nc -l 0.0.0.0 4444

Meaning:

- Listen on port 4444
- Accept incoming connections
- Wait for someone to connect

Possible hypothesis:

- Bind shell
- Backdoor
- Unauthorized listener

Always verify before concluding.

---

# Process Investigation Checklist

When a suspicious process is found:

✔ Check parent process

✔ Check full command

✔ Check open files

✔ Check network connections

✔ Check running user

✔ Check related script

✔ Check persistence

---

# What is a Cronjob?

A cronjob is a scheduled task.

Linux runs it automatically.

Example:

Every day

↓

Run backup

Every hour

↓

Clean logs

Every 5 minutes

↓

Run monitoring script

---

# Cron Syntax

Minute

Hour

Day of Month

Month

Day of Week

Command

Example:

10 05 * * * backup.sh

Meaning:

Run backup.sh every day at 5:10 AM.

---

# Important Cron Locations

System Cron

/etc/crontab

Runs system-wide scheduled tasks.

Can run commands as root.

---

Additional Cron Directories

/etc/cron.hourly

Runs every hour.

---

/etc/cron.daily

Runs every day.

---

/etc/cron.weekly

Runs every week.

---

/etc/cron.monthly

Runs every month.

---

/etc/cron.d

Stores additional cron configurations.

---

User Cronjobs

/var/spool/cron/crontabs/

Each user has their own cron file.

Example:

bob

janice

ubuntu

---

# Why Attackers Love Cronjobs

Cron provides persistence.

Example:

Every 5 minutes

↓

Download malware

↓

Execute malware

↓

Sleep

↓

Repeat forever

Even if the malware process is killed,

Cron starts it again.

---

# Example

*/5 * * * * root /var/tmp/backup

This is suspicious.

Why?

The script runs as root.

The script is stored inside /var/tmp.

The /var/tmp directory is writable.

An attacker could replace the script.

Root would execute it.

Possible privilege escalation.

---

# Cron Investigation Workflow

When you investigate cron:

Step 1

Read the cron entry.

↓

Step 2

Find the executed script.

↓

Step 3

Read the script.

↓

Step 4

Check for:

- curl
- wget
- bash
- nc
- python
- reverse shells

↓

Step 5

Check cron execution logs.

↓

Step 6

Look for persistence.

---

# Cron Logs

Cron activity is recorded in logs.

Common locations:

Debian

/var/log/syslog

RHEL

/var/log/cron

Useful information:

- Job execution
- Failed jobs
- Modified crontabs
- Execution time

---

# Pspy

Pspy monitors processes in real time.

Best feature:

It does not require root.

Useful for:

- Catching short-lived malware
- Detecting cron execution
- Watching new processes appear

If malware starts and exits quickly,

ps may miss it.

Pspy can capture it.

---

# SOC Investigation Flow

Suspicious Alert

↓

Check running processes

↓

Identify parent-child relationship

↓

Check open files

↓

Check network activity

↓

Check cronjobs

↓

Read executed scripts

↓

Check logs

↓

Identify persistence

↓

Build attack timeline

---

# Remember

Do not say:

"This is malware."

Say:

"This may be malware. I will verify it."

SOC analysts work with evidence.

Never with assumptions.  

---
# Topic 02 — Linux Services (SOC Notes)

## Why Should a SOC Analyst Learn Services?

A service is one of the most common ways attackers maintain persistence.

If malware starts automatically after every reboot,
the attacker does not need to attack the machine again.

This is why SOC analysts always investigate services during live incident response.

---

# What is a Service?

A service is a program that runs in the background.

It works continuously without the user opening it.

Examples:

- SSH Service
- Apache Web Server
- Cron Service
- Database Service

Example:

You restart your Linux machine.

↓

SSH automatically starts.

↓

Now users can connect remotely.

Nobody manually opened SSH.

The service started itself.

---

# Service vs Process

| Process | Service |
|----------|----------|
| A running program | A background program that usually starts automatically |
| Can start and stop anytime | Usually starts during system boot |
| May exist only for a short time | Usually runs continuously |

Example

Python script

↓

Runs

↓

Finishes

This is a process.

SSH

↓

Starts during boot

↓

Keeps running

This is a service.

---

# Why Do Attackers Love Services?

Services automatically start every time the system boots.

If an attacker creates a malicious service,

System Boot

↓

Malicious Service Starts

↓

Malware Starts

↓

Attacker gets persistence.

The attacker does not need to log in again.

---

# What is systemd?

systemd is the service manager.

Think of it as the "manager" of all services.

It decides:

- Which service should start
- Which service should stop
- Which service failed
- Which service should restart

Almost every modern Linux distribution uses systemd.

---

# What is systemctl?

systemctl is the tool used to communicate with systemd.

A SOC analyst uses it to investigate services.

Common actions:

Start a service

systemctl start service

Stop a service

systemctl stop service

Restart a service

systemctl restart service

Enable service during boot

systemctl enable service

Disable automatic startup

systemctl disable service

View service status

systemctl status service

---

# First Step During Investigation

List all running services.

Look for services that look unusual.

Example

apache.service

cron.service

sshd.service

These are usually normal.

But if you find

b4ckd00rftw.service

This deserves investigation.

Never assume it is malware.

Investigate first.

---

# Service Investigation Workflow

Step 1

Find the suspicious service.

↓

Step 2

Read its status.

↓

Step 3

Find the executable.

↓

Step 4

Read the executable.

↓

Step 5

Read the unit file.

↓

Step 6

Check service logs.

↓

Step 7

Determine persistence.

---

# Understanding systemctl status

Example

systemctl status b4ckd00rftw.service

This command tells us:

- Is the service running?
- When did it start?
- Which process is running?
- Which script is executed?
- Child processes

This is one of the most useful commands during investigations.

---

# Important Fields

## Active

Example

Active: running

Means

The service is currently running.

---

## Main PID

Example

Main PID: 596

This is the main process of the service.

You can investigate this PID further using process analysis.

---

## CGroup

Shows all child processes created by the service.

Example

Service

↓

bash

↓

sleep

This tells us exactly what the service is doing.

---

# Investigating the Executable

Suppose the service runs

/usr/local/bin/b4ckd00rftw.sh

Never stop at the service.

Always investigate the executable.

Read it.

Understand it.

Example

while true

↓

Create new user

↓

Add user to sudo group

↓

Sleep 60 seconds

↓

Repeat forever

This clearly shows persistence.

---

# Attacker's Goal

Imagine this timeline.

Attacker creates user

↓

SOC deletes user

↓

Service waits 60 seconds

↓

Creates user again

The attacker never loses access.

This is persistence.

---

# Why Live Cleanup Can Fail

Many beginners think

Delete the malicious user

↓

Problem solved.

Wrong.

If the service is still running,

it recreates the user.

Always remove the persistence mechanism first.

---

# Service Unit Files

Every service has a configuration file.

This file tells Linux how to run the service.

Usually found inside

/etc/systemd/system/

Think of the unit file as the instruction manual.

Example

Service Name

↓

Which script to run

↓

When to start

↓

Restart policy

↓

Dependencies

---

# Important Fields Inside Unit Files

## Description

Simple description of the service.

---

## ExecStart

Most important field.

It tells Linux which file to execute.

Example

ExecStart=/usr/local/bin/script.sh

Now you know exactly which file to investigate.

---

## Restart

Example

Restart=always

Very suspicious if the service is malicious.

Even if the process crashes,

Linux starts it again.

Attackers love this option.

---

# Service Logs

Every service generates logs.

Logs help us answer questions like

- What happened?
- When did it happen?
- Which command ran?
- Which user was affected?

---

# journalctl

journalctl reads logs stored by systemd.

Very useful during investigations.

Example

journalctl -u service

Shows logs of one service.

Example

journalctl -f -u service

Shows live logs as they appear.

---

# Example Investigation

Suppose logs show

useradd

↓

usermod

↓

Added user to sudo group

Now compare this with the script.

The script says

Create user

↓

Add to sudo

The logs confirm it actually happened.

Evidence matches.

Now your confidence is much higher.

---

# SOC Investigation Checklist

When a suspicious service is found

✔ Check service name

✔ Check current status

✔ Check Main PID

✔ Check child processes

✔ Find executable

✔ Read executable

✔ Read unit file

✔ Check Restart option

✔ Check service logs

✔ Look for persistence

---

# Normal vs Suspicious

| Normal | Suspicious |
|---------|------------|
| apache.service | random123.service |
| sshd.service | unknown.service |
| cron.service | service running from /tmp |
| Service starts expected program | Service starts unknown script |
| No unexpected user creation | Creates admin users repeatedly |

---

# Attacker Perspective

The attacker wants the malware to survive reboot.

Creating a malicious service is one of the easiest ways to achieve persistence.

The service automatically starts every time Linux boots.

Even if the attacker disconnects,

the malware keeps running.

---

# Investigator Perspective

Never investigate only the service.

Always investigate:

Service

↓

Executable

↓

Unit File

↓

Logs

↓

Processes

↓

Persistence

Only after collecting evidence should you conclude that the service is malicious.

---

# Remember

A suspicious service is only an indicator.

Evidence comes from:

- Executable
- Unit file
- Logs
- Running processes

SOC analysts never guess.

They verify.

---
# Topic 03 — Linux Autostart Persistence (SOC Notes)

## Why Should a SOC Analyst Learn Autostart?

Attackers do not always use cronjobs or services.

Sometimes they want malware to run only when a user logs in.

For this, they use **Autostart**.

Autostart is another common persistence technique.

---

# What is Autostart?

Autostart means:

"Run this program automatically."

The program starts without the user opening it.

Example

User logs in

↓

Browser opens automatically

↓

Music player starts automatically

↓

Custom script runs automatically

This is Autostart.

---

# Difference Between Services, Cronjobs and Autostart

| Services | Cronjobs | Autostart |
|----------|----------|-----------|
| Start during system boot | Run at scheduled time | Run when a user logs in |
| Usually run continuously | Run only when schedule matches | Run once after login |
| Good for persistence | Good for persistence | Good for user-targeted persistence |

---

# Why Attackers Use Autostart

Suppose an attacker wants to steal passwords.

The attacker creates an autostart entry.

Now every time the victim logs in,

Malicious script starts automatically.

The victim does not notice anything.

The attacker gets persistence.

---

# Types of Autostart

There are two types.

## 1. System Autostart

Runs during system boot.

Before users log in.

Usually used for system services.

---

## 2. User Autostart

Runs after a user logs in.

Only affects that user.

This is commonly abused by attackers.

---

# System Autostart Locations

Some common locations are

/etc/init.d/

/etc/systemd/system/

These locations normally contain legitimate services.

But attackers may also place malicious startup scripts here.

Always investigate unknown entries.

---

# User Autostart Location

The most common location is

~/.config/autostart/

Every user can have their own autostart folder.

Example

/home/janice/.config/autostart/

---

# What is a .desktop File?

Autostart usually uses **.desktop** files.

Think of it as a small instruction file.

It tells Linux

"What program should I start after login?"

---

# Example

The file says

Exec

↓

Run setup.sh

Now,

Every time the user logs in,

Linux automatically runs setup.sh.

---

# Important Fields

## Name

Just the name shown to the user.

Example

Setup Development Environment

This is not important for investigation.

Attackers can write any name.

---

## Exec

Most important field.

This tells Linux exactly which command will run.

Always investigate this field.

Example

Exec

↓

bash

↓

python

↓

curl

↓

unknown script

This is where attackers usually hide malicious commands.

---

# Investigation Workflow

Step 1

Find all autostart entries.

↓

Step 2

Read every .desktop file.

↓

Step 3

Look at the Exec field.

↓

Step 4

Investigate the executed script.

↓

Step 5

Check whether it is legitimate.

---

# Example Attack

Suppose you find

keygrabber.desktop

You open it.

Exec says

Send

/home/janice/.ssh/id_rsa

to an external server.

This is highly suspicious.

---

# Why is id_rsa Important?

id_rsa is the user's private SSH key.

Only the owner should have it.

If an attacker steals it,

they may log in as that user.

Private keys should never leave the machine.

---

# Attack Timeline

Attacker compromises machine

↓

Creates autostart file

↓

Victim logs in

↓

Autostart executes

↓

Private SSH key is stolen

↓

Attacker uses stolen key later

Persistence + Credential Theft

---

# Other Important User Artefacts

Autostart is not the only thing to check.

Always investigate these locations too.

---

## .bash_history

Contains commands typed by the user.

Useful for answering

"What commands were executed?"

Example

vim authorized_keys

↓

cat password.txt

↓

curl malware.sh

This helps build the attack timeline.

---

## .ssh Directory

One of the most important directories.

Contains SSH-related files.

Important files include

id_rsa

Private key

Never share this.

---

id_rsa.pub

Public key

Safe to distribute.

---

authorized_keys

Contains public keys allowed to log in.

If the attacker adds their own public key,

they can log in without using a password.

Very common persistence technique.

---

known_hosts

Stores systems previously connected through SSH.

Useful during investigations.

---

# .profile

Runs when a user logs in.

Normally it sets environment variables.

Attackers may add malicious commands here.

Always inspect it.

---

# MOTD (Message of the Day)

Normally,

Linux displays a welcome message after SSH login.

Example

Welcome to Ubuntu

Today's updates...

Attackers may abuse MOTD.

Instead of showing a message,

they execute a malicious script.

This creates another persistence method.

---

# Normal vs Suspicious

| Normal | Suspicious |
|---------|------------|
| Opens browser | Downloads malware |
| Opens IDE | Runs unknown shell script |
| Starts calculator | Sends SSH keys to internet |
| Opens terminal | Downloads payload from attacker server |

---

# SOC Investigation Checklist

When investigating Autostart

✔ Find all .desktop files

✔ Read every Exec command

✔ Investigate executed scripts

✔ Check for curl or wget

✔ Check for SSH key theft

✔ Check .bash_history

✔ Check .ssh directory

✔ Check authorized_keys

✔ Check .profile

✔ Check MOTD

---

# Attacker Perspective

The attacker wants malware to start automatically.

The victim only needs to log in.

The malware starts without any action.

This provides persistence.

---

# Investigator Perspective

Do not stop after finding an autostart file.

Always continue.

Autostart

↓

Executed script

↓

Downloaded files

↓

Network connections

↓

SSH keys

↓

Logs

↓

Timeline

---

# Remember

Autostart itself is not malware.

It is simply a way to automatically run programs.

What matters is **what the autostart executes.**

Always investigate the command inside the **Exec** field before making conclusions.

---
# Topic 04 — Linux Application Artefacts (SOC Notes)

## Why Should a SOC Analyst Learn Application Artefacts?

Attackers do not only leave malware.

They also leave traces inside applications.

These traces help us answer questions like:

- Which websites were visited?
- Which files were downloaded?
- Which commands were executed?
- Which editor was used?
- Which browser was used?
- What happened before the attack?

Application artefacts help us build the attack timeline.

---

# What are Application Artefacts?

Application artefacts are files created by applications while they are running.

Examples:

- Browser history
- Browser cookies
- Download history
- Editor history
- Configuration files
- Cache files
- Log files

Think of them as footprints left behind by applications.

---

# Investigation Goal

Do not only ask

"Is malware present?"

Also ask

"What did the attacker do?"

Application artefacts help answer this question.

---

# Step 1 — Identify Installed Applications

First understand what applications exist on the system.

Example

Browser

↓

Text Editor

↓

Database

↓

Mail Client

↓

Web Server

Different applications create different artefacts.

---

# dpkg

dpkg lists software installed using the Linux package manager.

Useful for answering

"What software is officially installed?"

Remember

It only shows packages installed by the package manager.

If the attacker manually copied malware,

dpkg will not show it.

Never depend only on dpkg.

---

# Vim Artefacts

Many Linux users use Vim.

Vim saves information inside

.viminfo

This file is very useful during investigations.

---

# What does .viminfo contain?

Examples

- Search history
- Command history
- Recently opened files
- Editor information

Example

Suppose the attacker edits

authorized_keys

using Vim.

Even if the attacker closes Vim,

.viminfo may still contain evidence.

---

# Why is .viminfo Useful?

Imagine this timeline.

Attacker

↓

Opens authorized_keys

↓

Adds SSH public key

↓

Saves file

↓

Deletes shell history

Even if shell history is deleted,

.viminfo may still reveal that Vim was used.

This helps investigators.

---

# Other Editor Artefacts

Nano

↓

.nano_history

Emacs

↓

.emacs

↓

.emacs.d

Every editor leaves different artefacts.

---

# Browser Artefacts

Browsers store a lot of useful information.

Examples

- Browsing history
- Download history
- Cookies
- Search history
- Saved sessions
- Bookmarks

This information is extremely useful during DFIR.

---

# Why Browser Artefacts Matter

Suppose malware was downloaded.

Browser history may show

Visited website

↓

Downloaded malware

↓

Execution time

This helps build the timeline.

---

# Firefox Profiles

Firefox stores user data inside

.mozilla/firefox

Inside this folder,

one or more profiles exist.

Each profile stores user activity.

---

# Browser Profiles

A browser profile contains

- History
- Cookies
- Downloads
- Bookmarks
- Preferences

Each user has their own profile.

Always investigate the correct profile.

---

# Legacy vs Active Profile

Sometimes multiple profiles exist.

Example

default

default-release

Usually,

default-release is the active profile.

Always verify before analysis.

---

# Browser Investigation Workflow

Find browser directory

↓

Find user profile

↓

Read browser artefacts

↓

Extract useful evidence

↓

Build timeline

---

# What are Cookies?

Cookies are small files stored by websites.

They remember information about users.

Examples

- Login sessions
- Website preferences
- Shopping carts

---

# Why Cookies Matter?

Suppose an attacker steals cookies.

The attacker may log into a website

without knowing the password.

This is called Session Hijacking.

Cookies are valuable evidence.

---

# Browser History

Browser history tells us

- Which websites were visited
- Visit time
- Search activity

Useful questions

Did the user visit phishing websites?

Did the attacker access a C2 server?

Was malware downloaded?

---

# Download History

Download history shows

- Downloaded files
- Download source
- Download time

This helps identify malware downloads.

---

# Bookmarks

Bookmarks usually are not malicious.

But they may reveal

- Frequently used websites
- Internal company portals
- Interesting attacker behaviour

---

# Dumpzilla

Dumpzilla is a browser forensic tool.

It automatically extracts browser artefacts.

Instead of manually opening database files,

Dumpzilla collects evidence for us.

---

# What Can Dumpzilla Extract?

Examples

- Cookies
- History
- Downloads
- Bookmarks
- Search history
- Extensions

This saves a lot of investigation time.

---

# Example Investigation

Suppose Dumpzilla shows

History

↓

malware-download.com

↓

Downloaded

payload.zip

↓

Cookies

↓

Attacker C2 domain

Now we have evidence.

We can correlate it with

- Process logs
- Network logs
- Timeline

---

# Browser Timeline

Example

10:00

Visited phishing website

↓

10:01

Downloaded payload

↓

10:02

Executed payload

↓

10:03

Reverse shell started

Now the attack becomes much easier to understand.

---

# Normal vs Suspicious

| Normal | Suspicious |
|---------|------------|
| Google Search | Unknown malware website |
| University Portal | C2 Server |
| GitHub | Credential harvesting page |
| Microsoft Update | Fake software download |

---

# Other Useful Application Artefacts

Different systems require different investigations.

Examples

Mail Server

- Mail logs
- Attachments
- Email database

---

Web Server

- Access logs
- Error logs
- Configuration files

---

Database Server

- Query logs
- Authentication logs
- Database configuration

---

Word Processing Software

- Recently opened documents
- Temporary files

---

Terminal Multiplexers

Examples

Screen

Tmux

May contain running sessions or command history.

---

# SOC Investigation Checklist

✔ Identify installed applications

✔ Find user artefacts

✔ Check editor history

✔ Check browser history

✔ Check downloads

✔ Check cookies

✔ Check bookmarks

✔ Check browser profiles

✔ Correlate with logs

✔ Build attack timeline

---

# Attacker Perspective

Attackers try to remove evidence.

But many applications automatically save history.

Even if malware is deleted,

application artefacts may still reveal

- Websites visited
- Commands used
- Files opened
- Credentials stolen

---

# Investigator Perspective

Application artefacts are not proof by themselves.

Always correlate them with

Processes

↓

Logs

↓

Network Connections

↓

Persistence

↓

Timeline

Only then make conclusions.

---

# Remember

Application artefacts answer one important question:

"What happened on this system?"

They help investigators reconstruct the entire attack step by step.
