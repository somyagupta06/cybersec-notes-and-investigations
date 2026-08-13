# Osquery 

## 1. What is Osquery?

Osquery is a tool that lets us ask questions about a computer using SQL.

Think of Osquery like this:

Computer = a big house
Osquery = an investigator
SQL query = the question asked by the investigator

For example:

"Show me all running processes."

Osquery can give:

PID       Process
1234      chrome.exe
4567      powershell.exe
7890      svchost.exe


Instead of using many different Windows/Linux commands, we can use SQL queries.

Examples:

SELECT * FROM processes;

SELECT * FROM users;

SELECT * FROM programs;


So remember:

Osquery = SQL + Operating System information


--------------------------------------------------
## 2. Why is Osquery useful for SOC?
--------------------------------------------------

A SOC Analyst investigates computers.

During an investigation, the analyst may want to know:

- Which users exist?
- Which processes are running?
- Which programs are installed?
- Which services are running?
- Which files exist?
- Which network connections are active?
- Which startup programs exist?

Osquery provides many tables for this information.


For example:

users table       -> information about users
processes table   -> running processes
programs table    -> installed programs
services table    -> services
file table        -> file information


This makes Osquery very useful for:

- Threat Hunting
- Incident Response
- Endpoint Investigation
- DFIR
- SOC investigations


--------------------------------------------------
## 3. Starting Osquery
--------------------------------------------------

To start the interactive Osquery shell:

osqueryi

After starting it, you will see:

osquery>

Now we can enter commands and SQL queries.


--------------------------------------------------
## 4. What does "Interactive Mode" mean?
--------------------------------------------------

Interactive mode means:

We type a command.
Osquery gives the result immediately.

Example:

osquery> SELECT * FROM users;


It is similar to opening Python and typing commands one by one.

Python:

>>>

Osquery:

osquery>


--------------------------------------------------
## 5. What is a Virtual Database?
--------------------------------------------------

When Osquery starts, it says:

"You are connected to a transient 'in-memory' virtual database."

Do not get scared by this sentence.

It simply means:

Osquery is NOT a normal database like MySQL.

Instead, Osquery creates tables that represent information from the operating system.

Example:

OS has running processes.

Osquery represents them as:

processes table


OS has users.

Osquery represents them as:

users table


OS has installed software.

Osquery represents them as:

programs table


So:

Operating System
       |
       v
    Osquery
       |
       v
Virtual SQL Tables


Important:

These tables are mainly used to READ information from the endpoint.


--------------------------------------------------
## 6. SQL vs Osquery Meta-Commands
--------------------------------------------------

There are two types of commands we use in Osquery.

### SQL commands

Example:

SELECT * FROM users;


### Meta-commands

Example:

.tables

.schema users

.help


Meta-commands usually start with:

.


Very important:

.tables

is NOT SQL.

.schema

is NOT SQL.

.help

is NOT SQL.


They are commands for controlling or exploring the Osquery shell.


--------------------------------------------------
## 7. .help
--------------------------------------------------

The .help command shows the commands available in Osquery.

Use:

.help


Some important commands are:

.tables
.schema
.mode
.exit
.quit
.show


Do not try to memorize every command.

For SOC work, remember these first:

.help
.tables
.schema
.mode
.exit


--------------------------------------------------
## 8. .tables
--------------------------------------------------

.tables shows the tables available in Osquery.

Example:

.tables


You may see tables like:

users
processes
programs
services
scheduled_tasks
startup_items
etc.


Think of tables like different drawers.

Drawer 1:

users

Drawer 2:

processes

Drawer 3:

programs

Drawer 4:

services


Each drawer contains a different type of information.


--------------------------------------------------
## 9. .tables user
--------------------------------------------------

We can also search for tables containing a particular word.

Example:

.tables user


This may show:

user_groups
user_ssh_keys
userassist
users


This is useful when we know what we are investigating.

Example:

If the investigation is about users:

.tables user


If the investigation is about processes:

.tables process


