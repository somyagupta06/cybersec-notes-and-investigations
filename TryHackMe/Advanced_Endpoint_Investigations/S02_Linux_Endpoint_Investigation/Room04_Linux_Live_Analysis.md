# Linux Live Forensics — SOC Analyst Notes

## 1. What is Live Forensics?

Live forensics means investigating a computer **while it is still running**.

In normal disk forensics, we may shut down the machine and then examine the disk.

But in live forensics, we keep the machine running because some important evidence exists only while the machine is running.

### Simple Example

Imagine an attacker has compromised a Linux server.

Right now:

- a malicious process is running
- a connection to the attacker's server is active
- a malicious file is open
- an attacker may still be logged in
- a fileless malware may be present only in memory

If we suddenly shut down the machine, some of this evidence may disappear.

Therefore:

> Live forensics focuses mainly on collecting volatile and currently active evidence before it disappears.

---

# 2. Why is Volatile Data Important?

Volatile data is data that can disappear when the system is:

- shut down
- rebooted
- powered off
- sometimes even when a process terminates

The most important example is **RAM**.

RAM contains information about what is happening RIGHT NOW.

For example:

```text
RAM

├── Running processes
├── Active network connections
├── Logged-in users
├── Process memory
├── Temporary information
├── Encryption keys
├── Some passwords/secrets
└── Fileless malware

```
