#  Slingway Inc. Web Server Investigation (Elastic Stack)

---

##  Context

Slingway Inc., a toy company, detected suspicious activity on its e-commerce web server along with possible unauthorized database changes.

The logs were provided through Elastic Stack, and the suspicious activity started on **July 26, 2023**.

At this point, there was no clear idea about:

* where the attack started
* what exactly the attacker did
* how deep the compromise was

So the investigation had to be built step-by-step from logs only.

---

## Objective

The goal of this investigation was to:

* Identify reconnaissance and enumeration techniques used by the attacker
* Detect how the attacker gained access to the system
* Understand post-exploitation behavior
* Identify sensitive data accessed (especially database activity)

---

##  Investigation Approach

When I opened the logs in Elastic, there were too many logs and too many fields. It was overwhelming and I did not understand where to start.

Instead of randomly searching, I decided to:

* start with commonly used fields
* look for abnormal patterns
* and build the investigation step-by-step based on evidence

I avoided guessing and focused on **what the logs are actually showing**.

---

##  Evidence-Based Investigation

---

###  Stage 1: Identifying Initial Anomaly (404 Errors)

I started by checking the checking popular fields section and there I found the `response.code` field.

I noticed a large number of **404 responses**.

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 24 56 AM" src="https://github.com/user-attachments/assets/21d34b2c-e805-48a9-9b4b-d4f23cdd0443" />

At first, I did not fully understand why this was happening. So I searched and learned:

* 404 means the requested resource does not exist on the server

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 22 45 AM" src="https://github.com/user-attachments/assets/406c5561-1601-44e4-ba09-1bc82a6cff0d" />
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 23 59 AM" src="https://github.com/user-attachments/assets/84cc84cf-cc7c-4499-a232-210d15f795db" />
This indicated:
➡️ someone is requesting multiple non-existing paths

This is not normal user behavior.

---

### Key Observation

I checked the `transaction.remote_address` field. 
I did not fully understand what was this. So I searched and learned:
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 27 15 AM" src="https://github.com/user-attachments/assets/3e511e7a-faec-4c6c-b76a-4b359546555c" />

After checking it I found:

* a **single IP address** sending most of these 404 requests

➡️ This strongly indicated automated activity

➡️ I marked this IP as the **attacker IP**
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 25 52 AM" src="https://github.com/user-attachments/assets/1ed2bfbe-8d78-4b44-84ac-e3c830460178" />

---

###  Stage 2: Reconnaissance Activity (Nmap & Gobuster)

I filtered logs using this attacker IP and started opening events.

Initially, I did not understand much, so I focused on recognizable patterns and start with opening the first event.

---

####  Nmap Detection

In the first event I saw:

* `nmap` in logs
  
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 30 25 AM" src="https://github.com/user-attachments/assets/5813ada8-380d-47c3-a2ad-cb50e4494f87" />

Since I already knew:
 Nmap is used for scanning

I concluded:
 attacker is performing **reconnaissance (port scanning)**

---

####  Gobuster Detection

Then after a little scrolling, I found:

* `gobuster`

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 33 10 AM" src="https://github.com/user-attachments/assets/662c9a0a-80f0-4b3a-a7f1-3b8e9b0bb4a8" />

I was not fully sure, so I searched:

 Gobuster is used for:

* directory brute forcing
* finding hidden endpoints

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 33 20 AM" src="https://github.com/user-attachments/assets/b738dcdb-9a35-40a8-80aa-8e7ecdd37dd9" />
 
---

###  Log Behavior

I observed:

* multiple `.php` files
* multiple `.txt` files

This confirmed: attacker is trying to discover hidden directories/files

There when I search for flag in the search bar I got a flag directory with a THM Flag in it.
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 59 52 AM" src="https://github.com/user-attachments/assets/cd3f6e50-8638-482e-ac5c-4d76893f4a83" />

---

###  Mistake (Critical Learning)

At this stage, I made two major mistakes:

1. I was only seeing **100 events at a time**
2. I had applied filter:

   ```
   attacker IP + 404
   ```