If the investigation is about network information:

.tables network


This helps us quickly find useful tables.


--------------------------------------------------
## 10. What is a Schema?
--------------------------------------------------

A table name only tells us WHAT the table is about.

It does not tell us WHAT information is inside it.

For that, we check the schema.


Use:

.schema users


The schema tells us:

- Column names
- Data types
- Sometimes extra information about the columns


For example, the users table may contain:

uid
gid
username
description
directory
shell
uuid
type


Think of schema like the labels on boxes.

Box:

USERS

Inside it:

username
uid
gid
directory
shell


Now we know what information we can ask for.


--------------------------------------------------
## 11. Important users columns
--------------------------------------------------

### uid

UID means User ID.

It is a number used to identify a user.


Example:

James -> UID 1002


### gid

GID means Group ID.

It tells us the group associated with the user.


### username

The name of the user.

Example:

James
Administrator
Guest


### directory

The user's home directory.

Example:

C:\Users\James


### shell

The program/shell used by the user.

Example:

C:\Windows\system32\cmd.exe


### description

A description of the account.


--------------------------------------------------
## 12. SELECT
--------------------------------------------------

SELECT means:

"Give me this information."


Basic syntax:

SELECT column1, column2 FROM table;


Example:

SELECT username FROM users;


Meaning:

"Show me usernames from the users table."


Example:

SELECT username, uid FROM users;


Meaning:

"Show me the username and UID of every user."


--------------------------------------------------
## 13. SELECT *
--------------------------------------------------

The * means:

"Give me everything."


Example:

SELECT * FROM users;


Meaning:

"Show me all columns and all rows from the users table."


Think:

* = everything


If we only need specific information, it is better to ask for specific columns.


Example:

SELECT username, uid, directory FROM users;


This is cleaner than:

SELECT * FROM users;


SOC tip:

Do not ask for everything when you only need 2-3 things.


--------------------------------------------------
## 14. FROM
--------------------------------------------------

FROM tells Osquery:

"Which table should I look at?"


Example:

SELECT username FROM users;


Here:

SELECT username
= What do I want?

FROM users
= Where should I get it from?


Easy way to remember:

SELECT = What?

FROM = Where?


--------------------------------------------------
## 15. LIMIT
--------------------------------------------------

LIMIT controls how many rows we want to see.


Example:

SELECT * FROM programs LIMIT 1;


Meaning:

"Show me only 1 result."


Example:

SELECT * FROM processes LIMIT 10;


Meaning:

"Show me only 10 processes."


Why is this useful?

Some tables can contain hundreds or thousands of rows.

Instead of showing everything, we can first test our query with:

LIMIT 5

or

LIMIT 10


--------------------------------------------------
## 16. COUNT()
--------------------------------------------------

COUNT tells us:

"How many records are there?"


Example:

SELECT COUNT(*) FROM programs;


Suppose the result is:

160


That means:

There are 160 program entries in the table.


Another example:

SELECT COUNT(*) FROM users;


If the result is:

7


There are 7 user entries.


SOC use:

COUNT can help us quickly understand the endpoint.

For example:

How many users?

How many programs?

How many processes?


--------------------------------------------------
## 17. WHERE
--------------------------------------------------

WHERE means:

"I don't want everything.
Give me only what matches my condition."


Example:

SELECT * FROM users WHERE username='James';


Meaning:

"From the users table, show me only the user whose username is James."


Think:

WHERE = filter


Example:

All users:

Administrator
Guest
James
SYSTEM


WHERE username='James'


Result:

James


--------------------------------------------------
## 18. Why WHERE is important for SOC
--------------------------------------------------

SOC analysts usually investigate something specific.

For example:

"Is there a user named hacker?"


Instead of checking hundreds of users manually:

SELECT * FROM users WHERE username='hacker';


Or:

"Is powershell.exe running?"


SELECT * FROM processes WHERE name='powershell.exe';


Or:

"Find programs related to Chrome."


