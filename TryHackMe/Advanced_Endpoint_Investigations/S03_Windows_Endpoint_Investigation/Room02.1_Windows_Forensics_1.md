# Windows Registry Forensics — SOC & DFIR Easy Revision Notes

## 1. What is Windows Registry?

Think of the **Windows Registry as a huge notebook/database maintained by Windows**.

Windows stores many things here:

* System configuration
* User preferences
* Installed software information
* User account information
* Recently opened files
* Programs that may have been executed
* USB devices
* Network information
* Startup programs
* Services

For SOC/DFIR, this is extremely useful because **Windows activity leaves traces in the Registry**.

### Simple example

Suppose an employee says:

> "I never connected a USB."

We may check the Registry and find:

```text
SanDisk
Serial Number: ABC123
First Connection: 10 August
Last Connection: 18 August
```

Now we have evidence that the USB was connected.

---

# 2. Registry Structure

The Registry contains:

```text
Root Key
   ↓
Key
   ↓
Subkey
   ↓
Value
   ↓
Data
```

### Easy example

Think of it like a school:

```text
School
 └── Class 9
      └── Student
           └── Name
                └── Somya
```

Similarly:

```text
HKEY_CURRENT_USER
 └── Software
      └── Microsoft
           └── Windows
                └── ...
```

---

# 3. Five Main Root Keys

| Root Key | Easy Meaning                                   |
| -------- | ---------------------------------------------- |
| HKCU     | Information about the currently logged-in user |
| HKU      | Information about loaded user profiles         |
| HKLM     | Information about the whole computer           |
| HKCR     | File/program association information           |
| HKCC     | Current hardware profile                       |

Full names:

```text
HKCU = HKEY_CURRENT_USER

HKU = HKEY_USERS

HKLM = HKEY_LOCAL_MACHINE

HKCR = HKEY_CLASSES_ROOT

HKCC = HKEY_CURRENT_CONFIG
```

### SOC Tip

Remember:

```text
HKCU → User
HKLM → Machine
```

This simple distinction will save you a lot of confusion.

---

# 4. What is a Registry Hive?

A **Registry Hive is a file on the disk that stores Registry data**.

For example:

```text
SYSTEM
SOFTWARE
SAM
SECURITY
NTUSER.DAT
USRCLASS.DAT
Amcache.hve
```

When Windows is running, these files are loaded/mapped into the Registry.

---

# 5. Live System vs Disk Image

This is VERY important in DFIR.

## Live System

The computer is running.

We can use:

```text
regedit.exe
```

because Windows has already loaded the Registry.

---

## Disk Image

Suppose police give us:

```text
computer.E01
```

The computer itself is not running.

The Registry exists as files inside the image.

We cannot simply use:

```text
regedit.exe
```

because the Registry is not loaded as the live Windows Registry.

Instead:

```text
Disk Image
    ↓
Extract Registry Hives
    ↓
Registry Explorer
    ↓
Analyze
```

### DFIR Rule

**Never modify the original evidence if you can avoid it.**

Work on an acquired copy.

---

# 6. System Registry Hives

Most important system hives are located here:

```text
C:\Windows\System32\Config
```

Important files:

| Hive     | Main Purpose                                                  |
| -------- | ------------------------------------------------------------- |
| SYSTEM   | System configuration, services, devices, control sets         |
| SOFTWARE | Installed software, OS information, network history, Run keys |
| SAM      | Local user accounts and account information                   |
| SECURITY | Security-related configuration                                |
| DEFAULT  | Default user/system information                               |

---

# 7. User Registry Hives

User-specific hives are inside:

```text
C:\Users\<username>\
```

## NTUSER.DAT

Location:

```text
C:\Users\<username>\NTUSER.DAT
```

This mainly contains information about that particular user's activity and preferences.

Examples:

* Recent files
* Typed paths
* Search history
* UserAssist
* Run keys
* Other user activity

---

## USRCLASS.DAT

Location:

```text
C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT
```

Important for things such as:

* ShellBags
* User-specific shell information

Both are hidden files.

---

# 8. AmCache

Location:

```text
C:\Windows\AppCompat\Programs\Amcache.hve
```

