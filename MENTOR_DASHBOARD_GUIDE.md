# MentorBee Eduverse — Mentor Dashboard Operational Guide
## Live Class Link Access, Search, Filtering & Security Protocol

---

## 📌 1. Overview & Purpose
This guide is the official standard operating procedure (SOP) for all **Mentors and Academic Staff** accessing the **MentorBee Class Link & Session Portal**.

As a Mentor, your portal provides instant, universal access to live Zoom links, meeting IDs, passcodes, and pre-formatted WhatsApp broadcast messages across all educational batches (8th to 12th, State & CBSE).

> [!IMPORTANT]
> **Accountability & Zero-Tolerance Policy**: Every login, link copy, message generation, and Zoom session launch is **actively monitored and logged** in the Super Admin Audit Trail with your Name, Timestamp, and IP address. Follow the security guidelines in this document strictly.

---

## 🔐 2. Portal Login & Authentication

Navigate to the portal URL (`/` or `/mentor/login`) on your phone, tablet, or desktop browser.

### 2.1 Login Credentials Matrix

| Field | Value / Requirement | Details |
| :--- | :--- | :--- |
| **Your Full Name** | *(Your Official Name)* | **Mandatory.** Enter your actual name (e.g., `Devdarsh P S`, `Rahul Sharma`). This identifies you in the Admin Security Logs. |
| **Username** | `mentor` | Common staff username. |
| **Password** | `agentBEE` | Common mentor verification password *(case-sensitive)*. |
| **Access Scope** | **Universal Access** | Unlocks all 106+ batches across both State & CBSE syllabuses. |

### 2.2 Step-by-Step Login Procedure
1. Open the portal: `https://<your-portal-url>/mentor/login`.
2. In the **Your Full Name** field, type your full official name.
3. Keep the **Username** as `mentor`.
4. Enter the password: `agentBEE`.
5. Tap **`Access All Class Sessions`**.
6. You will be redirected immediately to the live class hub. Your name and **`ALL CLASSES`** status will appear in the top-right header.

---

## 🔍 3. How to Search for Classes

The mentor dashboard features a **Real-Time Instant Search Engine** positioned right below the syllabus switcher.

```
+------------------------------------------------------------------------+
| 🔍 Search by topic, batch name, subject, or time...                [×] |
+------------------------------------------------------------------------+
```

### 3.1 Search Capabilities
You can search across any of the following parameters with zero page reloads:
* **Batch Name**: Type `10TH CBSE`, `EVNG`, `KL BATCH`, `STATE ONLINE`, etc.
* **Subject & Topic**: Type `Mathematics`, `Physics`, `Quadratic Equations`, `Organic Chemistry`, etc.
* **Scheduled Time**: Type `07:00`, `PM`, `AM`, `08:30`, etc.
* **Grade**: Type `10th`, `11th`, `12th`, `8th`, etc.

### 3.2 Instant Filtering & Clearing
* As you type each letter, the dashboard instantly narrows down the displayed cards to matching sessions.
* **Clear Search**: Tap the **`×`** button at the right end of the search input to reset the search instantly.
* If no classes match your query, an empty state will appear with a **`Clear Search Query`** shortcut button.

---

## 🎛️ 4. How to Filter Classes

Because every mentor has access to all batches, the dashboard provides a **two-tier structured filter system** for fast navigation.

### 4.1 Primary Tier: CBSE vs. STATE vs. EXAM KILLER
At the very top of the dashboard, use the primary switcher tabs:

```
[  🔵 CBSE  (14)  ]   [  🟢 STATE  (18)  ]   [  ⚡ EXAM KILLER  (6)  ]
```

* **CBSE Tab**: Displays only CBSE affiliated batches and classes.
* **STATE Tab**: Displays only Kerala State Board batches and classes.
* **⚡ EXAM KILLER Tab**: Dedicated section for high-intensity Exam Killer crash batches, model exams, and revision discussions (separated completely from regular classes).
* Dynamic counter badges indicate the exact number of active sessions available in each section.


---

### 4.2 Secondary Tier: Class / Grade Chips
Directly beneath the time tabs, tap any grade chip to filter sessions within your selected syllabus:

| Chip Button | Filter Applied |
| :--- | :--- |
| **`All Classes`** | Shows all grades (8th through 12th) in the selected syllabus. |
| **`8th`** | Displays only 8th Standard batches. |
| **`9th`** | Displays only 9th Standard batches. |
| **`10th`** | Displays only 10th Standard batches. |
| **`11th Sci`** | Displays 11th Science stream batches (Physics, Chemistry, Maths, Bio). |
| **`11th Com`** | Displays 11th Commerce stream batches (Accountancy, Economics, Business). |
| **`12th Sci`** | Displays 12th Science stream batches. |
| **`12th Com`** | Displays 12th Commerce stream batches. |

---

### 4.3 Schedule Tabs: Today vs. Upcoming
* **Today's Classes**: Default view. Shows all classes scheduled for the current date in chronological order.
* **Upcoming**: Shows scheduled classes for tomorrow and future dates with formatted date tags (e.g., `Fri, Aug 22`).

---

## 🕒 5. How to Check for the Latest Changed ID / Timings

In fast-paced online learning environments, Zoom links, meeting IDs, or teachers may change at the last minute due to technical issues or studio reassignments.

### 5.1 The "UPDATED [Time]" Timestamp Badge
Every session card displays a dedicated timestamp badge in the upper-right corner:

