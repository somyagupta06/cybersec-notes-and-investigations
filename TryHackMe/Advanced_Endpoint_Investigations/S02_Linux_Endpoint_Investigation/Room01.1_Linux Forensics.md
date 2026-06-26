# Linux User and System Enumeration (SOC Notes)

## Why do we collect this information?

When a Linux system is suspected to be compromised, the first job of a SOC analyst is to understand the system.

Questions to answer:

* Which Linux version is running?
* Who can log in?
* Who has administrator privileges?
* When did users log in?
* Were there any failed login attempts?

These artifacts help build the attack timeline.

---

# 1. Linux Distribution

A Linux distribution (distro) is a version of Linux.

Common distributions:

* Ubuntu
* Debian
* CentOS
* Red Hat
* Arch Linux
* Linux Mint
* OpenSUSE

### Why is this important?

Different distributions use different tools and configurations.

Example:

Ubuntu uses `apt`

CentOS uses `yum`

A SOC analyst should know the operating system before starting an investigation.

---

# 2. OS Release Information

File:

`/etc/os-release`

Command:

`cat /etc/os-release`

Example Output

* Ubuntu
* Version 20.04
* Codename: Focal Fossa

### SOC View

Check:

* Operating System
* Version
* Support status

### Why?

Older operating systems may contain known security vulnerabilities.

---

# 3. User Accounts

File:

`/etc/passwd`

Command:

`cat /etc/passwd`

Each line represents one user.

Example

`ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash`

## Important Fields

| Field          | Meaning                                                |
| -------------- | ------------------------------------------------------ |
| Username       | User name                                              |
| Password       | Usually `x` (real password is stored in `/etc/shadow`) |
| UID            | User ID                                                |
| GID            | Group ID                                               |
| Home Directory | User files location                                    |
| Shell          | Default command shell                                  |

---

## UID

| UID   | Meaning         |
| ----- | --------------- |
| 0     | Root user       |
| 1-999 | System accounts |
| 1000+ | Normal users    |

### SOC Checks

Look for:

* Unknown users
* New accounts
* Multiple UID 0 users
* Strange home directories
* Suspicious login shells

---

# 4. Group Information

File:

`/etc/group`

Command:

`cat /etc/group`

Groups control permissions.

Example

Group:

`sudo`

Members:

`ubuntu`

### SOC Checks

Look for users added to:

* sudo
* adm
* docker

Unexpected group membership may indicate privilege escalation.

---

# 5. Sudoers File

File:

`/etc/sudoers`

Command:

`sudo cat /etc/sudoers`

This file decides who can become root.

Example

`%sudo ALL=(ALL:ALL) ALL`

Meaning:

Every member of the sudo group can run commands as root.

### SOC Checks

Look for:

* Unknown users
* NOPASSWD entries
* Custom sudo rules

---

# 6. Login History

Files

Successful logins

`/var/log/wtmp`

Failed logins

`/var/log/btmp`

Command

`last -f /var/log/wtmp`

`last -f /var/log/btmp`

These files are binary files.

### SOC Checks

* Who logged in?
* Login time
* Logout time
* Reboot history
* Failed login attempts

Many failed logins may indicate a brute-force attack.

---

# 7. Authentication Log

File

`/var/log/auth.log`

Command

`cat /var/log/auth.log`

This is one of the most important forensic files.

It records:

* SSH logins
* sudo usage
* su usage
* Authentication failures
* Authentication success
* Root sessions

Example

`COMMAND=/usr/bin/cat /etc/sudoers`

Meaning

The user used sudo to read the sudoers file.

---

# SOC Investigation Checklist

| Artifact            | Purpose                        |
| ------------------- | ------------------------------ |
| `/etc/os-release`   | Identify Linux version         |
| `/etc/passwd`       | List all users                 |
| `/etc/group`        | Check user groups              |
| `/etc/sudoers`      | Find administrator permissions |
| `/var/log/wtmp`     | Successful logins              |
| `/var/log/btmp`     | Failed logins                  |
| `/var/log/auth.log` | Authentication activity        |

---

# Red Flags 🚩

* Unknown user account
* User with UID 0 (except root)
* User added to sudo group
* Many failed login attempts
* Login at unusual time
* Login from unexpected location
* Unknown sudo commands
* Changes to the sudoers file

---

# Quick Revision