AmCache is a **very important forensic artifact**.

It contains information related to applications/programs seen by Windows.

It can provide information such as:

* Program path
* SHA1
* Installation information
* Execution-related information
* Deletion-related information

### SOC Use

Suppose:

```text
C:\Users\John\AppData\Local\Temp\invoice.exe
```

is suspicious.

AmCache may help us identify:

```text
Where was it?
What was its hash?
What program was it?
What other metadata exists?
```

### Important

AmCache is **strong evidence**, but do not blindly say:

> "AmCache entry = 100% execution."

Always correlate with other artifacts.

---

# 9. Registry Transaction Logs

Think of Registry transaction logs as a **change diary**.

Windows may write changes to transaction logs before those changes are fully reflected in the main hive.

Example:

```text
SAM
SAM.LOG
SAM.LOG1
SAM.LOG2
```

These files may contain recent Registry changes.

### Why SOC/DFIR cares?

Suppose an attacker modifies a Registry key and then tries to hide it.

The main hive may not tell the complete story.

Transaction logs may contain useful evidence of recent changes.

### Remember

```text
Hive = Main Registry data

.LOG / .LOG1 / .LOG2 = Transaction/change information
```

---

# 10. Registry Backups — RegBack

Older Windows forensic material often refers to:

```text
C:\Windows\System32\Config\RegBack
```

This directory contains backup copies of Registry hives on systems/configurations where RegBack is populated.

Why useful?

Suppose:

```text
Current SYSTEM hive
        ↓
Attacker modified something
```

A previous Registry copy may help investigators compare the older and current state.

### Important

Do not blindly assume modern Windows always has useful automatic RegBack copies.

Always check whether the files actually exist and contain meaningful data.

---

# 11. Data Acquisition

**Data acquisition = safely collecting forensic evidence for analysis.**

Instead of investigating the original system directly:

```text
Original Evidence
       ↓
Acquire / Copy
       ↓
Forensic Analysis
```

This protects evidence integrity and makes the investigation safer.

---

# 12. Tools for Registry Acquisition

## KAPE

KAPE is commonly used for:

* Live data collection
* Forensic artifact collection
* Registry acquisition

It can collect important Windows artifacts quickly.

SOC/DFIR use:

```text
Compromised Windows Machine
        ↓
KAPE
        ↓
Collect Registry + Other Artifacts
        ↓
Analyze
```

---

## Autopsy

Autopsy can work with:

* Disk images
* Live sources

You can navigate to a file and extract it for analysis.

Useful when working with a forensic image.

---

## FTK Imager

FTK Imager can:

* Open disk images
* Mount drives/images
* Export files
* Acquire protected files from a live system

It has an option called:

```text
Obtain Protected Files
```

This can help collect protected Registry hives from a live Windows machine.

### Important limitation

The protected-file collection does **not necessarily collect Amcache.hve**, so collect AmCache separately when required.

---

# 13. Tools for Reading Registry Hives

## Registry Viewer

Looks similar to Windows Registry Editor.

But:

* Usually loads one hive at a time
* Does not properly incorporate transaction logs

---

## Eric Zimmerman's Registry Explorer

This is extremely useful in DFIR.

It can:

* Load multiple hives
* Work with transaction logs
* Present Registry data clearly
* Provide forensic bookmarks

### Why SOC/DFIR analysts like it

Instead of manually searching hundreds of Registry keys, bookmarks help investigators quickly reach important forensic locations.

---

## RegRipper

RegRipper takes a Registry hive and extracts important forensic information.

Input:

```text
Registry Hive
```

Output:

```text
Text Report
```

It is useful for quickly extracting known forensic artifacts.

### Important limitation

RegRipper does not itself account for Registry transaction logs.

Better workflow:

```text
Registry Hive
      +
Transaction Logs
      ↓
Registry Explorer
      ↓
Updated/Merged Hive
      ↓
RegRipper
      ↓
Report
```

---

# 14. System Information

Before investigating a machine, first answer:

> **What machine am I investigating?**

Do not immediately jump into malware.

---

# 15. OS Version

