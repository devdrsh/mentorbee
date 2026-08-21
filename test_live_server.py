import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def make_request(path, method="GET", data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {
        "User-Agent": "MentorBeeTest/1.0"
    }
    encoded_data = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        encoded_data = json.dumps(data).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            try:
                return response.status, json.loads(res_body)
            except Exception:
                return response.status, res_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, err_body

def run_tests():
    print("=" * 70)
    print("COMPREHENSIVE LIVE API & FEATURE TEST SUITE")
    print("=" * 70)

    # 1. Test Static & HTML pages
    for path in ["/", "/mentor/login", "/admin", "/admin/dashboard"]:
        status, body = make_request(path)
        print(f"[HTML] GET {path:20} -> Status: {status} (Length: {len(body)})")
        assert status == 200, f"Failed GET {path}"

    # 2. Test Mentor Logins (All Classes with master & class-specific passcodes)
    mentor_cases = [
        ("Rahul Sharma", "8TH", "AGENTBEE0809", True),
        ("Ananya Iyer", "9TH", "MENTOR9TH", True),
        ("Karthik Raj", "10TH", "BEE10TH", True),
        ("Sneha Nair", "11TH SCI", "MENTOR11SCI", True),
        ("Arjun V", "11TH COM", "MENTOR11COM", True),
        ("Divya Menon", "12TH SCI", "MENTOR12SCI", True),
        ("Vishnu Prasad", "12TH COM", "MENTOR12COM", True),
        ("Principal Admin", "ALL", "AGENTBEE0809", True),
        ("Invalid User", "8TH", "WRONG_PASS", False),
    ]

    print("\n--- Testing Mentor Logins & Token Generation ---")
    active_mentor_tokens = {}
    for name, assigned_class, passcode, should_pass in mentor_cases:
        status, data = make_request("/api/mentor/login", method="POST", data={
            "name": name,
            "assigned_class": assigned_class,
            "passcode": passcode
        })
        if should_pass:
            assert status == 200, f"Expected 200 for {name} ({assigned_class}), got {status}: {data}"
            token = data["access_token"]
            active_mentor_tokens[assigned_class] = token
            print(f"  [PASS] Mentor '{name}' ({assigned_class}) -> Login OK (Token granted)")
        else:
            assert status == 401, f"Expected 401 for bad passcode, got {status}"
            print(f"  [PASS] Invalid passcode rejection -> Status: {status} ({data.get('detail')})")

    # 3. Test Mentor Action Logging
    print("\n--- Testing Mentor Action Logging ---")
    status, res = make_request("/api/mentor/log-action", method="POST", token=active_mentor_tokens["8TH"], data={
        "action": "COPY_MESSAGE",
        "session_id": 1,
        "batch_name": "8TH STATE ONLINE BATCH",
        "details": "Mentor copied WhatsApp broadcast template"
    })
    assert status == 200, f"Expected 200 for mentor action log, got {status}: {res}"
    print(f"  [PASS] Action COPY_MESSAGE logged successfully")

    status, res = make_request("/api/mentor/log-action", method="POST", token=active_mentor_tokens["10TH"], data={
        "action": "COPY_LINK",
        "session_id": 2,
        "batch_name": "10TH CBSE EVNG KL BATCH",
        "details": "Mentor copied direct Zoom URL"
    })
    assert status == 200
    print(f"  [PASS] Action COPY_LINK logged successfully")

    # 4. Test Coordinator & Admin Logins
    admins = [
        ("Super Admin", "admin@mentorbee.com", "AdminPassword@123", "SUPER_ADMIN", "ALL"),
        ("ABIN M M (8th)", "abin@mentorbee.com", "AbinPassword@8th", "COORDINATOR", "8TH"),
        ("ABHIJITH M B (9th)", "abhijith@mentorbee.com", "AbhijithPassword@9th", "COORDINATOR", "9TH"),
        ("SREEHARI R (10th)", "sreehari@mentorbee.com", "SreehariPassword@10th", "COORDINATOR", "10TH"),
        ("PAVIN PAULSON (11th Sci)", "pavin@mentorbee.com", "PavinPassword@11sci", "COORDINATOR", "11TH SCI"),
        ("AKASH (11th Com)", "akash@mentorbee.com", "AkashPassword@11com", "COORDINATOR", "11TH COM"),
        ("MURALI (12th Sci/Com)", "murali@mentorbee.com", "MuraliPassword@12th", "COORDINATOR", "12TH SCI,12TH COM"),
    ]

    print("\n--- Testing All Admin & Class Coordinator Logins ---")
    admin_tokens = {}
    for label, email, pwd, role, assigned_classes in admins:
        status, data = make_request("/api/admin/login", method="POST", data={"email": email, "password": pwd})
        assert status == 200, f"Login failed for {email}: {data}"
        assert data["role"] == role
        assert data["assigned_classes"] == assigned_classes
        admin_tokens[email] = data["access_token"]
        print(f"  [PASS] {label:26} ({email}) -> Scope: {data['assigned_classes']}")

    # 5. Test Coordinator Scoped Batch Access
    print("\n--- Testing Class-Scoped Batch Retrieval for Each Coordinator ---")
    for label, email, _, _, scope in admins:
        tok = admin_tokens[email]
        status, data = make_request("/api/batches", token=tok)
        assert status == 200
        print(f"  [PASS] {label:26} -> Batches visible: {len(data):2} batches (Scope: {scope})")

    # 6. Test Creating, Updating, and Querying Sessions as Coordinator and Super Admin
    print("\n--- Testing Session Lifecycle (Create, Update, Fetch) ---")
    super_token = admin_tokens["admin@mentorbee.com"]
    
    # Fetch 8th batch id
    status, batches_8th = make_request("/api/batches?class_category=8TH", token=super_token)
    b8 = batches_8th[0]
    
    # Create session
    status, new_session = make_request("/api/sessions", method="POST", token=super_token, data={
        "batch_id": b8["id"],
        "class_category": "8TH",
        "topic": "8TH ADVANCED SCIENCE - CELL BIOLOGY",
        "class_date": "2026-08-21",
        "start_time": "18:30",
        "zoom_link": "https://zoom.us/j/99887766554?pwd=cellbio123",
        "meeting_id": "998 8776 6554",
        "passcode": "cellbio123"
    })
    assert status == 200, f"Failed session creation: {new_session}"
    session_id = new_session["id"]
    print(f"  [PASS] Created test session ID {session_id} for batch '{b8['name']}'")

    # Update session
    status, updated_session = make_request(f"/api/sessions/{session_id}", method="PUT", token=super_token, data={
        "batch_id": b8["id"],
        "class_category": "8TH",
        "topic": "8TH ADVANCED SCIENCE - CELL STRUCTURE & FUNCTIONS (UPDATED)",
        "class_date": "2026-08-21",
        "start_time": "18:30",
        "zoom_link": "https://zoom.us/j/99887766554?pwd=cellbio123",
        "meeting_id": "998 8776 6554",
        "passcode": "cellbio123"
    })
    assert status == 200, f"Failed updating session: {updated_session}"
    assert "UPDATED" in updated_session["topic"]
    print(f"  [PASS] Updated session topic -> {updated_session['topic']}")

    # Query public sessions (what mentors see)
    status, mentor_sessions = make_request("/api/sessions?scope=all")
    assert status == 200
    print(f"  [PASS] Public sessions count: {len(mentor_sessions)} active sessions")

    # 7. Test Admin Audit Logs Query (Super Admin vs Coordinator)
    print("\n--- Testing Audit Logs Access ---")
    status, logs = make_request("/api/admin/audit-logs", token=super_token)
    assert status == 200
    print(f"  [PASS] Super Admin audit logs retrieved: {len(logs)} entries")
    if logs:
        print(f"         Latest log: [{logs[0]['created_at']}] {logs[0]['mentor_name']} -> {logs[0]['action']} ({logs[0]['details']})")

    # Clean up test session
    status, _ = make_request(f"/api/sessions/{session_id}", method="DELETE", token=super_token)
    assert status == 200
    print(f"  [PASS] Cleaned up temporary test session ID {session_id}")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