| File                | Purpose                      |
| ------------------- | ---------------------------- |
| `/etc/os-release`   | Operating system information |
| `/etc/passwd`       | User accounts                |
| `/etc/group`        | User groups                  |
| `/etc/sudoers`      | Sudo permissions             |
| `/var/log/wtmp`     | Successful login history     |
| `/var/log/btmp`     | Failed login history         |
| `/var/log/auth.log` | Authentication events        |

---

# Remember

A SOC analyst does **not** only look for malware.

A SOC analyst first answers these questions:

* What system am I investigating?
* Who can access this system?
* Who has administrator privileges?
* Who logged in?
* Did anyone try to break in?
* Did anyone use sudo?

These answers help build the attack timeline.


---

# Linux System Configuration and Persistence (SOC Notes)

## Why do we collect this information?

After identifying the users, a SOC analyst must understand:

* Which machine is this?
* How is it connected to the network?
* What programs are running?
* Can malware survive after a reboot?

This helps identify suspicious activity and persistence.

---

# 1. Hostname

File

`/etc/hostname`

Command

`cat /etc/hostname`

Example

`tryhackme`

## What is a hostname?

A hostname is the computer's name.

Example

| Device          | Hostname |
| --------------- | -------- |
| Web Server      | web01    |
| Database Server | db01     |
| User Laptop     | john-pc  |

## SOC Checks

* Is the hostname expected?
* Does it match the system's role?
* Is this the correct machine for the investigation?

---

# 2. Timezone

File

`/etc/timezone`

Command

`cat /etc/timezone`

Example

`Etc/UTC`

## Why is it important?

Every log uses timestamps.

If the timezone is wrong, the attack timeline will also be wrong.

### SOC Checks

* System timezone
* Log timestamps
* Correct event timeline

---

# 3. Network Configuration

File

`/etc/network/interfaces`

Command

`cat /etc/network/interfaces`

This file shows how the network is configured.

Example

`iface eth0 inet dhcp`

Meaning

The IP address is assigned automatically using DHCP.

### SOC Checks

* DHCP or Static IP
* Network interface names
* Unexpected configuration changes

---

# 4. IP and MAC Address

Command

`ip address show`

This command shows:

* IP Address
* MAC Address
* Network Interface
* Interface Status

## Important Terms

| Item        | Meaning                           |
| ----------- | --------------------------------- |
| IP Address  | Device address on the network     |
| MAC Address | Physical hardware address         |
| Interface   | Network adapter (eth0, lo, wlan0) |

### SOC Checks

* Expected IP address
* Unexpected network interfaces
* Unknown MAC address
* VPN or tunnel interfaces

---

# 5. Active Network Connections

Command

`netstat -natp`

Shows all active network connections.

## Connection States

| State       | Meaning                          |
| ----------- | -------------------------------- |
| LISTEN      | Waiting for incoming connections |
| ESTABLISHED | Active communication             |

Example

Port 22 → SSH

Port 80 → Web Server

Port 443 → HTTPS

### SOC Checks

Look for:

* Unknown remote IP addresses
* Unexpected listening ports
* Reverse shell connections
* Suspicious external communication

---

# 6. Running Processes

Command

`ps aux`

Shows all running programs.

Important Columns

| Column  | Meaning       |
| ------- | ------------- |
| USER    | Process owner |
| PID     | Process ID    |
| CPU     | CPU usage     |
| MEM     | Memory usage  |
| COMMAND | Program name  |

### SOC Checks

* Unknown processes
* Malware running as root
* High CPU usage
* Suspicious scripts
* Reverse shells

---

# 7. Hosts File

File

`/etc/hosts`

Command

`cat /etc/hosts`

The hosts file maps a hostname to an IP address.

Example

`127.0.0.1 localhost`

### SOC Checks

Look for fake entries.

Example

`google.com → 10.10.10.10`

This may redirect users to a malicious server.

---

# 8. DNS Configuration

File

`/etc/resolv.conf`

Command

`cat /etc/resolv.conf`

This file shows which DNS server the system uses.

Example

`nameserver 127.0.0.53`

### SOC Checks

* Unexpected DNS server
* Unknown search domains
* DNS hijacking

---

# 9. Persistence

Persistence means:

**The malware starts again after the computer restarts.**

Attackers use persistence so they never lose access.

---

# 10. Cron Jobs

File

`/etc/crontab`

Command

`cat /etc/crontab`

Cron automatically runs commands at scheduled times.

It is similar to Windows Task Scheduler.