Registry location:

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion
```

This can tell us information about the Windows version/build.

### SOC use

If the evidence came from a triage collection and you don't know the OS version:

```text
SYSTEM + SOFTWARE
        ↓
OS information
```

This helps you understand which artifacts and Registry structures should be expected.

---

# 16. Control Sets

Inside the SYSTEM hive, you may see:

```text
SYSTEM\ControlSet001
SYSTEM\ControlSet002
```

These contain system configuration.

Think of Control Sets as **different stored configurations for Windows startup/system operation**.

---

# 17. CurrentControlSet

On a live system, Windows exposes:

```text
HKLM\SYSTEM\CurrentControlSet
```

This is the active/current configuration.

But in an offline SYSTEM hive, you need to understand which actual ControlSet corresponds to the current one.

Check:

```text
SYSTEM\Select\Current
```

Example:

```text
Current = 1
```

This means:

```text
ControlSet001
```

is the current Control Set.

---

# 18. Last Known Good

Check:

```text
SYSTEM\Select\LastKnownGood
```

This tells us which Control Set represents the last known good configuration.

### Easy memory

```text
Select\Current
        ↓
Current configuration

Select\LastKnownGood
        ↓
Last known good configuration
```

---

# 19. Computer Name

Registry:

```text
SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName
```

This gives the computer name.

### Why important?

Imagine you receive evidence from 20 computers.

You need to make sure:

> "Am I investigating the correct machine?"

Computer Name helps establish that identity.

---

# 20. Time Zone

Registry:

```text
SYSTEM\CurrentControlSet\Control\TimeZoneInformation
```

This is VERY important for timelines.

Why?

Because timestamps may be represented in:

```text
UTC
```

or

```text
Local Time
```

Suppose an event says:

```text
18:00 UTC
```

and the computer is in India.

You need to correctly convert/interpret the time.

Otherwise your timeline can be wrong.

### SOC Rule

Before building a timeline:

```text
Know the system time zone.
```

---

# 21. Network Interfaces

Registry:

```text
SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
```

Each network interface has a GUID.

Information can include:

* IP address
* DHCP information
* Subnet mask
* DNS information
* Network configuration

### SOC use

This helps identify:

> Which network configuration belonged to this machine?

It can also support incident timelines and network investigations.

---

# 22. Past Networks

Windows remembers networks the machine connected to.

Locations:

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged
```

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Managed
```

These can help identify:

* Previous networks
* When the machine was connected to them

### SOC use

Useful when investigating:

> Was this laptop previously connected to a particular network?

---

# 23. Autoruns / Run Keys

These Registry locations can contain programs that automatically start when a user logs in.

Important locations:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Run
```

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
```

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
```

---

# 24. Why Attackers Love Run Keys

Suppose attacker puts:

```text
invoice.exe
```

inside:

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

When the user logs in:

```text
User Login
     ↓
Windows checks Run key
     ↓
invoice.exe starts
```

This is called **persistence**.

The attacker does not have to manually start the malware every time.

### SOC Question

If you see an unknown executable in a Run key:

> Investigate it.

Check:

* File path
* Hash
* Signature
* AmCache
* Prefetch
* Event Logs
* Network activity

---

# 25. Services

Registry:

```text
SYSTEM\CurrentControlSet\Services
```

This contains information about Windows services.

A service can also be abused for persistence.

One important value is:

```text
Start
```

Common value:

```text
0x02
```

means the service starts automatically during system startup.

### SOC Alert

If you see:

```text
Suspicious Service
+
Unknown executable
+
Start = 0x02
```

Investigate immediately.

---

# 26. SAM Hive

SAM contains information about local Windows accounts.

Location:

```text
SAM\Domains\Account\Users
```

It can provide information such as:

* User RID
* Login-related information
* Last login
* Failed login information
* Password change information
* Account policy information
* Group-related information

### SOC use

Useful for:

* Account investigations
* Suspicious login investigations
* Insider threat investigations
* Compromised account analysis

---

# 27. RecentDocs

Windows keeps track of recently opened files.

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

Example:

```text
Salary.xlsx
passwords.txt
invoice.docx
```

### Extension-specific keys

You can also investigate a particular extension.

