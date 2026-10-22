import os
import subprocess
import base64

def get_logo_base64():
    logo_path = os.path.join("app", "static", "img", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def build_mentor_guide_html():
    logo_b64 = get_logo_base64()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MentorBee Eduverse — Mentor Dashboard Operational Guide</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

        @page {{
            size: A4 portrait;
            margin: 16mm 16mm 16mm 16mm;
            @bottom-right {{
                content: "Page " counter(page);
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 8.5pt;
                color: #94a3b8;
                font-weight: 600;
            }}
            @bottom-left {{
                content: "MentorBee Eduverse • Confidential Operations Guide";
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 8.5pt;
                color: #94a3b8;
                font-weight: 500;
            }}
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
            background-color: #ffffff;
            line-height: 1.5;
            font-size: 9.5pt;
            margin: 0;
            padding: 0;
        }}

        /* Header */
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 12pt;
            border-bottom: 2.5px solid #f59e0b;
            margin-bottom: 16pt;
        }}
        .header-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .header-logo {{
            height: 44px;
            width: auto;
            object-fit: contain;
        }}
        .header-title-block h1 {{
            font-size: 16pt;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.3px;
        }}
        .header-title-block p {{
            font-size: 9pt;
            color: #b45309;
            font-weight: 700;
            margin: 2px 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .header-badge {{
            background: #fffbeb;
            border: 1px solid #fcd34d;
            color: #92400e;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 8pt;
            font-weight: 800;
            text-transform: uppercase;
        }}

        /* Section Headings */
        h2 {{
            font-size: 12pt;
            font-weight: 800;
            color: #92400e;
            background: #fffbeb;
            padding: 6pt 10pt;
            border-left: 4px solid #f59e0b;
            border-radius: 4px;
            margin-top: 16pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 10.5pt;
            font-weight: 700;
            color: #0f172a;
            margin-top: 10pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 6pt;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            margin: 8pt 0 12pt 0;
            page-break-inside: avoid;
        }}
        th {{
            background-color: #f8fafc;
            color: #334155;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 7.5pt;
            letter-spacing: 0.5px;
            padding: 6pt 8pt;
            border: 1px solid #e2e8f0;
            text-align: left;
        }}
        td {{
            padding: 6pt 8pt;
            border: 1px solid #e2e8f0;
            color: #1e293b;
        }}
        tr:nth-child(even) {{
            background-color: #fafaf9;
        }}

        /* Callout Alerts */
        .alert {{
            padding: 8pt 12pt;
            border-radius: 8pt;
            margin: 10pt 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        .alert-amber {{
            background-color: #fffbeb;
            border: 1px solid #fcd34d;
            border-left: 4px solid #f59e0b;
            color: #92400e;
        }}
        .alert-danger {{
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            border-left: 4px solid #ef4444;
            color: #991b1b;
        }}
        .alert-blue {{
            background-color: #eff6ff;
            border: 1px solid #bfdbfe;
            border-left: 4px solid #3b82f6;
            color: #1e40af;
        }}
        .alert-title {{
            font-weight: 800;
            font-size: 9.5pt;
            margin-bottom: 3pt;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        /* Code / Template Preview */
        pre, code {{
            font-family: 'JetBrains Mono', monospace;
        }}
        .template-box {{
            background-color: #0f172a;
            color: #e2e8f0;
            border-radius: 6pt;
            padding: 10pt;
            font-size: 8pt;
            line-height: 1.45;
            margin: 8pt 0;
            border: 1px solid #334155;
            page-break-inside: avoid;
        }}

        /* Mockup Visual Elements */
        .mockup-bar {{
            background: #f8fafc;
            border: 1.5px solid #cbd5e1;
            border-radius: 8px;
            padding: 6pt 10pt;
            font-weight: 600;
            font-size: 8.5pt;
            color: #64748b;
            margin: 6pt 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .card-diagram {{
            border: 1.5px solid #fde68a;
            background: #ffffff;
            border-radius: 8pt;
            padding: 8pt 10pt;
            margin: 8pt 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            page-break-inside: avoid;
        }}
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5pt;
        }}
        .badge-cbse {{
            background: #eff6ff;
            color: #1e40af;
            font-weight: 800;
            font-size: 7.5pt;
            padding: 2px 6px;
            border-radius: 999px;
            border: 1px solid #bfdbfe;
        }}
        .badge-updated {{
            background: #f1f5f9;
            color: #475569;
            font-weight: 700;
            font-size: 7.5pt;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}
        .card-actions {{
            display: flex;
            gap: 8px;
            margin-top: 6pt;
        }}
        .btn-mock-copy {{
            background: #f59e0b;
            color: #0f172a;
            font-weight: 700;
            font-size: 8pt;
            padding: 4pt 8pt;
            border-radius: 6px;
            display: inline-block;
        }}
        .btn-mock-zoom {{
            background: #ffffff;
            color: #0f172a;
            font-weight: 700;
            font-size: 8pt;
            padding: 4pt 8pt;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            display: inline-block;
        }}

        /* Lists */
        ul, ol {{
            margin-top: 2pt;
            margin-bottom: 6pt;
            padding-left: 18pt;
        }}
        li {{
            margin-bottom: 3pt;
        }}

        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>

    <!-- Header Block -->
    <div class="header">
        <div class="header-brand">
            {'<img src="' + logo_b64 + '" class="header-logo" alt="MentorBee Logo">' if logo_b64 else ''}
            <div class="header-title-block">
                <h1>Mentor Dashboard Operations Guide</h1>
                <p>Live Class Link Access, Search, Filtering & Security Protocol</p>
            </div>
        </div>
        <div class="header-badge">Official Staff SOP</div>
    </div>

    <!-- Alert: Mandatory Audit -->
    <div class="alert alert-amber">
        <div class="alert-title">🔒 Mandatory Staff Accountability & Real-Time Security Notice</div>
        Every login, Zoom launch, link copy, and broadcast message generation is <strong>actively tracked and recorded</strong> in the Super Admin Audit Trail with your <strong>Full Name, Timestamp, and IP Address</strong>. Treat all meeting links with strict confidentiality.
    </div>

    <!-- 1. Authentication -->
    <h2>1. Portal Access & Universal Authentication</h2>
    <p>Staff members access the live session repository by navigating to <code>/mentor/login</code> or the platform home page (<code>/</code>).</p>
    
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Login Field</th>
                <th style="width: 25%;">Required Input</th>
                <th>Security & Operational Purpose</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Your Full Name</strong></td>
                <td><code style="color: #b45309;">Staff Official Name</code></td>
                <td><strong>Mandatory.</strong> Identifies the exact mentor responsible for sharing links. Submissions with empty names are blocked by the system.</td>
            </tr>
            <tr>
                <td><strong>Username</strong></td>
                <td><code>mentor</code></td>
                <td>Common staff authentication username.</td>
            </tr>
            <tr>
                <td><strong>Password</strong></td>
                <td><code>agentBEE</code></td>
                <td>Common mentor access password (case-sensitive). Not displayed on screen for protection against over-the-shoulder viewing.</td>
            </tr>
            <tr>
                <td><strong>Access Scope</strong></td>
                <td><strong>Universal (All Classes)</strong></td>
                <td>Unlocks all 106+ batches across both State & CBSE syllabuses without separate logins.</td>
            </tr>
        </tbody>
    </table>

    <!-- 2. Search -->
    <h2>2. How to Search for Classes Instantly</h2>
    <p>The dashboard includes a high-performance <strong>Real-Time Search Bar</strong> located immediately beneath the primary syllabus switcher:</p>
    
    <div class="mockup-bar">
        <span>🔍 Search by topic, batch name, subject, or time...</span>
        <span style="font-weight: 800; color: #ef4444; font-size: 11pt;">&times;</span>
    </div>

    <ul>
        <li><strong>Batch Search:</strong> Type any part of the batch name (e.g., <code>10TH CBSE</code>, <code>KL BATCH</code>, <code>EVNG</code>, <code>STATE ONLINE</code>).</li>
        <li><strong>Subject & Topic Search:</strong> Type <code>Physics</code>, <code>Mathematics</code>, <code>Quadratic Equations</code>, <code>Organic Chemistry</code>, etc.</li>
        <li><strong>Time Search:</strong> Type <code>07:00</code>, <code>PM</code>, <code>08:30 AM</code> to quickly locate classes starting at a specific time.</li>
        <li><strong>Clearing Search:</strong> Tap the red <strong><code>&times;</code></strong> button on the right edge of the input to instantly reset the filter and display all classes.</li>
    </ul>

    <!-- 3. Filtering -->
    <h2>3. How to Filter Classes by Syllabus, Grade & Date</h2>
    <p>To navigate 100+ batches effortlessly, use the two-tier hierarchical filter system:</p>

    <h3>Tier 1: CBSE vs. STATE vs. EXAM KILLER Switcher</h3>
    <p>Use the prominent three-way switcher at the top of the interface:</p>
    <ul>
        <li><strong>CBSE Tab (Blue Dot):</strong> Filters the view to all CBSE curriculum classes with a live badge showing total count.</li>
        <li><strong>STATE Tab (Green Dot):</strong> Filters the view to all Kerala State Board curriculum classes with live count.</li>
        <li><strong>⚡ EXAM KILLER Tab (Rose Dot):</strong> Dedicated section for high-intensity Exam Killer crash courses, model exams, and question discussion sessions, kept strictly separate from regular daily classes.</li>
    </ul>


    <h3>Tier 2: Class / Grade Chips (Inside Syllabus)</h3>
    <p>Within your selected syllabus, tap any of the grade chips to view standard-specific sessions:</p>
    
    <table>
        <thead>
            <tr>
                <th>Filter Chip</th>
                <th>Standard Scope</th>
                <th>Target Streams</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>All Classes</strong></td>
                <td>Grades 8 through 12</td>
                <td>Comprehensive view of all active sessions</td>
            </tr>
            <tr>
                <td><strong>8th</strong></td>
                <td>8th Standard</td>
                <td>All 8th State & CBSE batches</td>
            </tr>
            <tr>
                <td><strong>9th</strong></td>
                <td>9th Standard</td>
                <td>All 9th State & CBSE batches</td>
            </tr>
            <tr>
                <td><strong>10th</strong></td>
                <td>10th Standard</td>
                <td>All 10th State & CBSE batches (Morning & Evening)</td>
            </tr>
            <tr>
                <td><strong>11th Sci</strong></td>
                <td>11th Science</td>
                <td>Physics, Chemistry, Mathematics, Biology</td>
            </tr>
            <tr>
                <td><strong>11th Com</strong></td>
                <td>11th Commerce</td>
                <td>Accountancy, Economics, Business Studies</td>
            </tr>
            <tr>
                <td><strong>12th Sci</strong></td>
                <td>12th Science</td>
                <td>Physics, Chemistry, Mathematics, Biology</td>
            </tr>
            <tr>
                <td><strong>12th Com</strong></td>
                <td>12th Commerce</td>
                <td>Accountancy, Economics, Business Studies</td>
            </tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <!-- 4. Checking Latest Changed ID / Timings -->
    <h2>4. How to Verify the Latest Changed ID & Timestamps</h2>
    <p>Online schedules often experience last-minute link updates, studio swaps, or emergency teacher replacements. The platform provides real-time verification indicators so mentors never broadcast outdated links.</p>

    <div class="card-diagram">
        <div class="card-top">
            <div>
                <span class="badge-cbse">CBSE</span>
                <span style="font-weight: 800; font-size: 8pt; margin-left: 4px;">10TH CBSE EVNG KL BATCH</span>
            </div>
            <span class="badge-updated">🕒 UPDATED 06:48 PM</span>
        </div>
        <div style="font-weight: 800; font-size: 10pt; color: #0f172a; margin-top: 4px;">
            MATHEMATICS - QUADRATIC EQUATIONS
        </div>
        <div style="font-size: 8.5pt; color: #64748b; margin-top: 2px;">
            🕒 07:00 PM IST
        </div>
        <div class="card-actions">
            <span class="btn-mock-copy">📋 Copy Message</span>
            <span class="btn-mock-zoom">🚀 Join Zoom</span>
        </div>
    </div>

    <h3>Verification Rules for Mentors:</h3>
    <ol>
        <li><strong>Inspect the <code>UPDATED [Time]</code> Badge:</strong> Every card indicates the exact time the link or topic was last edited by a coordinator (e.g., <code>UPDATED 06:48 PM</code>).</li>
        <li><strong>Live WebSocket Synchronization:</strong> If a coordinator changes a Zoom link while you have the dashboard open, your screen updates automatically within milliseconds.</li>
        <li><strong>4-Second Fallback Polling:</strong> The application automatically queries the server every 4 seconds to guarantee zero lag, even on unstable mobile connections.</li>
        <li><strong>Pre-Broadcast Golden Rule:</strong> If coordinators announce a link update in staff channels, locate the card, check that the <code>UPDATED</code> badge shows the recent time, and tap <strong>Copy Message</strong> to fetch the fresh credentials.</li>
    </ol>

    <!-- 5. 1-Click WhatsApp Broadcast -->
    <h2>5. 1-Click WhatsApp Broadcast Message Generation</h2>
    <p>When you tap <strong><code>Copy Message</code></strong>, the system formats the standardized WhatsApp text and copies it to your clipboard with a green <strong><code>✓ Copied!</code></strong> visual confirmation.</p>

    <div class="template-box">
*MENTORBEE EDUVERSE*<br>
*10TH CBSE EVNG KL BATCH*<br>
---------------------------------------<br>
*TOPIC : MATHEMATICS - QUADRATIC EQUATIONS*<br>
*DATE : AUGUST 21, 2026*<br>
*TIME : 07:00 PM IST*<br>
<br>
*Join Zoom Meeting*<br>
https://zoom.us/j/99887766554?pwd=samplepassword<br>
<br>
*Meeting ID: 998 8776 6554*<br>
*Passcode: 123456*
    </div>

    <!-- 6. Critical Security Warning -->
    <h2>6. 🚨 CRITICAL SECURITY PROTOCOL: ID MIS-SHARING & AUDIT MONITORING</h2>

    <div class="alert alert-danger">
        <div class="alert-title">⚠️ ZERO-TOLERANCE SECURITY & DISCIPLINARY POLICY</div>
        <strong>EVERY SINGLE LINK COPY, MESSAGE GENERATION, AND ZOOM ACCESS IS MONITORED.</strong><br>
        The Super Admin Console maintains an unalterable audit log displaying:
        <ul style="margin-top: 4px; margin-bottom: 4px;">
            <li><strong>Mentor Full Name</strong> (entered at login)</li>
            <li><strong>Batch Name & Session Topic</strong> accessed</li>
            <li><strong>Exact Action:</strong> <code>✓ Copied Message</code>, <code>✓ Copied Link</code>, or <code>⚡ Launched Zoom</code></li>
            <li><strong>Exact Timestamp</strong> (to the second) &amp; <strong>IP Address</strong></li>
        </ul>
    </div>

    <h3>Strict Rules on Link Distribution:</h3>
    <ul>
        <li><strong>NEVER Cross-Post Links Between Batches:</strong> Sending an 8th State link into an 8th CBSE broadcast group causes severe disruption, confusion, and unauthorized student entry. Always verify the Batch Header before sending.</li>
        <li><strong>NEVER Share Unofficial or Personal Links:</strong> Only broadcast links generated through this official portal.</li>
        <li><strong>DO NOT Disclose Staff Passwords:</strong> The password <code>agentBEE</code> is strictly confidential to MentorBee staff and must never be shared with students or parents.</li>
        <li><strong>Full Accountability:</strong> When link mis-sharing occurs, Super Admin cross-references the broadcast time against the Security Audit Log to identify the responsible mentor. Negligence will result in immediate administrative action.</li>
    </ul>

    <!-- 7. Support -->
    <h2>7. Administrative & Technical Support</h2>
    <p>For urgent scheduling issues, link corrections, or coordinator escalations:</p>
    <ul>
        <li><strong>Super Administrator:</strong> <code>admin@mentorbee.com</code></li>
        <li><strong>Class Coordinators:</strong> Contact your grade coordinator (Abin, Abhijith, Sreehari, Pavin, Akash, Murali).</li>
    </ul>

</body>
</html>
"""
    return html

def main():
    html_file = os.path.abspath("MENTOR_DASHBOARD_GUIDE.html")
    pdf_file = os.path.abspath("Mentor_Dashboard_Guide.pdf")

    print("Generating HTML content for Mentor Dashboard Guide...")
    html_content = build_mentor_guide_html()
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote HTML guide to: {html_file}")

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
