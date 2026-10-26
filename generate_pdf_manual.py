import base64
import os
import subprocess

def get_logo_base64():
    logo_path = os.path.join("app", "static", "img", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def generate_manual_html():
    logo_b64 = get_logo_base64()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MentorBee Eduverse — User & Operations Manual</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

        @page {{
            size: A4 portrait;
            margin: 18mm 16mm 18mm 16mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 9pt;
                color: #94a3b8;
            }}
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
            background-color: #ffffff;
            line-height: 1.55;
            font-size: 10pt;
            margin: 0;
            padding: 0;
        }}

        /* Typography */
        h1, h2, h3, h4, h5 {{
            color: #0f172a;
            font-weight: 800;
            line-height: 1.25;
            margin-top: 0;
        }}

        h1 {{ font-size: 22pt; margin-bottom: 6px; letter-spacing: -0.5px; }}
        h2 {{ 
            font-size: 14pt; 
            margin-top: 22pt; 
            margin-bottom: 10pt; 
            padding-bottom: 5pt;
            border-bottom: 2px solid #fef3c7;
            color: #b45309;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        h3 {{ font-size: 11.5pt; margin-top: 14pt; margin-bottom: 6pt; color: #1e293b; }}
        h4 {{ font-size: 10.5pt; margin-top: 10pt; margin-bottom: 4pt; color: #334155; }}

        p {{
            margin-top: 0;
            margin-bottom: 8pt;
            color: #334155;
        }}

        .page-break {{
            page-break-before: always;
        }}

        .no-break {{
            page-break-inside: avoid;
        }}

        /* Header / Cover banner */
        .cover-header {{
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #fde68a 100%);
            border: 1.5px solid #fcd34d;
            border-radius: 12pt;
            padding: 18pt 20pt;
            margin-bottom: 18pt;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo-img {{
            height: 48px;
            width: auto;
            object-fit: contain;
        }}

        .header-badge {{
            background-color: #f59e0b;
            color: #ffffff;
            font-size: 8pt;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            padding: 3pt 8pt;
            border-radius: 20pt;
            display: inline-block;
            margin-bottom: 6pt;
        }}

        .doc-title {{
            font-size: 19pt;
            font-weight: 800;
            color: #78350f;
            margin: 0 0 4pt 0;
            letter-spacing: -0.3px;
        }}

        .doc-subtitle {{
            font-size: 10pt;
            color: #92400e;
            font-weight: 600;
            margin: 0;
        }}

        /* Meta block */
        .meta-strip {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8pt;
            padding: 8pt 12pt;
            margin-bottom: 16pt;
            display: flex;
            justify-content: space-between;
            font-size: 8.5pt;
            color: #64748b;
        }}
        .meta-item strong {{
            color: #0f172a;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0 14pt 0;
            font-size: 9pt;
        }}

        th, td {{
            padding: 7pt 9pt;
            text-align: left;
            vertical-align: middle;
            border: 1px solid #e2e8f0;
        }}

        th {{
            background-color: #fffbeb;
            color: #78350f;
            font-weight: 700;
            font-size: 8.5pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #fde68a;
        }}

        tr:nth-child(even) {{
            background-color: #fcfcfd;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 2pt 6pt;
            border-radius: 4pt;
            font-size: 7.5pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .badge-cbse {{ background-color: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }}
        .badge-state {{ background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }}
        .badge-admin {{ background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
        .badge-pass {{ background-color: #f1f5f9; color: #0f172a; border: 1px solid #cbd5e1; font-family: 'JetBrains Mono', monospace; font-size: 8pt; }}
        .badge-active {{ background-color: #dcfce7; color: #166534; font-weight: 700; }}

        /* Cards & Callouts */
        .card {{
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8pt;
            padding: 10pt 12pt;
            margin-bottom: 10pt;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}

        .callout {{
            border-left: 4px solid #f59e0b;
            background-color: #fffbeb;
            border-radius: 0 8pt 8pt 0;
            padding: 9pt 12pt;
            margin: 10pt 0;
            font-size: 9pt;
        }}
        .callout-title {{
            font-weight: 800;
            color: #92400e;
            margin-bottom: 3pt;
            font-size: 9.5pt;
        }}

        .callout-info {{
            border-left-color: #3b82f6;
            background-color: #eff6ff;
        }}
        .callout-info .callout-title {{
            color: #1e40af;
        }}

        .callout-success {{
            border-left-color: #10b981;
            background-color: #ecfdf5;
        }}
        .callout-success .callout-title {{
            color: #065f46;
        }}

        /* Code block / formatted message */
        .code-box {{
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 8.2pt;
            padding: 10pt 12pt;
            border-radius: 6pt;
            border: 1px solid #334155;
            white-space: pre-wrap;
            line-height: 1.45;
            margin: 8pt 0 12pt 0;
        }}

        /* Feature grid */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10pt;
            margin: 8pt 0 12pt 0;
        }}

        .feature-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8pt;
            padding: 9pt 11pt;
        }}
        .feature-box h4 {{
            margin-top: 0;
            color: #78350f;
            display: flex;
            align-items: center;
            gap: 4pt;
        }}

        /* Step numbers */
        .step-list {{
            counter-reset: step-counter;
            list-style: none;
            padding-left: 0;
            margin: 8pt 0;
        }}
        .step-list > li {{
            position: relative;
            padding-left: 28pt;
            margin-bottom: 10pt;
        }}
        .step-list > li::before {{
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            top: 0;
            width: 18pt;
            height: 18pt;
            background-color: #f59e0b;
            color: #ffffff;
            font-weight: 800;
            font-size: 9pt;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            line-height: 18pt;
        }}

        .ui-element {{
            display: inline-block;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #334155;
            font-weight: 700;
            font-size: 8.5pt;
            padding: 1.5pt 5pt;
            border-radius: 4pt;
        }}

        .btn-ui {{
            display: inline-block;
            background: #fbbf24;
            color: #0f172a;
            font-weight: 800;
            font-size: 8.5pt;
            padding: 2pt 7pt;
            border-radius: 5pt;
            border: 1px solid #f59e0b;
        }}

        .btn-ui-secondary {{
            display: inline-block;
            background: #ffffff;
            color: #334155;
            font-weight: 700;
            font-size: 8.5pt;
            padding: 2pt 7pt;
            border-radius: 5pt;
            border: 1.5px solid #cbd5e1;
        }}

        .btn-ui-danger {{
            display: inline-block;
            background: #fef2f2;
            color: #b91c1c;
            font-weight: 700;
            font-size: 8.5pt;
            padding: 2pt 7pt;
            border-radius: 5pt;
            border: 1px solid #fecaca;
        }}

        .toc-list {{
            list-style: none;
            padding-left: 0;
            margin: 6pt 0;
            font-size: 9.5pt;
        }}
        .toc-list li {{
            padding: 4pt 0;
            border-bottom: 1px dashed #e2e8f0;
            display: flex;
            justify-content: space-between;
        }}
        .toc-list li a {{
            color: #1e293b;
            text-decoration: none;
            font-weight: 600;
        }}
        .toc-page {{
            color: #94a3b8;
            font-weight: 700;
        }}
    </style>
</head>
<body>

    <!-- Cover Page Banner -->
    <div class="cover-header">
        <div>
            <span class="header-badge">Official Documentation</span>
            <div class="doc-title">MentorBee Eduverse</div>
            <div class="doc-subtitle">Class Link Management & WhatsApp Broadcast System</div>
        </div>
        {f'<img src="{logo_b64}" class="logo-img" alt="MentorBee">' if logo_b64 else ''}
    </div>

    <div class="meta-strip">
        <div class="meta-item"><strong>Document Type:</strong> Complete Operations & User Manual</div>
        <div class="meta-item"><strong>Version:</strong> 2.0 (Production Release)</div>
        <div class="meta-item"><strong>Audience:</strong> Super Admin, Class Coordinators & Mentors</div>
    </div>

    <!-- Executive Summary -->
    <div class="callout callout-info no-break">
        <div class="callout-title">📖 About This Manual</div>
        This document provides a comprehensive, step-by-step functional guide for both <strong>Admin & Class Coordinators</strong> and <strong>Staff / Mentors</strong> of MentorBee Eduverse. It covers authentication, scheduling with Smart Zoom Auto-Parsing, 1-click WhatsApp message generation, WebSocket real-time synchronization, batch management, and the security audit trail.
    </div>

    <!-- Table of Contents -->
    <div class="card no-break">
        <h3 style="margin-top: 0; color: #78350f;">📑 Table of Contents</h3>
        <ul class="toc-list">
            <li><span><strong>1.</strong> System Architecture & Workflow</span> <span>Section 1</span></li>
            <li><span><strong>2.</strong> Access Control & Credentials Matrix</span> <span>Section 2</span></li>
            <li><span><strong>3.</strong> Admin & Coordinator Portal (Complete Breakdown)</span> <span>Section 3</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;3.1 Sessions Management & Smart Zoom AI Auto-Fill</span> <span>Section 3.1</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;3.2 Batch Catalog & Syllabus Configuration</span> <span>Section 3.2</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;3.3 Security & Access Audit Trail (Super Admin)</span> <span>Section 3.3</span></li>
            <li><span><strong>4.</strong> Mentor & Staff Portal (Complete Breakdown)</span> <span>Section 4</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;4.1 Mobile & Desktop Login Workflow</span> <span>Section 4.1</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;4.2 CBSE vs STATE Syllabus Switcher & Grade Filtering</span> <span>Section 4.2</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;4.3 1-Click WhatsApp Broadcast Copy & Zoom Meeting Launch</span> <span>Section 4.3</span></li>
            <li><span>&nbsp;&nbsp;&nbsp;&nbsp;4.4 Real-Time Background Synchronization Engine</span> <span>Section 4.4</span></li>
            <li><span><strong>5.</strong> Standard WhatsApp Broadcast Template Specifications</span> <span>Section 5</span></li>
            <li><span><strong>6.</strong> Operational FAQs & Troubleshooting Guide</span> <span>Section 6</span></li>
        </ul>
    </div>

    <!-- SECTION 1: System Overview & Architecture -->
    <h2>📌 1. System Architecture & Workflow</h2>
    <p>
        <strong>MentorBee Class Link Management System</strong> is engineered to eliminate manual link errors, delays, and WhatsApp formatting inconsistencies across 106+ educational batches spanning <strong>8th, 9th, 10th, 11th Science/Commerce, and 12th Science/Commerce</strong> (both State Syllabus and CBSE).
    </p>

    <div class="grid-2 no-break">
        <div class="feature-box">
            <h4>⚡ High-Speed Scheduling</h4>
            Coordinators paste raw WhatsApp meeting invites. The smart regex engine extracts the Zoom URL, Meeting ID, and Passcode in milliseconds.
        </div>
        <div class="feature-box">
            <h4>🔄 Real-Time WebSocket Sync</h4>
            Newly scheduled classes or link modifications reflect instantly across all active mentor dashboards without manual refresh.
        </div>
        <div class="feature-box">
            <h4>📱 Mobile-First Mentor UI</h4>
            Clean, high-contrast touch interface with 1-click WhatsApp message copying and direct Zoom deep-linking.
        </div>
        <div class="feature-box">
            <h4>🛡️ Security & Full Audit Trail</h4>
            Every login, message copy, link copy, and Zoom launch is timestamped with staff name, class scope, and IP address.
        </div>
    </div>

    <div class="callout callout-success no-break">
        <div class="callout-title">🔄 End-to-End Operational Lifecycle</div>
        <strong>Step 1:</strong> Faculty creates Zoom meeting &gt; <strong>Step 2:</strong> Coordinator pastes invite text into Admin Portal &gt; <strong>Step 3:</strong> System parses details and publishes session &gt; <strong>Step 4:</strong> WebSocket pushes update to Mentor Portals &gt; <strong>Step 5:</strong> Mentor taps "Copy Message" and dispatches to WhatsApp student groups.
    </div>

    <!-- SECTION 2: Access Control & Credentials Matrix -->
    <div class="page-break"></div>
    <h2>👥 2. User Roles & Credentials Reference Matrix</h2>

    <h3>A. Admin & Class Coordinator Accounts (`/admin`)</h3>
    <p>Access the administrative dashboard to schedule classes, manage batches, and monitor access.</p>

    <table class="no-break">
        <thead>
            <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Login Email</th>
                <th>Default Password</th>
                <th>Assigned Scope</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Super Admin</strong></td>
                <td><span class="badge badge-admin">Super Admin</span></td>
                <td><code>admin@mentorbee.com</code></td>
                <td><span class="badge badge-pass">AdminPassword@123</span></td>
                <td><strong>ALL Classes & Audit Logs</strong></td>
            </tr>
            <tr>
                <td><strong>ABIN M M</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>abin@mentorbee.com</code></td>
                <td><span class="badge badge-pass">AbinPassword@8th</span></td>
                <td><strong>8th Class (State & CBSE)</strong></td>
            </tr>
            <tr>
                <td><strong>ABHIJITH M B</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>abhijith@mentorbee.com</code></td>
                <td><span class="badge badge-pass">AbhijithPassword@9th</span></td>
                <td><strong>9th Class (State & CBSE)</strong></td>
            </tr>
            <tr>
                <td><strong>SREEHARI R</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>sreehari@mentorbee.com</code></td>
                <td><span class="badge badge-pass">SreehariPassword@10th</span></td>
                <td><strong>10th Class (State & CBSE)</strong></td>
            </tr>
            <tr>
                <td><strong>PAVIN PAULSON</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>pavin@mentorbee.com</code></td>
                <td><span class="badge badge-pass">PavinPassword@11sci</span></td>
                <td><strong>11th Science (State & CBSE)</strong></td>
            </tr>
            <tr>
                <td><strong>AKASH</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>akash@mentorbee.com</code></td>
                <td><span class="badge badge-pass">AkashPassword@11com</span></td>
                <td><strong>11th Commerce (State & CBSE)</strong></td>
            </tr>
            <tr>
                <td><strong>MURALI</strong></td>
                <td><span class="badge badge-admin">Coordinator</span></td>
                <td><code>murali@mentorbee.com</code></td>
                <td><span class="badge badge-pass">MuraliPassword@12th</span></td>
                <td><strong>12th Science & 12th Commerce</strong></td>
            </tr>
        </tbody>
    </table>

    <h3>B. Mentor & Staff Authentication Matrix (`/mentor/login` or `/`)</h3>
    <p>Mentors log in by typing their name, selecting their class, and entering an authorized staff verification passcode.</p>

    <table class="no-break">
        <thead>
            <tr>
                <th>Assigned Class</th>
                <th>Universal Master Passcode</th>
                <th>Class-Specific Passcodes</th>
                <th>Default View Filter</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>8th Class</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR8TH</span> / <span class="badge badge-pass">BEE8TH</span></td>
                <td>All 8th State & CBSE Batches</td>
            </tr>
            <tr>
                <td><strong>9th Class</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR9TH</span> / <span class="badge badge-pass">BEE9TH</span></td>
                <td>All 9th State & CBSE Batches</td>
            </tr>
            <tr>
                <td><strong>10th Class</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR10TH</span> / <span class="badge badge-pass">BEE10TH</span></td>
                <td>All 10th State & CBSE Batches</td>
            </tr>
            <tr>
                <td><strong>11th Science</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR11SCI</span> / <span class="badge badge-pass">BEE11SCI</span></td>
                <td>11th Science Batches</td>
            </tr>
            <tr>
                <td><strong>11th Commerce</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR11COM</span> / <span class="badge badge-pass">BEE11COM</span></td>
                <td>11th Commerce Batches</td>
            </tr>
            <tr>
                <td><strong>12th Science</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR12SCI</span> / <span class="badge badge-pass">BEE12SCI</span></td>
                <td>12th Science Batches</td>
            </tr>
            <tr>
                <td><strong>12th Commerce</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTOR12COM</span> / <span class="badge badge-pass">BEE12COM</span></td>
                <td>12th Commerce Batches</td>
            </tr>
            <tr>
                <td><strong>All Classes (Admin Mentor)</strong></td>
                <td><span class="badge badge-pass">AGENTBEE0809</span></td>
                <td><span class="badge badge-pass">MENTORALL</span> / <span class="badge badge-pass">BEEALL</span></td>
                <td>All Grades & Streams</td>
            </tr>
        </tbody>
    </table>

    <!-- SECTION 3: Admin & Coordinator Portal -->
    <div class="page-break"></div>
    <h2>🛠️ 3. Admin & Coordinator Portal (`/admin`)</h2>
    <p>
        The Administrative Console allows Super Admins and Class Coordinators to manage live sessions, batch catalogs, and audit logs.
    </p>

    <h3>3.1 Top Navigation & Identity Status</h3>
    <div class="card no-break">
        <ul>
            <li><strong>Logo & Home link</strong>: Quickly identify the platform and branding.</li>
            <li><strong>User Badge</strong>: Displays logged-in coordinator name with a green status indicator and their authorized class scope (e.g. <span class="badge badge-admin">COORD: 10TH</span> or <span class="badge badge-admin">SUPER ADMIN</span>).</li>
            <li><strong>Mentor Portal Shortcut (`↗`)</strong>: Opens the live mentor dashboard in a new tab for rapid testing.</li>
            <li><strong>Logout Button</strong>: Destroys session token and returns securely to the login portal.</li>
        </ul>
    </div>

    <h3>3.2 Tab 1: Sessions Management</h3>
    <p>The primary command center for scheduling and broadcasting Zoom sessions.</p>

    <div class="callout no-break">
        <div class="callout-title">⚡ How to Create a Class Session (Step-by-Step)</div>
        <ol class="step-list">
            <li>
                <strong>Open Create Modal</strong>: Click the golden <span class="btn-ui">+ Create Session</span> button in the top right.
            </li>
            <li>
                <strong>Smart Zoom Paste Auto-Fill (Recommended)</strong>:<br>
                Paste the raw WhatsApp text received from the teacher into the <span class="ui-element">⚡ Quick Zoom Paste Auto-Fill</span> textarea.<br>
                Click <span class="btn-ui">Auto Parse Link &amp; Credentials</span>. The system instantly extracts the Zoom URL, Meeting ID, and Passcode and fills them into their respective fields.
            </li>
            <li>
                <strong>Select Class Stream &amp; Batch</strong>:<br>
                Select the <strong>Assigned Class Stream</strong> (e.g. <em>10th Class</em>).<br>
                Optionally filter by <strong>Syllabus Filter</strong> (<em>CBSE</em> or <em>STATE</em>).<br>
                Select the exact target <strong>Batch</strong> from the filtered dropdown list.
            </li>
            <li>
                <strong>Enter Class Topic &amp; Schedule</strong>:<br>
                Type the <strong>Class Topic / Subject</strong> (e.g. <em>Mathematics - Quadratic Equations</em>).<br>
                Set the <strong>Date</strong> (defaults to today) and <strong>Start Time</strong> (IST).
            </li>
            <li>
                <strong>Publish &amp; Broadcast</strong>:<br>
                Click <span class="btn-ui">Save &amp; Broadcast Session</span>.<br>
                The session is committed to the database, formatted messages are pre-computed, and an instant WebSocket broadcast triggers updates across all mentor dashboards.
            </li>
        </ol>
    </div>

    <div class="grid-2 no-break">
        <div class="feature-box">
            <h4>✏️ Editing Sessions</h4>
            Click <span class="btn-ui-secondary">Edit</span> on any session row. You can modify the topic, link, time, or passcode on the fly. All changes are logged in the version change history and instantly updated for mentors.
        </div>
        <div class="feature-box">
            <h4>🗑️ Deleting Sessions</h4>
            Click <span class="btn-ui-danger">Delete</span> on any session row. A confirmation prompt prevents accidental deletion. Once confirmed, the session is removed permanently and cleared from mentor views.
        </div>
    </div>

    <!-- SECTION 3.2 & 3.3 -->
    <div class="page-break"></div>
    <h3>3.3 Tab 2: Batches Management</h3>
    <p>
        Maintains the institution's catalog of all active academic batches.
    </p>

    <div class="card no-break">
        <h4>Key Functions in Batches Tab</h4>
        <ul>
            <li><strong>Batch Inventory</strong>: Displays Batch ID, Assigned Class Category, Full Batch Name, Syllabus (<span class="badge badge-cbse">CBSE</span> or <span class="badge badge-state">STATE</span>), and Active Status.</li>
            <li><strong>Class Scope Isolation</strong>: Coordinators only view batches matching their assigned grades. Super Admin views all 106+ batches.</li>
            <li><strong>Create New Batch</strong>: Click <span class="btn-ui">+ Create Batch</span>, enter the name (e.g. <em>10TH STATE EVNG KL BATCH</em>). The system automatically infers syllabus and grade categories from the naming pattern.</li>
            <li><strong>Edit Batch</strong>: Rename or update batch metadata whenever class structures evolve.</li>
        </ul>
    </div>

    <h3>3.4 Tab 3: Security & Access Audit Trail (Super Admin Exclusive)</h3>
    <p>
        A tamper-evident, real-time activity log tracking mentor interactions across all classes.
    </p>

    <table class="no-break">
        <thead>
            <tr>
                <th>Logged Event</th>
                <th>Action Badge</th>
                <th>Description &amp; Compliance Value</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Mentor Login</strong></td>
                <td><span class="badge badge-admin">🔑 Staff Login</span></td>
                <td>Records staff member name, class scope, timestamp, and IP address upon entering the system.</td>
            </tr>
            <tr>
                <td><strong>Copy Broadcast Message</strong></td>
                <td><span class="badge badge-active">✓ Copied Message</span></td>
                <td>Logs every instance of a mentor copying the WhatsApp broadcast message for a specific batch.</td>
            </tr>
            <tr>
                <td><strong>Copy Direct Zoom Link</strong></td>
                <td><span class="badge badge-active">✓ Copied Link</span></td>
                <td>Tracks direct URL copies for audit verification.</td>
            </tr>
            <tr>
                <td><strong>Launch Zoom Meeting</strong></td>
                <td><span class="badge badge-cbse">⚡ Launched Zoom</span></td>
                <td>Logs when a mentor clicks "Join Zoom" to enter the live room directly.</td>
            </tr>
        </tbody>
    </table>

    <div class="callout callout-info no-break">
        <div class="callout-title">🔍 Refreshing Audit Logs</div>
        Click <span class="btn-ui">↻ Refresh Logs</span> to pull the latest 100 access logs in real time. Super Admins can verify which staff member dispatched the link to student groups and at what exact second.
    </div>

    <!-- SECTION 4: Mentor & Staff Portal -->
    <div class="page-break"></div>
    <h2>📱 4. Mentor & Staff Portal (`/` and `/mentor/login`)</h2>
    <p>
        The Mentor Portal is designed for maximum speed and simplicity on mobile devices (smartphones, tablets) and desktops.
    </p>

    <h3>4.1 Mobile & Desktop Login Workflow</h3>
    <ol class="step-list no-break">
        <li>Navigate to the homepage <code>https://your-domain/</code> or <code>/mentor/login</code>.</li>
        <li>Enter your <strong>Full Staff Name</strong> (e.g., <em>ANJALI</em>, <em>RAHUL</em>).</li>
        <li>Select your <strong>Assigned Class</strong> from the dropdown (e.g., <em>10TH</em>, <em>11TH SCI</em>).</li>
        <li>Enter the authorized <strong>Staff Verification Passcode</strong> (<span class="badge badge-pass">AGENTBEE0809</span> or class passcode).</li>
        <li>Tap <span class="btn-ui">Access Dashboard</span>. Your session is securely authenticated for 24 hours.</li>
    </ol>

    <h3>4.2 Dashboard Layout & Navigation Controls</h3>
    <div class="grid-2 no-break">
        <div class="feature-box">
            <h4>1. Primary Syllabus Switcher</h4>
            Top-level toggle between <span class="badge badge-cbse">CBSE</span> and <span class="badge badge-state">STATE</span> syllabuses. Includes real-time pill badges showing the exact number of active classes in each syllabus.
        </div>
        <div class="feature-box">
            <h4>2. Time Sub-Tabs</h4>
            Toggle between <strong>Today's Classes</strong> (active classes for the current date) and <strong>Upcoming</strong> (classes scheduled for future dates).
        </div>
    </div>

    <div class="card no-break">
        <h4>3. Grade &amp; Scope Filter Chips</h4>
        <ul>
            <li><strong>Class-Scoped Mentors</strong>: Displays an active chip locked to the mentor's assigned class (e.g. <em>Class 10TH</em>) showing all State and CBSE batches.</li>
            <li><strong>Multi-Class Mentors</strong>: Interactive filter bar allowing seamless switching between <em>All Classes</em>, <em>8th</em>, <em>9th</em>, <em>10th</em>, <em>11th Sci</em>, <em>11th Com</em>, <em>12th Sci</em>, and <em>12th Com</em>.</li>
        </ul>
    </div>

    <h3>4.3 Class Session Card & 1-Click Actions</h3>
    <p>Each class session is displayed in a dedicated, high-contrast visual card:</p>

    <div class="card no-break" style="border: 1.5px solid #fcd34d; background: #fffdf5;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6pt;">
            <div>
                <span class="badge badge-cbse">CBSE</span>
                <span class="badge badge-admin">10TH</span>
                <span class="badge" style="background:#fef3c7; color:#92400e; font-weight:800;">10TH CBSE EVNG KL BATCH</span>
            </div>
            <span style="font-size: 8pt; color: #64748b; font-weight: 600;">🕒 UPDATED 06:45 PM</span>
        </div>
        <h3 style="margin: 4pt 0; font-size: 13pt; color: #0f172a; text-transform: uppercase;">MATHEMATICS — QUADRATIC EQUATIONS</h3>
        <p style="font-size: 9pt; color: #475569; font-weight: 600; margin-bottom: 8pt;">⏰ 07:00 PM IST</p>
        <div style="display: flex; gap: 8pt;">
            <div style="flex: 1; text-align: center; background: #fbbf24; color: #0f172a; padding: 6pt; border-radius: 6pt; font-weight: 800; font-size: 8.5pt;">
                📋 Copy Message
            </div>
            <div style="flex: 1; text-align: center; background: #ffffff; color: #1e293b; border: 1.5px solid #fcd34d; padding: 6pt; border-radius: 6pt; font-weight: 800; font-size: 8.5pt;">
                🚀 Join Zoom
            </div>
        </div>
    </div>

    <div class="grid-2 no-break">
        <div class="feature-box">
            <h4>📋 Copy Message Button</h4>
            1-tap copies the pre-formatted WhatsApp message ready to paste directly into student WhatsApp groups. The button turns green (<span class="badge badge-active">✓ Copied!</span>) with an animated toast notification.
        </div>
        <div class="feature-box">
            <h4>🚀 Join Zoom Button</h4>
            Launches the Zoom application or browser directly into the live meeting room with meeting ID and passcode automatically applied.
        </div>
    </div>

    <!-- SECTION 5: WhatsApp Broadcast Message Format -->
    <div class="page-break"></div>
    <h2>⚡ 5. Standard WhatsApp Broadcast Template</h2>
    <p>
        When mentors click <strong>"Copy Message"</strong>, the system generates a clean, professional, standardized message formatted specifically for WhatsApp readability:
    </p>

    <div class="code-box no-break">*MENTORBEE EDUVERSE*
*EXAM KILLER 4.0 - REVISE*
*10TH CBSE KL REV-2 BATCH (2)* 
-----------------------------------
*TOPIC : CHEMISTRY*
*DATE : OCTOBER 26, 2026*
*TIME : 06:00 PM IST*


*Join Zoom Meeting*
https://us06web.zoom.us/j/89982457863?pwd=cDv1PpMA7zYEjbQ3kVgZGqbbwakqi3.1

*Meeting ID: 899 8245 7863*
*Passcode: mentorbee*</div>

    <div class="callout callout-success no-break">
        <div class="callout-title">✨ Key Formatting Features</div>
        <ul>
            <li><strong>Clear Institution &amp; Batch Header</strong>: High-visibility asterisks for WhatsApp bold text formatting.</li>
            <li><strong>Separation Bar</strong>: Clean divider line separating metadata from connection details.</li>
            <li><strong>Explicit IST Time Tag</strong>: Prevents timezone ambiguity for students across regions.</li>
            <li><strong>Direct Clickable URL</strong>: Zoom deep link with embedded token for 1-tap entry.</li>
            <li><strong>Explicit ID &amp; Passcode</strong>: Fallback credentials for manual Zoom room entry.</li>
        </ul>
    </div>

    <!-- SECTION 6: Troubleshooting & FAQs -->
    <h2>📞 6. Operational Troubleshooting & FAQs</h2>

    <div class="card no-break">
        <h4>Q1: Passcode rejected during Mentor Login?</h4>
        <p><strong>Solution:</strong> Ensure you are using the Master Staff Passcode <code>AGENTBEE0809</code> or the class-specific passcode matching your selected class. Passcodes are case-insensitive.</p>
    </div>

    <div class="card no-break">
        <h4>Q2: No batches appear in the "Select Batch" dropdown when creating a session?</h4>
        <p><strong>Solution:</strong> Check the <strong>Syllabus Filter</strong> in the creation modal. If it is set to "CBSE" and you selected an 11th Commerce class with only State batches, switch the filter to "All Syllabuses".</p>
    </div>

    <div class="card no-break">
        <h4>Q3: Zoom Auto-Extractor fails to parse invite text?</h4>
        <p><strong>Solution:</strong> Verify that the pasted WhatsApp message contains a valid <code>https://zoom.us/j/...</code> URL. If the message only has Meeting ID and Passcode, enter the values manually into the corresponding fields.</p>
    </div>

    <div class="card no-break">
        <h4>Q4: How does real-time synchronization work if a link changes last minute?</h4>
        <p><strong>Solution:</strong> When a coordinator edits a session, the backend broadcasts a WebSocket message and mentor devices automatically reload data within milliseconds. In addition, the mentor portal runs an automatic background poll every 4 seconds as a fail-safe.</p>
    </div>

    <!-- Signoff block -->
    <div class="callout callout-info no-break" style="margin-top: 20pt; text-align: center;">
        <p style="font-weight: 800; color: #1e40af; margin-bottom: 2pt;">MentorBee Eduverse Operations Team</p>
        <p style="font-size: 8.5pt; color: #475569; margin: 0;">For credential resets, technical inquiries, or institutional batch additions, contact: <strong>admin@mentorbee.com</strong></p>
    </div>

</body>
</html>"""
    return html

def main():
    print("Generating HTML User Manual...")
    html_content = generate_manual_html()
    html_file = os.path.abspath("USER_MANUAL.html")
    pdf_file = os.path.abspath("MentorBee_User_Manual.pdf")
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote HTML manual to: {html_file}")

    print("Compiling HTML to PDF using Headless Edge...")
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    
    browser_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            browser_exe = p
            break
            
    if not browser_exe:
        print("Error: Could not find Edge or Chrome executable.")
        return

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(pdf_file):
        print(f"SUCCESS: PDF generated successfully at: {pdf_file}")
        print(f"PDF File size: {os.path.getsize(pdf_file)} bytes")
    else:
        print(f"Error generating PDF: {result.stderr}")

if __name__ == "__main__":
    main()