SELECT * FROM programs WHERE name LIKE '%Chrome%';


WHERE makes investigation faster.


--------------------------------------------------
## 19. Comparison Operators
--------------------------------------------------

WHERE can use different operators.


= 

Means equal.

Example:

WHERE username='James'


<> 

Means not equal.

Example:

WHERE username<>'James'


>

Greater than.


<

Less than.


>=

Greater than or equal to.


<=

Less than or equal to.


BETWEEN

Means between two values.


Example:

WHERE uid BETWEEN 1000 AND 2000


Meaning:

Find users whose UID is between 1000 and 2000.


--------------------------------------------------
## 20. LIKE
--------------------------------------------------

LIKE is used when we do not know the exact value.

Example:

WHERE username LIKE 'James%'


Here:

% means any number of characters.


So it can match:

James
James1
James123
James_Admin


Another example:

WHERE name LIKE '%PowerShell%'


This can find names containing:

PowerShell


LIKE is very useful during threat hunting.


--------------------------------------------------
## 21. Wildcards
--------------------------------------------------

The % symbol is a wildcard.

It means:

"Any number of characters."


Example:

'Power%'


Can match:

PowerShell
Power
Power123


Example:

'%Power%'


Can match:

PowerShell
WindowsPower
MyPowerTool


The _ symbol means:

"One character."


Example:

'A_m'


Can match:

Arm
Aim
A7m


--------------------------------------------------
## 22. File Table
--------------------------------------------------

The file table is slightly different.

If we run:

SELECT * FROM file;


Osquery may give an error.

Why?

Because the file table needs a specific WHERE condition.

Why?

Imagine asking:

"Show me every file on this computer."

There could be:

100,000 files
500,000 files
1,000,000 files


That would be expensive and slow.

So Osquery says:

"Tell me which file/path you want to check."


Example:

SELECT * FROM file WHERE path='C:\Windows\System32\cmd.exe';


Now Osquery knows exactly what to check.


SOC example:

Suppose an alert says:

Suspicious file found:

C:\Users\Public\malware.exe


We can check:

SELECT * FROM file WHERE path='C:\Users\Public\malware.exe';


This is much better than asking Osquery to scan every file.


--------------------------------------------------
## 23. JOIN
--------------------------------------------------

JOIN is one of the most useful SQL features for SOC investigations.


Sometimes one table has information that another table has.


Example:


users table:

UID     Username

1002    James
1003    John


processes table:

PID     Name          UID

5000    chrome.exe    1002
6000    powershell    1003


The processes table tells us:

powershell is running with UID 1003


But it does not directly tell us the username.


The users table tells us:

UID 1003 = John


So we JOIN the tables.


Result:

PID     Process       Username

6000    powershell    John


Now we know:

John is running PowerShell.


--------------------------------------------------
## 24. JOIN using UID
--------------------------------------------------

Both tables contain:

uid


users:

uid
username


processes:

uid
pid
name
path


Because both tables have UID, we can connect them.


Example:

SELECT p.pid, p.name, p.path, u.username
FROM processes p
JOIN users u
ON u.uid=p.uid;


Here:

p = processes

u = users


ON u.uid=p.uid

means:

"Connect the process with the user having the same UID."


--------------------------------------------------
## 25. Why JOIN is powerful for SOC
--------------------------------------------------

Imagine you find:

powershell.exe


You know:

Process name = powershell.exe

But you also want to know:

Who ran it?


A JOIN can answer this.


Example:

SELECT p.pid, p.name, p.path, u.username
FROM processes p
JOIN users u
ON u.uid=p.uid
WHERE p.name='powershell.exe';


Now the SOC analyst can see:

- PID
- Process name
- Process path
- Username


This gives much more context.


--------------------------------------------------
# 26. SOC Investigation Example
--------------------------------------------------

Imagine a SOC alert says:

"Suspicious PowerShell execution detected."


The analyst can investigate step by step.


### Step 1: Check whether PowerShell is running