Example

A backup runs every day at 6:00 AM.

### SOC Checks

Look for:

* Unknown scheduled tasks
* Suspicious scripts
* Malware running every few minutes

---

# 11. Startup Services

Directory

`/etc/init.d`

Command

`ls /etc/init.d`

Services start automatically during system boot.

Examples

* SSH
* Apache
* Cron
* OpenVPN

### SOC Checks

* Unknown services
* Malware disguised as a service
* Newly added startup services

---

# 12. Bash Startup File

File

`~/.bashrc`

Command

`cat ~/.bashrc`

This file runs automatically whenever a Bash shell starts.

Normally it contains:

* Aliases
* Environment variables
* Prompt settings

### SOC Checks

Look for:

* Suspicious commands
* Download scripts
* Reverse shell commands
* Hidden aliases

---

# 13. System-wide Startup Files

Files

`/etc/bash.bashrc`

`/etc/profile`

These files affect **all users** on the system.

### SOC Checks

* Malicious startup commands
* Modified PATH variable
* Unauthorized changes

---

# SOC Investigation Checklist

| Artifact                  | Purpose                            |
| ------------------------- | ---------------------------------- |
| `/etc/hostname`           | Identify the machine               |
| `/etc/timezone`           | Build the correct timeline         |
| `/etc/network/interfaces` | Check network configuration        |
| `ip address show`         | View IP and MAC addresses          |
| `netstat -natp`           | Check active network connections   |
| `ps aux`                  | View running processes             |
| `/etc/hosts`              | Detect local DNS changes           |
| `/etc/resolv.conf`        | Check DNS servers                  |
| `/etc/crontab`            | Find scheduled tasks               |
| `/etc/init.d`             | Find startup services              |
| `~/.bashrc`               | Check user startup commands        |
| `/etc/bash.bashrc`        | Check system-wide startup settings |
| `/etc/profile`            | Check login startup settings       |

---

# Red Flags 🚩

* Unknown hostname
* Wrong timezone
* Unexpected IP address
* Unknown listening port
* Connection to an unknown external IP
* Suspicious running process
* Modified hosts file
* Unknown DNS server
* Suspicious cron job
* Unknown startup service
* Malicious command in `.bashrc`
* Unauthorized changes in `/etc/profile`

---

# Quick Revision

| File / Command            | Purpose                   |
| ------------------------- | ------------------------- |
| `/etc/hostname`           | Computer name             |
| `/etc/timezone`           | Timezone                  |
| `/etc/network/interfaces` | Network configuration     |
| `ip address show`         | IP and MAC information    |
| `netstat -natp`           | Active connections        |
| `ps aux`                  | Running processes         |
| `/etc/hosts`              | Local hostname mapping    |
| `/etc/resolv.conf`        | DNS server configuration  |
| `/etc/crontab`            | Scheduled tasks           |
| `/etc/init.d`             | Startup services          |
| `~/.bashrc`               | User startup commands     |
| `/etc/bash.bashrc`        | System-wide Bash settings |
| `/etc/profile`            | Login startup settings    |

---

# Remember

A SOC analyst should answer these questions:

* Which machine am I investigating?
* What is its network configuration?
* Who is it communicating with?
* Which programs are running?
* Is there any persistence that will survive a reboot?

---

# Linux Execution Evidence and Log Analysis (SOC Notes)

## Why is this important?

One of the first questions during an investigation is:

**"What did the attacker execute?"**

Linux stores execution evidence in different artifacts. A SOC analyst collects these artifacts to rebuild the attack timeline.

---

# 1. Sudo Execution History

File

`/var/log/auth.log`

Command

`cat /var/log/auth.log* | grep -i COMMAND`

This log records commands executed using **sudo**.

Example

`COMMAND=/usr/bin/cat /etc/sudoers`

Meaning

The user used **sudo** to read the sudoers file.

### Information You Can Find

* Username
* Executed command
* Working directory
* Time of execution

### SOC Checks

Look for:

* User creation
* Password changes
* Permission changes
* Unknown sudo commands
* Privilege escalation

---

# 2. Bash History

File

`~/.bash_history`

Command

`cat ~/.bash_history`

This file stores commands executed **without sudo**.

Each user has a separate history file.

Examples

* cd
* ls
* unzip
* rm
* mkdir
* mv

### SOC Checks

Look for:

* Downloaded files
* Deleted files
* Extracted archives
* Executed scripts
* Suspicious tools