Example:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.pdf
```

This can help identify recently used PDF files.

### SOC use

If investigating data theft:

```text
RecentDocs
    ↓
Sensitive files accessed?
```

---

# 28. Office Recent Files

Microsoft Office also maintains recent document information.

General location:

```text
NTUSER.DAT\Software\Microsoft\Office\VERSION
```

Example:

```text
NTUSER.DAT\Software\Microsoft\Office\15.0\Word
```

Office 2013 uses:

```text
15.0
```

For newer Office versions, user-specific MRU locations may be used.

Example:

```text
NTUSER.DAT\Software\Microsoft\Office\VERSION\UserMRU\LiveID_####\FileMRU
```

This can contain the path of recently used files.

### SOC use

Suppose employee says:

> "I never opened confidential.xlsx."

Office MRU may help investigate that claim.

---

# 29. ShellBags

This is a VERY useful artifact.

When a user opens folders, Windows remembers how those folders were displayed.

That information creates **ShellBags**.

Locations include:

```text
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\Bags
```

```text
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
```

```text
NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
```

```text
NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags
```

### Why DFIR loves ShellBags

They can provide evidence that a user browsed particular folders.

Example:

```text
E:\HR_DATA
```

If ShellBags shows that folder, it can support the conclusion that the user browsed it.

### Tool

Eric Zimmerman's:

```text
ShellBags Explorer
```

makes ShellBag analysis much easier.

---

# 30. OpenSavePidlMRU

When you open/save a file, Windows often remembers locations used in the Open/Save dialog.

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU
```

This can help investigators understand files/locations recently used through Open/Save dialogs.

---

# 31. LastVisitedPidlMRU

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU
```

This can help identify applications and locations associated with Open/Save activity.

### Easy difference

```text
OpenSavePidlMRU
        ↓
What files/locations were used?

LastVisitedPidlMRU
        ↓
Which applications/locations were visited?
```

---

# 32. TypedPaths

Users can type paths into the Windows Explorer address bar.

Windows may remember them.

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

Example:

```text
C:\Users\John\Downloads
E:\
\\Server\Shared
```

### SOC use

Can help answer:

> Did the user manually type/access this location?

---

# 33. WordWheelQuery

This is related to searches performed through Windows Explorer.

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
```

Example searches:

```text
password
salary
confidential
backup
```

### SOC use

Suppose an employee searches:

```text
"confidential salary"
```

before accessing sensitive files.

This may become useful supporting evidence.

---

# 34. UserAssist

Location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count
```

UserAssist tracks applications launched through Windows Explorer for statistical purposes.

It can contain:

* Program information
* Launch information
* Execution count

### Important limitation

UserAssist does NOT capture every execution method.

For example:

```text
Explorer launch → UserAssist may record it

CMD/PowerShell launch → UserAssist may not record it
```

Therefore:

```text
No UserAssist entry
        ≠
Program definitely never executed
```

This is VERY important.

---

# 35. ShimCache

Location:

```text
SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache
```

Also called:

```text
Application Compatibility Cache
```

Windows uses it mainly for application compatibility.

It can contain information such as:

* File name
* File size
* Modified time

### Important

Do NOT automatically treat every ShimCache entry as proof of execution.

Think:

```text
ShimCache
    ↓
Strong supporting artifact
    ↓
Correlate with other evidence
```

### Tool

Eric Zimmerman's:

```text
AppCompatCacheParser
```

can parse ShimCache data.

---

# 36. AmCache vs ShimCache

| Feature                       | ShimCache                 | AmCache                               |
| ----------------------------- | ------------------------- | ------------------------------------- |
| Main purpose                  | Application compatibility | Compatibility/application information |
| File information              | Yes                       | Yes                                   |
| Execution-related information | Useful                    | Stronger/more detailed                |
| SHA1                          | Limited/not primary       | Yes                                   |
| Path information              | More limited              | More detailed                         |
| DFIR value                    | High                      | Very high                             |

### Easy memory

```text
ShimCache → "I know about this file."