➡️ Because of this:

* I missed a large portion of attacker activity

---

###  Fix

I corrected this by:

* removing the 404 filter
* keeping only attacker IP

➡️ This gave full visibility of attacker behavior

---

### Stage 3: Brute Force Activity (Hydra)

Next, I decided to check **User-Agent field**

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 54 22 AM" src="https://github.com/user-attachments/assets/10561b2c-94e7-4e7a-ad5f-9f0a51eac467" />

I found:

* `hydra`

I searched it and learned:

 Hydra is used for brute force attacks (login cracking)

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 9 55 24 AM" src="https://github.com/user-attachments/assets/667c26c5-ff60-47be-8244-4930622536c5" />

---

### 🔍 Log Evidence

I saw:

* repeated login attempts

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 04 32 AM" src="https://github.com/user-attachments/assets/c445c3ff-8442-49aa-b1f3-4fce6727869b" />

* `request.headers.Authorization` field

<img width="1104" height="696" alt="Screenshot 2026-03-22 at 10 18 35 AM" src="https://github.com/user-attachments/assets/3b43bf94-abd0-4c34-9256-4517c94aff53" />

➡️ attacker is trying different credentials

---

###  Stage 4: Authentication Analysis (401 → 200 Logic)

I observed:

* many `401 Unauthorized` responses

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 04 45 AM" src="https://github.com/user-attachments/assets/cd5bbc0e-25ec-4297-b9e8-de660acbd6a2" />

I confirmed:

 401 means invalid credentials

 attacker is trying multiple passwords

---

### Problem

* too many attempts
* passwords encoded
* manual tracking not possible

---

###  Breakthrough Logic

I thought:

```text
If attacker gets correct credentials → response should be 200
```

---

###  Validation

* I checked logs → response 200 existed
* So my logic was correct

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 23 31 AM" src="https://github.com/user-attachments/assets/30a2a511-c4b0-42d0-b54c-0c62049da56b" />

---

###  Execution

I:

* filtered response = 200
* matched timestamps with last 401 (~14:29)

Then I opened that event

 That contained the **correct password**

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 24 59 AM" src="https://github.com/user-attachments/assets/a223bfbc-9c3a-4d5f-8c0c-95a697eda324" />
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 25 37 AM" src="https://github.com/user-attachments/assets/f4418be1-082c-498a-a709-81654d5bb9bc" />

---

###  Additional Confirmation

I also noticed:

* User-Agent changed from **Hydra → Linux browser**

 This confirmed:
attacker successfully logged in

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 26 59 AM" src="https://github.com/user-attachments/assets/16515035-a11b-4b7c-bfbd-948d2f0c238f" />

---

###  Stage 5: Post-Login Activity (Web Shell Upload)

After identifying login success, I:

* filtered logs after login timestamp

Now logs were reduced and clearer

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 35 05 AM" src="https://github.com/user-attachments/assets/a8696779-0e35-4a1a-abeb-69ca85631e0a" />

---

###  Key Finding

I found:

* a **POST request**
* endpoint: `upload.php`

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 36 27 AM" src="https://github.com/user-attachments/assets/5541e94d-6c19-4758-84fe-98b9173da789" />

---

###  Interpretation

POST request = data sent to server

 likely file upload

---

### 🔍 Further Analysis

I saw:

* command execution (`whoami`)

 This confirmed:

```text
Attacker uploaded a web shell
```

 attacker now has **remote command execution**

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 37 58 AM" src="https://github.com/user-attachments/assets/abe82e7c-5091-4a6e-8263-5e5b293a95fa" />

Here In this POST request I got a THM Flag.

---

###  Stage 6: Post Exploitation Confusion

At this stage:

* too many directories
* too many requests

I could not clearly understand attacker behavior

This phase was confusing because:

* attacker activity became complex
* logs were not linear

---


---

### 🟥 Stage 8: LFI Indicators (Partial Understanding)

After further searching, I observed:

* `/etc/passwd`
* parameters like `page=`

