# MentorBee Eduverse — Class Link Management & Broadcast System
## Official Operations & User Manual (Comprehensive Guide)

---

## 📌 1. System Overview & Architecture

**MentorBee Class Link Management System** is a mission-critical platform engineered for MentorBee Eduverse to streamline live Zoom class scheduling, WhatsApp broadcast message generation, and mentor link access across all 106+ educational batches (8th, 9th, 10th, 11th Science/Commerce, and 12th Science/Commerce) in both State and CBSE Syllabuses.

### Key Architectural Pillars
- **Role-Based Access Control (RBAC)**: Class Coordinators only manage their assigned classes; Super Admin oversees the entire institution.
- **Smart Zoom AI / Regex Parser**: Paste raw WhatsApp text with Zoom meeting invites, and the system automatically extracts the Zoom Link, Meeting ID, and Passcode in milliseconds.
- **1-Click WhatsApp Broadcast Template**: Standardized formatted messages ready to copy and dispatch instantly to student broadcast channels.
- **Real-Time WebSocket Sync**: Live updates pushed instantly to all connected mentor dashboards without requiring manual page refresh, reinforced with a 4-second auto-poll fallback.
- **Security & Audit Trail**: Real-time logging of all mentor logins, message copies, link copies, and Zoom launches with IP addresses and timestamps.

---

## 👥 2. User Roles & Login Credentials Reference Matrix

### A. Admin & Class Coordinators Portal (`/admin`)

| Name | Role | Email | Default Password | Assigned Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | Super Administrator | `admin@mentorbee.com` | `AdminPassword@123` | **ALL Classes & Audit Logs** |
| **ABIN M M** | Class Coordinator | `abin@mentorbee.com` | `AbinPassword@8th` | **8th Class (State & CBSE)** |
| **ABHIJITH M B** | Class Coordinator | `abhijith@mentorbee.com` | `AbhijithPassword@9th` | **9th Class (State & CBSE)** |
| **SREEHARI R** | Class Coordinator | `sreehari@mentorbee.com` | `SreehariPassword@10th` | **10th Class (State & CBSE)** |
| **PAVIN PAULSON** | Class Coordinator | `pavin@mentorbee.com` | `PavinPassword@11sci` | **11th Science (State & CBSE)** |
| **AKASH** | Class Coordinator | `akash@mentorbee.com` | `AkashPassword@11com` | **11th Commerce (State & CBSE)** |
| **MURALI** | Class Coordinator | `murali@mentorbee.com` | `MuraliPassword@12th` | **12th Science & 12th Commerce** |

---

### B. Staff & Mentors Authentication Matrix (`/mentor/login` or `/`)

*Universal Staff Access: Every mentor has access to all batches and sessions across both CBSE and State syllabuses.*

| Credential Field | Value | Notes |
| :--- | :--- | :--- |
| **Your Full Name** | *(Mandatory staff input)* | Recorded in Audit Trail so Admin knows who entered and shared each link |
| **Username** | `mentor` | Common staff username |
| **Password** | `agentBEE` | Common mentor access password |
| **Scope** | **ALL Classes & Streams** | Access to all 8th, 9th, 10th, 11th, and 12th batches |

---

## 🛠️ 3. Admin & Coordinator Portal (`/admin`)

The Administrative Console provides total operational control over sessions, batches, and security logs.

### 3.1 Top Navigation & Identity Status
- **User Badge**: Displays logged-in coordinator name and authorized scope badge (e.g. `COORD: 10TH` or `SUPER ADMIN`).
- **Mentor Portal Link (`↗`)**: Direct shortcut to open the live mentor view in a new browser tab.
- **Logout**: Clears the JWT admin token and returns to the login screen.

### 3.2 Tab 1: Sessions Management
- **Creating a Session**:
  1. Click **`+ Create Session`**.
  2. *(Recommended)* Paste full Zoom meeting invite into **`⚡ Quick Zoom Paste Auto-Fill`** and click **`Auto Parse Link & Credentials`**.
  3. Select **Assigned Class Stream** (e.g., *10th Class*) and **Syllabus Filter** (e.g., *CBSE*).
  4. Select the target **Batch** from the filtered dropdown.
  5. Enter the **Class Topic / Subject** (e.g., *Mathematics - Quadratic Equations*).
  6. Confirm **Date** and **Start Time** (IST).
  7. Click **`Save & Broadcast Session`**.
- **Editing a Session**: Click **`Edit`** on any row to modify topics, meeting links, or start times. Changes trigger instant WebSocket notifications to mentors.
- **Deleting a Session**: Click **`Delete`** to remove obsolete sessions with confirmation protection.

