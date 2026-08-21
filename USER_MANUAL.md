# MentorBee Eduverse — Class Link Management & Broadcast System
## Official User & Operations Manual

---

## 📌 1. System Overview

**MentorBee Class Link Management System** is a mission-critical platform engineered for MentorBee Eduverse to streamline live Zoom class scheduling, WhatsApp broadcast message generation, and mentor link access across all educational batches (8th, 9th, 10th, 11th Science/Commerce, and 12th Science/Commerce).

### Key Features
- **Role-Based Access Control**: Class Coordinators only manage their assigned classes; Super Admin oversees the entire institution.
- **Smart Zoom AI / Regex Parser**: Paste raw WhatsApp text with Zoom meeting invites, and the system automatically extracts the Zoom Link, Meeting ID, and Passcode.
- **1-Click WhatsApp Broadcast Template**: Standardized formatted messages ready to copy and dispatch instantly to student broadcast channels.
- **Real-Time WebSocket Sync**: Live updates pushed instantly to all connected mentor dashboards without requiring manual page refresh.
- **Security & Audit Trail**: Real-time logging of all mentor logins, link copies, message copies, and meeting launches.

---

## 👥 2. User Roles & Login Credentials

### A. Staff & Mentors Portal (`/mentor/login`)
Mentors log in by selecting their name/class and entering the authorized staff verification passcode.

- **Universal Staff Passcode**: `AGENTBEE0809`
- **Class-Specific Passcodes**:
  - **8th Class**: `MENTOR8TH` or `BEE8TH`
  - **9th Class**: `MENTOR9TH` or `BEE9TH`
  - **10th Class**: `MENTOR10TH` or `BEE10TH`
  - **11th Science**: `MENTOR11SCI` or `BEE11SCI`
  - **11th Commerce**: `MENTOR11COM` or `BEE11COM`
  - **12th Science**: `MENTOR12SCI` or `BEE12SCI`
  - **12th Commerce**: `MENTOR12COM` or `BEE12COM`
  - **All Classes**: `MENTORALL` or `BEEALL`

---

### B. Admin & Class Coordinators Portal (`/admin`)

| Name | Role | Email | Password | Assigned Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | Super Administrator | `admin@mentorbee.com` | `AdminPassword@123` | **ALL Classes & Audit Logs** |
| **ABIN M M** | Class Coordinator | `abin@mentorbee.com` | `AbinPassword@8th` | **8th Class** |
| **ABHIJITH M B** | Class Coordinator | `abhijith@mentorbee.com` | `AbhijithPassword@9th` | **9th Class** |
| **SREEHARI R** | Class Coordinator | `sreehari@mentorbee.com` | `SreehariPassword@10th` | **10th Class** |
| **PAVIN PAULSON** | Class Coordinator | `pavin@mentorbee.com` | `PavinPassword@11sci` | **11th Science** |
| **AKASH** | Class Coordinator | `akash@mentorbee.com` | `AkashPassword@11com` | **11th Commerce** |
| **MURALI** | Class Coordinator | `murali@mentorbee.com` | `MuraliPassword@12th` | **12th Science & 12th Commerce** |

---

## 🚀 3. Module-by-Module User Guide

### 📱 Module 1: Mentor Portal (`/` and `/mentor/login`)
Designed for fast, error-free meeting link retrieval on mobile and desktop.

1. **Access**: Navigate to the home URL `https://your-domain/` or `/mentor/login`.
2. **Login**:
   - Type your **Full Name**.
   - Select your **Assigned Class** (e.g. `10TH`, `11TH SCI`).
   - Enter the **Staff Passcode** and click **Access Dashboard**.
3. **Filtering & Searching**:
   - Filter by **Syllabus**: `All Syllabus`, `State Syllabus`, or `CBSE Syllabus`.
   - Filter by **Class**: Toggle between classes or view your assigned class.
   - Search by batch name or topic in the real-time search box.
4. **1-Click Actions**:
   - 📋 **Copy Formatted Message**: Copies the pre-formatted WhatsApp message ready to paste directly into WhatsApp groups.
   - 🔗 **Copy Zoom Link**: Copies the direct meeting URL to clipboard.
   - 🚀 **Join Meeting**: Opens the Zoom app or web browser to join directly.

---

### 🛠️ Module 2: Admin & Coordinator Dashboard (`/admin/dashboard`)

#### 1. Creating a Class Session
1. Log in at `/admin`.
2. In the **Create / Schedule Session** section:
   - **Step A: Smart Zoom Text Auto-Fill (Optional but Recommended)**:
     - Paste raw WhatsApp text containing the Zoom invite into the **"Paste Raw Zoom Text"** box.
     - Click **"Auto-Extract"**. The system will automatically extract and fill the Zoom URL, Meeting ID, and Passcode into the form.
   - **Step B: Select Batch & Class Details**:
     - Choose the **Class Category** and **Target Batch**.
     - Enter the **Subject / Topic** (e.g., *Physics - Thermodynamics*).
     - Select the **Date** and **Start Time** (IST).
   - **Step C: Publish**:
     - Click **"Publish Session"**.
     - The session is instantly saved and broadcasted to all connected mentors via WebSockets in real time.

#### 2. Managing Existing Sessions
- **Live Search & Filter**: Filter sessions by date, syllabus, and class category.
- **Edit Session**: Update link, topic, or timing on the fly.
- **Permanent Delete**: Remove outdated or cancelled sessions.

#### 3. Batch Management
- View all 106+ pre-loaded State and CBSE batches.
- Add new batches or update syllabus classifications anytime.

#### 4. Security & Audit Trail (Super Admin Only)
- Accessible only by Super Admin (`admin@mentorbee.com`).
- Live tracking of all mentor activity:
  - Timestamp
  - Staff / Mentor Name
  - Assigned Class
  - Action performed (`LOGIN`, `COPY_MESSAGE`, `COPY_LINK`, `JOIN_ZOOM`)
  - Target Batch & Session
  - IP Address

---

## ⚡ 4. Standard Broadcast Message Format

When mentors click **"Copy Formatted Message"**, the system generates the following clean, professional message:

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

## 📞 5. Support & Troubleshooting

- **Forgot Password?** Contact the Super Admin (`admin@mentorbee.com`) to reset coordinator credentials.
- **Passcode Rejected?** Ensure you are entering the correct staff passcode: `AGENTBEE0809` or your class-specific passcode.
- **Real-Time Sync**: If connection indicator shows disconnected, the system automatically attempts reconnection every 5 seconds.