<img width="1104" height="694" alt="Screenshot 2026-03-22 at 11 08 51 AM" src="https://github.com/user-attachments/assets/8aa6d64c-7cf0-429f-a9ad-b77f2e803dbe" />

I did not fully understand initially

Later I realized:

➡️ This may indicate **LFI (Local File Inclusion)** attempts

<img width="1100" height="691" alt="Screenshot 2026-03-22 at 11 09 14 AM" src="https://github.com/user-attachments/assets/11275745-1e28-4b7d-b042-36c59f52b600" />
<img width="1105" height="696" alt="Screenshot 2026-03-22 at 11 09 42 AM" src="https://github.com/user-attachments/assets/968f4c85-e59f-477f-8f6d-b42047645aa7" />

---

###  Additional Observation

I saw:

* base64 encoded data

I did not fully understand the use

But it suggested:
 attacker manipulating or encoding data

---

###  Stage 9: Database Access (phpMyAdmin)

Then I found:

* attacker accessed **phpMyAdmin**

 This means:
 attacker reached database management interface

<img width="1106" height="698" alt="Screenshot 2026-03-22 at 11 10 25 AM" src="https://github.com/user-attachments/assets/085f885a-4ad8-406a-aaac-329d56560517" />

---

###  Stage 10: Database Operations

I observed multiple requests:



* `index.php`
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 11 11 17 AM" src="https://github.com/user-attachments/assets/e0da66f6-83b1-46f0-9664-921a00305ec8" />
* Some passwords inside it 
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 11 11 32 AM" src="https://github.com/user-attachments/assets/147a8ddf-8650-470f-9021-cbd051170ec4" />
* `ajax.php`
* multiple POST requests
* multiple `.png` requests (unclear purpose)
<img width="1470" height="956" alt="Screenshot 2026-03-22 at 11 14 51 AM" src="https://github.com/user-attachments/assets/df77e018-b331-455b-adb6-6d49dafc848d" />

---

###  Key  Sensitive Data Discovery

After further searching:

I found:

* database related to **customer credit cards**

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 11 15 09 AM" src="https://github.com/user-attachments/assets/579bcd06-27be-4cd7-a39f-b8f208b08a23" />

 This was critical data

Indicates **data access / potential exfiltration**

I found:

* credit card database opened

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 10 57 05 AM" src="https://github.com/user-attachments/assets/16cc7f14-e8fd-4fc7-826c-a7c6b533b118" />

Also:

* `export.php`
* `import.php`
* `tbl_replace`
* `lint.php`

<img width="1470" height="956" alt="Screenshot 2026-03-22 at 11 21 35 AM" src="https://github.com/user-attachments/assets/a997ad95-950d-47c5-b5c6-988508ba7857" />

---

###  Interpretation

 attacker is:

* interacting with database
* modifying / exporting data
* possibly extracting sensitive information

---

##  Full Attack Chain

1. Attacker scans server using Nmap
2. Uses Gobuster for directory discovery
3. Finds login endpoint
4. Performs brute force using Hydra
5. Gains access (401 → 200 transition)
6. Uploads web shell via POST request
7. Executes commands remotely
8. Explores system and directories
9. Accesses phpMyAdmin
10. Interacts with database
11. Accesses sensitive credit card data

---

##  Challenges & Mistakes

* Initial confusion due to too many logs
* Limited visibility (100 events only)
* Incorrect filtering (IP + 404 together)
* Difficulty understanding post-exploitation
* Lack of clarity around LFI and encoding

---

##  Key Learnings

* Always start with simple anomalies (404 patterns)
* Avoid over-filtering early
* Focus on behavior, not just values
* 401 → 200 logic is critical for login detection
* POST requests often indicate actions (upload / execution)
* Investigation is iterative, not linear

---

##  Tools Used

* Elastic Stack (Kibana)
* Log analysis
* External research (Nmap, Gobuster, Hydra)

---

##  Conclusion

This investigation showed how an attacker:

* moved from reconnaissance to exploitation
* gained access via brute force
* established control using web shell
* and accessed sensitive database information

The key takeaway was learning how to move from confusion to structured analysis using evidence from logs.