AmCache → "I know much more about this program."
```

Still, neither should be interpreted alone.

---

# 37. BAM

Full form:

```text
Background Activity Monitor
```

Registry:

```text
SYSTEM\CurrentControlSet\Services\bam\UserSettings\{SID}
```

BAM keeps information about application activity, especially background activity.

It can provide:

* Program path
* Last execution time

### SOC use

Useful when investigating:

> When was this executable last active?

---

# 38. DAM

Full form:

```text
Desktop Activity Moderator
```

Registry:

```text
SYSTEM\CurrentControlSet\Services\dam\UserSettings\{SID}
```

DAM is related to Windows power/resource management.

It can also contain activity information.

---

# 39. USB Forensics

Now imagine:

> "An employee may have copied company data to a USB."

Registry can help us investigate.

---

# 40. USBSTOR

Location:

```text
SYSTEM\CurrentControlSet\Enum\USBSTOR
```

This is one of the most important USB artifacts.

It can provide:

* Vendor
* Product
* Version
* Serial number

Example:

```text
SanDisk
Cruzer Blade
32 GB
Serial: ABC123
```

### Important

USBSTOR tells us:

> This USB storage device was associated with the machine.

It does NOT automatically prove:

> Data was copied to the USB.

That requires correlation.

---

# 41. USB

Location:

```text
SYSTEM\CurrentControlSet\Enum\USB
```

This contains information about USB devices.

It can include devices beyond storage devices.

For example:

* Mouse
* Keyboard
* Phone
* USB storage

### Easy difference

```text
USB
   ↓
General USB devices

USBSTOR
   ↓
USB storage devices
```

---

# 42. USB First/Last Connection Times

Location:

```text
SYSTEM\CurrentControlSet\Enum\USBSTOR\Ven_Prod_Version\USBSerial#\Properties\{83da6326-97a6-4088-9453-a19231573b29}\####
```

Important values:

| Value | Meaning          |
| ----- | ---------------- |
| 0064  | First connection |
| 0066  | Last connection  |
| 0067  | Last removal     |

### Easy memory

```text
0064 → First

0066 → Last connected

0067 → Removed
```

---

# 43. USB Volume Name

Location:

```text
SOFTWARE\Microsoft\Windows Portable Devices\Devices
```

This can help identify the friendly/volume name associated with the device.

Example:

```text
HR_BACKUP
OFFICE_USB
KINGSTON
```

Investigators can correlate the device identifier/GUID with USB information to connect the friendly name to the physical device.

---

# 44. The Most Important DFIR Concept: Correlation

This is the thing I want you to remember most.

**One artifact rarely tells the whole story.**

Suppose:

```text
USBSTOR
    ↓
USB connected
```

That does NOT prove:

```text
Data stolen
```

Now add:

```text
USBSTOR
    ↓
USB connected

ShellBags
    ↓
E:\HR_BACKUP browsed

RecentDocs
    ↓
Salary.xlsx accessed

Office MRU
    ↓
Salary.xlsx opened

File system artifacts
    ↓
File copied/created

Timeline
    ↓
All events happen close together
```

Now the story becomes much stronger.

---

# 45. Evidence → Observation → Inference → Conclusion

This is the correct DFIR mindset.

### Bad approach

```text
USBSTOR exists
↓
Employee stole data.
```

Too much conclusion from too little evidence.

### Better approach

```text
USBSTOR
↓
A USB storage device was connected.

ShellBags
↓
A folder on the USB was browsed.

RecentDocs / Office MRU
↓
Sensitive documents were accessed.

File system artifacts
↓
Files were copied/created.

Timeline correlation
↓
The activities happened during the same period.
```

Then:

> These combined artifacts provide strong evidence consistent with data being copied to the USB device.

This is much more professional.

---

# 46. Attacker Perspective

Attackers often try to:

* Delete malware
* Delete files
* Clear logs
* Remove USB devices
* Modify Registry keys
* Hide persistence
* Rename malware
* Use PowerShell/CMD
* Use scheduled tasks/services

But Windows may leave traces in different places.

Example:

```text
Attacker runs malware
        ↓
AmCache
        ↓
BAM
        ↓
Prefetch
        ↓
Event Logs
        ↓