SELECT pid, name, path, cmdline
FROM processes
WHERE name='powershell.exe';


Now we know:

Which PowerShell?
Which PID?
Where is it running from?
What command did it run?


### Step 2: Find the user

SELECT p.pid, p.name, p.path, u.username
FROM processes p
JOIN users u
ON p.uid=u.uid
WHERE p.name='powershell.exe';


Now we know who is associated with that process.


### Step 3: Check the user

SELECT username, directory, shell
FROM users
WHERE username='James';


Now we understand the account.


### Step 4: Check installed programs

SELECT name, version, publisher
FROM programs
LIMIT 20;


Now we can look for suspicious software.


--------------------------------------------------
# 27. Attacker Point of View
--------------------------------------------------

An attacker may try to:

- Create a new user
- Run PowerShell
- Run a malicious process
- Install malicious software
- Create persistence
- Hide malicious files
- Use a stolen account


Osquery can help the SOC analyst investigate many of these things.


For example:

Attacker creates a new account:

hacker


SOC can query:

SELECT username, directory, type
FROM users
WHERE username='hacker';


Attacker runs PowerShell:

SOC can query:

SELECT pid, name, path, cmdline
FROM processes
WHERE name='powershell.exe';


Attacker places a suspicious file:

SOC can query the file table with the exact path.


So Osquery helps us ask:

"What is happening on this endpoint right now?"


--------------------------------------------------
# 28. Very Important SOC Mindset
--------------------------------------------------

Do not just run random queries.

First ask:

"What am I investigating?"


Example:

Alert:

PowerShell detected.


Question 1:

Is PowerShell running?


Query:

SELECT pid, name, path, cmdline
FROM processes
WHERE name='powershell.exe';


Question 2:

Who is running it?


Use JOIN with users.


Question 3:

What command did it execute?


Look at:

cmdline


Question 4:

Where is PowerShell located?


Look at:

path


Question 5:

Is the user suspicious?


Check:

users


This is how a SOC analyst thinks.


--------------------------------------------------
# 29. Quick Revision
--------------------------------------------------

### Osquery

SQL-based endpoint investigation tool.


### osqueryi

Starts the interactive Osquery shell.


### .help

Shows Osquery shell commands.


### .tables

Shows available tables.


### .tables user

Shows tables containing "user".


### .schema users

Shows the structure of the users table.


### SELECT

Tells Osquery what information we want.


### FROM

Tells Osquery which table to use.


### *

Means all columns.


### LIMIT

Limits the number of results.


### COUNT()

Counts records.


### WHERE

Filters results.


### LIKE

Searches using patterns.


### %

Matches multiple characters.


### _

Matches one character.


### JOIN

Combines information from two tables.


### UID

Connects a process with its user.


--------------------------------------------------
# 30. One Simple Picture to Remember Everything
--------------------------------------------------

Think of Osquery as a detective's database.

              OS
              |
              v
           Osquery
              |
      -------------------
      |        |        |
      v        v        v
    users   processes  programs
      |        |        |
      |        |        |
      -------- JOIN -----
              |
              v
       Useful investigation


Example:

Alert
  |
  v
powershell.exe
  |
  v
processes table
  |
  v
PID + path + cmdline + UID
  |
  v
JOIN with users
  |
  v
Username
  |
  v
SOC investigation


--------------------------------------------------
# 31. Most Important Things to Remember
--------------------------------------------------

1. Osquery lets us query OS information using SQL.

2. Tables represent different types of endpoint information.

3. Use .tables to find tables.

4. Use .schema to understand a table.

5. SELECT chooses the information.

6. FROM chooses the table.

7. WHERE filters the result.

8. LIMIT reduces the number of results.

9. COUNT tells us how many records exist.

10. LIKE helps us search patterns.

11. Some tables, such as file, require a WHERE condition.

12. JOIN connects related information from different tables.

13. In SOC, JOIN is very useful for connecting processes with users.

14. The goal is not just to collect data.

15. The goal is to use the data to answer an investigation question.