```
+------------------------------------------------------------------------+
| [🔵 CBSE] [10TH] [10TH CBSE EVNG KL BATCH]       [🕒 UPDATED 06:45 PM] |
|                                                                        |
| TOPIC : MATHEMATICS - QUADRATIC EQUATIONS                              |
| 🕒 07:00 PM IST                                                        |
|                                                                        |
| [ 📋 Copy Message ]                            [ 🚀 Join Zoom ]        |
+------------------------------------------------------------------------+
```

### 5.2 Verification Checklist Before Dispatching Links
1. **Check the `UPDATED` Badge**: If a coordinator modified the Zoom Link, Meeting ID, or Passcode, the badge updates to show the exact time of the modification (e.g., `UPDATED 06:45 PM`).
2. **Real-Time WebSocket Sync**: Changes made by coordinators are pushed automatically to your screen within milliseconds without needing to refresh the page.
3. **4-Second Background Polling**: The dashboard automatically checks the server every 4 seconds to ensure your screen is 100% synchronized with the central database.
4. **Golden Rule**: If a class was reported to have link issues, check the `UPDATED` badge. If the update timestamp is recent, tap **`Copy Message`** to obtain the fresh link.

---

## 📋 6. 1-Click WhatsApp Broadcast & Zoom Actions

### 6.1 Copying WhatsApp Broadcast Message
1. Tap the golden **`Copy Message`** button on the target class card.
2. The button will immediately turn green and display **`✓ Copied!`** with a confirmation toast popup.
3. The standardized template is copied to your clipboard:

**For Exam Killer / Revision Batches:**
```text
*MENTORBEE EDUVERSE*
*EXAM KILLER 4.0 - REVISE*
*10TH CBSE KL REV-2 BATCH (2)* 
-----------------------------------
*TOPIC : CHEMISTRY*
*DATE : OCTOBER 26, 2026*
*TIME : 06:00 PM IST*


*Join Zoom Meeting*
https://us06web.zoom.us/j/89982457863?pwd=cDv1PpMA7zYEjbQ3kVgZGqbbwakqi3.1

*Meeting ID: 899 8245 7863*
*Passcode: mentorbee*
```

**For Regular Batches:**
```text
*MENTORBEE EDUVERSE*
*10TH CBSE EVNG KL BATCH*
-----------------------------------
*TOPIC : MATHEMATICS - QUADRATIC EQUATIONS*
*DATE : AUGUST 21, 2026*
*TIME : 07:00 PM IST*


*Join Zoom Meeting*
https://zoom.us/j/99887766554?pwd=samplepassword

*Meeting ID: 998 8776 6554*
*Passcode: 123456*
```
4. Paste directly into your official WhatsApp batch announcement group.

### 6.2 Joining Zoom Directly
Tap **`Join Zoom`** to launch the Zoom application or web client directly into the host/mentor room.

---

## 🚨 7. CRITICAL SECURITY WARNING: ID MIS-SHARING & AUDIT MONITORING

> [!CAUTION]
> ### STRICT COMPLIANCE & MONITORING NOTICE
> **Every single interaction on this portal is recorded in a tamper-proof audit log.**
> 
> The system tracks and logs:
> - **Who logged in**: Your exact Name entered during login.
> - **Who copied which link**: The exact batch, class topic, date, and second the message was copied.
> - **Who launched Zoom**: The exact batch Zoom meeting launched.
> - **Device & Network**: IP address and client timestamp.

### ⚠️ Rules on ID Sharing:

1. **NEVER Cross-Share Links Between Batches**:
   - Sending a 10th State link to a 10th CBSE broadcast group causes severe disruption, student confusion, and security lockouts.
   - Always double-check the **Batch Name** on the card and in the WhatsApp template header before hitting send.
2. **NEVER Share Unverified or External Links**:
   - Only broadcast links generated from the MentorBee portal. External personal Zoom links are strictly forbidden.
3. **DO NOT Share Your Login Password**:
   - The password `agentBEE` is strictly for MentorBee authorized staff. Do not disclose it to students, parents, or external contractors.
4. **Accountability**:
   - If an unauthorized, incorrect, or corrupted link is dispatched to students, Super Admin immediately inspects the **Security Access Log** (`/admin/dashboard`).
   - The audit log reveals the exact mentor name who clicked "Copy Message" for that batch and time.
   - Negligent mis-sharing or unauthorized forwarding will result in immediate administrative and disciplinary action.

---

## 💡 8. Troubleshooting & Frequently Asked Questions (FAQ)

### Q1: The password was rejected on login. What should I check?
- The common mentor password is **`agentBEE`** *(lowercase `agent` followed by uppercase `BEE`)*.
- Ensure you have entered your **Full Name**; the login form will reject submissions with an empty name.

### Q2: I don't see my class in the list.
- Check the **Syllabus Switcher**: Verify whether you are in the **CBSE** or **STATE** tab.
- Check the **Grade Filter Chip**: Ensure you haven't selected a different grade (e.g. selected `8th` when looking for `10th`). Tap **`All Classes`** to view everything.
- Check the **Search Bar**: Ensure the search box is clear of previous queries. Tap the **`×`** button.

### Q3: A coordinator said they changed the link. How do I make sure I have the new one?
- Look at the **`UPDATED [Time]`** badge on the card.
- Tap **`Copy Message`** again; it will automatically extract the updated credentials.

### Q4: The app seems slow to load after some time.
- The cloud server automatically maintains a keep-alive heartbeat. If accessing during an off-peak period, wait a few seconds on first load; all data syncs automatically every 4 seconds once loaded.

---

## 📞 9. Administrative Support
For urgent schedule alterations, link corrections, or coordinator escalation:
- **Super Admin**: `admin@mentorbee.com`
- **Class Coordinators**: Contact your grade coordinator (Abin, Abhijith, Sreehari, Pavin, Akash, Murali).