Network activity
```

Even if the original malware is deleted:

```text
malware.exe → deleted
```

some forensic artifacts may still remain.

---

# 47. SOC Investigation Example

Imagine this alert:

```text
Suspicious executable:
C:\Users\John\AppData\Local\Temp\invoice.exe
```

As a SOC/DFIR analyst, do not stop at the file.

Investigate:

```text
1. AmCache
   ↓
   Hash/path/program details

2. UserAssist
   ↓
   Was it launched through Explorer?

3. BAM
   ↓
   Last execution/activity

4. ShimCache
   ↓
   Application compatibility evidence

5. Run Keys
   ↓
   Persistence?

6. Services
   ↓
   Service persistence?

7. Prefetch
   ↓
   Execution history

8. Event Logs
   ↓
   How was it executed?

9. Network Logs
   ↓
   Did it communicate with an external server?
```

Now you are doing a real investigation.

---

# 48. Important Artifact Cheat Sheet

| Question                            | Artifact                                                      |
| ----------------------------------- | ------------------------------------------------------------- |
| Which Windows version?              | SOFTWARE\Microsoft\Windows NT\CurrentVersion                  |
| Which Control Set is current?       | SYSTEM\Select\Current                                         |
| Last known good Control Set?        | SYSTEM\Select\LastKnownGood                                   |
| Computer name?                      | SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName    |
| Time zone?                          | SYSTEM\CurrentControlSet\Control\TimeZoneInformation          |
| Network interfaces?                 | SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces |
| Past networks?                      | NetworkList\Signatures                                        |
| Startup programs?                   | Run / RunOnce keys                                            |
| Services?                           | SYSTEM\CurrentControlSet\Services                             |
| User accounts?                      | SAM                                                           |
| Recent files?                       | RecentDocs                                                    |
| Office recent files?                | Office MRU                                                    |
| Folder browsing?                    | ShellBags                                                     |
| Open/Save activity?                 | OpenSavePidlMRU                                               |
| Last visited locations/apps?        | LastVisitedPidlMRU                                            |
| Typed Explorer paths?               | TypedPaths                                                    |
| Windows searches?                   | WordWheelQuery                                                |
| Explorer-launched applications?     | UserAssist                                                    |
| Application compatibility evidence? | ShimCache                                                     |
| Detailed application metadata?      | AmCache                                                       |
| Background application activity?    | BAM                                                           |
| USB storage devices?                | USBSTOR                                                       |
| General USB devices?                | USB                                                           |
| USB first/last connection/removal?  | USB Properties values                                         |
| USB friendly/volume name?           | Windows Portable Devices                                      |

---

# 49. Super Short Revision

If you have only 2 minutes before an exam/interview, remember this:

```text
HKCU → Current User
HKLM → Whole Machine

SYSTEM → System configuration
SOFTWARE → Software/OS configuration
SAM → Accounts
SECURITY → Security configuration
NTUSER.DAT → User activity
USRCLASS.DAT → User shell activity
AmCache → Detailed program information

UserAssist → Explorer-launched programs
ShimCache → Application compatibility evidence
BAM → Background activity
Run Keys → Persistence
Services → Service configuration/persistence

RecentDocs → Recent files
Office MRU → Recent Office files
ShellBags → Folder browsing
TypedPaths → Typed Explorer paths
WordWheelQuery → Explorer searches

USBSTOR → USB storage devices
USB → USB devices
0064 → First connection
0066 → Last connection
0067 → Last removal
```

---

# 50. Golden SOC/DFIR Rule

Never think:

```text
One artifact = Final answer
```

Think:

```text
Artifact
   ↓
What does it actually prove?
   ↓
What does it NOT prove?
   ↓
Which other artifact can confirm it?
   ↓
Build timeline
   ↓
Make conclusion
```

### Example

```text
AmCache
   ↓
Strong evidence of program activity

+
BAM
   ↓
Last execution/activity

+
Prefetch
   ↓
Execution history

+
Event Logs
   ↓
Execution method

+
Network Logs
   ↓
Possible C2 communication

+
Run Key
   ↓
Persistence

=
Much stronger incident story
```

**That is the mindset you should develop as a SOC/DFIR analyst.**