### 3.3 Tab 2: Batches Management
- View all 106+ State and CBSE batches categorized by grade.
- Click **`+ Create Batch`** to register new classes. The system automatically infers syllabus and grade categories from the name.
- Click **`Edit`** to adjust batch nomenclature or status.

### 3.4 Tab 3: Security & Access Audit Trail (Super Admin Exclusive)
- Real-time compliance logging tracking mentor actions:
  - **`🔑 Staff Login`**: Staff sign-in events with timestamp and IP address.
  - **`✓ Copied Message`**: Every WhatsApp broadcast message copied by staff.
  - **`✓ Copied Link`**: Direct URL copies.
  - **`⚡ Launched Zoom`**: Live Zoom meeting launches.
- Click **`↻ Refresh Logs`** to retrieve the latest 100 access records.

---

## 📱 4. Staff & Mentor Portal (`/` and `/mentor/login`)

Designed for lightning-fast operation on mobile smartphones, tablets, and desktops with Universal Access.

### 4.1 Login Procedure
1. Navigate to `/` or `/mentor/login`.
2. Enter your **Full Name** *(Mandatory — used for Admin accountability and audit logs)*.
3. Common Username: `mentor`.
4. Enter the **Mentor Password**: `agentBEE`.
5. Click **`Access All Class Sessions`**.

### 4.2 Dashboard Controls, Instant Search & Class Filtering
- **CBSE vs STATE Primary Tabs**: Switch between CBSE and State syllabuses with dynamic live count badges.
- **🔍 Instant Search Bar**: Search dynamically by Batch Name, Subject/Topic, or Time. Results filter in real-time.
- **Class Filter Chips (Inside Syllabus)**: Filter instantly between `All Classes`, `8th`, `9th`, `10th`, `11th Sci`, `11th Com`, `12th Sci`, and `12th Com`.
- **Today vs Upcoming Tabs**: Filter between today's active schedule and future sessions.

### 4.3 1-Click Class Actions & Audit Accountability
- **📋 Copy Message**: Generates the standardized WhatsApp broadcast text with 1 tap. Automatically records the staff member's name in the Admin Security Audit Log.
- **🚀 Join Zoom**: Direct link to open the Zoom app or web meeting room. Records the launch action in the Admin Security Audit Log.

---

## ⚡ 5. Standard WhatsApp Broadcast Template

When mentors click **`Copy Message`**, the system outputs:

```text
*MENTORBEE EDUVERSE*
*10TH CBSE EVNG KL BATCH*
---------------------------------------
*TOPIC : MATHEMATICS - QUADRATIC EQUATIONS*
*DATE : AUGUST 21, 2026*
*TIME : 07:00 PM IST*


*Join Zoom Meeting*
https://zoom.us/j/99887766554?pwd=samplepassword

*Meeting ID: 998 8776 6554*
*Passcode: 123456*
```

---

## 🛠️ 6. Render Hosting Inactivity & Sleep Prevention Solutions

Render's Free Tier web services spin down (sleep) after 15 minutes of inactivity. When a request arrives, the app experiences a 50–70s cold start delay or timeout. Here is how this is solved:

### Solution 1: Automated In-App Heartbeat (Pre-Configured)
The application includes a background worker (`app/services/keep_alive.py`) that pings its own `/api/health` endpoint every 9 minutes when deployed on Render.
- When deploying on Render, Render provides `RENDER_EXTERNAL_URL` automatically.
- The background task detects this URL and keeps the app warm continuously!

### Solution 2: Free 24/7 External Pinger (UptimeRobot — Recommended & Guaranteed)
To guarantee 100% zero-sleep uptime even if the container restarts:
1. Create a free account at **[UptimeRobot.com](https://uptimerobot.com)**.
2. Click **`Add New Monitor`**:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `MentorBee System`
   - **URL (or IP)**: `https://<your-app-name>.onrender.com/api/health`
   - **Monitoring Interval**: `5 minutes` or `10 minutes`
3. Click **`Create Monitor`**.
4. UptimeRobot will ping your Render service 24/7, resetting the inactivity timer so Render **never sleeps**.

---

## 📞 7. Troubleshooting & FAQs

- **Password Rejected?** Use the common mentor password: `agentBEE`.
- **Missing Name Error?** Staff name is mandatory so Admin can track who accessed and copied links.
- **Auto-Sync Disconnected?** The system reconnects automatically every 4-5 seconds.
- **Admin Support**: Contact `admin@mentorbee.com` for credential resets.