Always check:

* User history
* Root history

---

# Difference

| Artifact      | Stores                      |
| ------------- | --------------------------- |
| auth.log      | Commands executed with sudo |
| .bash_history | Normal shell commands       |

---

# 3. Vim History

File

`~/.viminfo`

Command

`cat ~/.viminfo`

Vim saves information about opened files.

It may contain:

* Opened files
* Search history
* Command history
* Cursor position

### SOC Checks

Look for sensitive files such as:

* `/etc/passwd`
* `/etc/shadow`
* `/etc/sudoers`
* `.ssh/authorized_keys`

This helps identify which files the attacker viewed or modified.

---

# 4. Syslog

File

`/var/log/syslog`

Command

`cat /var/log/syslog`

Syslog records general system activity.

Examples

* Services
* Cron jobs
* Kernel messages
* DNS events
* System startup
* System shutdown

### SOC Checks

Look for:

* Service failures
* Cron execution
* System errors
* DNS problems
* Unexpected system activity

---

## Log Rotation

Linux automatically rotates old logs.

Example

| File        | Meaning            |
| ----------- | ------------------ |
| syslog      | Current log        |
| syslog.1    | Older log          |
| syslog.2.gz | Compressed old log |

Using

`/var/log/syslog*`

searches all rotated logs.

---

# 5. Authentication Log

File

`/var/log/auth.log`

This is one of the most important forensic artifacts.

It records:

* SSH login
* Login failure
* Login success
* sudo usage
* su usage
* pkexec usage
* User creation
* Group changes

Example

`new user: ubuntu`

Meaning

A new user account was created.

### SOC Checks

Look for:

* New users
* Added sudo privileges
* Failed logins
* Successful logins
* Suspicious authentication attempts

---

# 6. Third-Party Logs

Many applications keep their own logs inside:

`/var/log`

Examples

| Application | Log Location                    |
| ----------- | ------------------------------- |
| Apache      | `/var/log/apache2`              |
| Samba       | `/var/log/samba`                |
| OpenVPN     | `/var/log/openvpn`              |
| MySQL       | `/var/log/mysql` (if installed) |

---

# Apache Logs

Directory

`/var/log/apache2`

Important Files

| File                    | Purpose                    |
| ----------------------- | -------------------------- |
| access.log              | Client requests            |
| error.log               | Server errors              |
| other_vhosts_access.log | Requests for virtual hosts |

### Access Log

Records:

* Client IP
* Request time
* Requested page
* HTTP status code

Useful for detecting:

* Web attacks
* Web shell access
* Directory scanning
* SQL Injection attempts

---

### Error Log

Records:

* PHP errors
* Server crashes
* Permission errors
* Module failures

Useful for finding failed attacks or application problems.

---

# SOC Investigation Flow

```
Alert
   │
   ▼
auth.log
   │
   ▼
sudo commands
   │
   ▼
.bash_history
   │
   ▼
.viminfo
   │
   ▼
syslog
   │
   ▼
Application logs
   │
   ▼
Attack Timeline
```

---

# SOC Investigation Checklist

| Artifact                      | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `/var/log/auth.log`           | Authentication events and sudo commands |
| `~/.bash_history`             | User command history                    |
| `~/.viminfo`                  | Files opened in Vim                     |
| `/var/log/syslog`             | System activity                         |
| `/var/log/apache2/access.log` | Web requests                            |
| `/var/log/apache2/error.log`  | Web server errors                       |
| `/var/log`                    | Third-party application logs            |

---

# Red Flags 🚩

* Unknown sudo commands
* New user account
* User added to sudo group
* History showing malware download
* Deleted files after execution
* Sensitive files opened in Vim
* Suspicious cron activity in syslog
* Unknown external IP in web logs
* Large number of failed login attempts
* Unexpected application errors

---

# Quick Revision

| Artifact         | What It Shows                    |
| ---------------- | -------------------------------- |
| auth.log         | Login activity and sudo commands |
| .bash_history    | User commands                    |
| .viminfo         | Files opened in Vim              |
| syslog           | General system activity          |
| Apache Logs      | Website traffic                  |
| Third-party Logs | Application-specific events      |

---

# Remember

To understand an attack, answer these questions:

* Who logged in?
* Which commands were executed?
* Which files were opened?
* What happened on the system?
* Which application was attacked?

Combining these artifacts helps a SOC analyst build the complete attack timeline.
