import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.main import app

client = TestClient(app)

def test_all():
    print("=" * 60)
    print("RUNNING AUTOMATED SYSTEM TESTS")
    print("=" * 60)

    # 1. Test Mentor Login with correct passcode
    res = client.post("/api/mentor/login", json={
        "name": "TEST MENTOR",
        "assigned_class": "8TH",
        "passcode": "AGENTBEE0809"
    })
    print(f"1. Mentor Login (Valid Passcode): Status {res.status_code}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    mentor_data = res.json()
    mentor_token = mentor_data["access_token"]
    print(f"   Logged in as: {mentor_data['name']}, Class: {mentor_data['assigned_class']}")

    # 2. Test Mentor Login with invalid passcode
    res = client.post("/api/mentor/login", json={
        "name": "TEST MENTOR",
        "assigned_class": "8TH",
        "passcode": "WRONG_PASS"
    })
    print(f"2. Mentor Login (Invalid Passcode): Status {res.status_code}")
    assert res.status_code == 401, f"Expected 401, got {res.status_code}"

    # 3. Test Mentor Log Action
    res = client.post(
        "/api/mentor/log-action",
        headers={"Authorization": f"Bearer {mentor_token}"},
        json={
            "action": "COPY_MESSAGE",
            "session_id": 1,
            "batch_name": "8TH STATE ONLINE BATCH",
            "details": "Mentor copied message for 8th State"
        }
    )
    print(f"3. Mentor Action Logging: Status {res.status_code}")
    assert res.status_code == 200

    # 4. Test Coordinator & Super Admin Logins
    coordinators_to_test = [
        ("admin@mentorbee.com", "AdminPassword@123", "SUPER_ADMIN", "ALL"),
        ("abin@mentorbee.com", "AbinPassword@8th", "COORDINATOR", "8TH"),
        ("abhijith@mentorbee.com", "AbhijithPassword@9th", "COORDINATOR", "9TH"),
        ("sreehari@mentorbee.com", "SreehariPassword@10th", "COORDINATOR", "10TH"),
        ("pavin@mentorbee.com", "PavinPassword@11sci", "COORDINATOR", "11TH SCI"),
        ("akash@mentorbee.com", "AkashPassword@11com", "COORDINATOR", "11TH COM"),
        ("murali@mentorbee.com", "MuraliPassword@12th", "COORDINATOR", "12TH SCI,12TH COM"),
    ]

    print("\n4. Testing Admin / Coordinator Logins:")
    admin_token = None
    for email, pwd, expected_role, expected_class in coordinators_to_test:
        res = client.post("/api/admin/login", json={"email": email, "password": pwd})
        assert res.status_code == 200, f"Login failed for {email}: {res.text}"
        data = res.json()
        assert data["role"] == expected_role, f"Expected role {expected_role}, got {data['role']}"
        assert data["assigned_classes"] == expected_class, f"Expected class {expected_class}, got {data['assigned_classes']}"
        print(f"   [OK] {data['name']} ({email}) -> Role: {data['role']} | Class: {data['assigned_classes']}")
        if email == "admin@mentorbee.com":
            admin_token = data["access_token"]

    # 5. Test Batches Query Scoped by Class Category
    res = client.get("/api/batches?class_category=8TH")
    print(f"\n5. Batches Query for '8TH': Status {res.status_code}, Count: {len(res.json())}")
    assert res.status_code == 200

    # Create a dynamic test batch for 8TH
    res_b8 = client.post(
        "/api/batches",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "TEST 8TH DYNAMIC BATCH",
            "class_category": "8TH",
            "syllabus": "STATE"
        }
    )
    assert res_b8.status_code == 200
    batch_8th = res_b8.json()
    print(f"   [OK] Created dynamic test batch for 8TH (ID: {batch_8th['id']})")

    res = client.get("/api/batches?class_category=8TH")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 6. Test Admin Audit Logs Query
    res = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {admin_token}"})
    print(f"\n6. Audit Logs Query: Status {res.status_code}, Entries: {len(res.json())}")
    assert res.status_code == 200

    # 7. Test Session Creation with class_category
    res = client.post(
        "/api/sessions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "batch_id": batch_8th["id"],
            "class_category": "8TH",
            "topic": "8th Mathematics - Linear Equations",
            "class_date": "2026-08-20",
            "start_time": "18:00",
            "zoom_link": "https://zoom.us/j/888999111",
            "meeting_id": "888 999 111",
            "passcode": "123456"
        }
    )
    print(f"\n7. Create Session with class_category: Status {res.status_code}")
    assert res.status_code == 200
    created_session = res.json()
    assert created_session["class_category"] == "8TH"
    print(f"   Created Session ID: {created_session['id']}")

    # Clean up the 8TH test session and batch
    del_s = client.delete(f"/api/sessions/{created_session['id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert del_s.status_code == 200
    del_b = client.delete(f"/api/batches/{batch_8th['id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert del_b.status_code == 200
    print(f"   [OK] Cleaned up test session {created_session['id']} and batch {batch_8th['id']}")

    # 8. Test Batch Creation and Deletion (Normal and Force)
    print("\n8. Testing Batch Creation and Deletion:")
    # 8a: Create a standalone batch
    create_res = client.post(
        "/api/batches",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "TEMPORARY TEST BATCH ALPHA",
            "class_category": "10TH",
            "syllabus": "STATE"
        }
    )
    assert create_res.status_code == 200, f"Failed to create test batch: {create_res.text}"
    temp_batch = create_res.json()
    temp_batch_id = temp_batch["id"]
    print(f"   [OK] Created Temp Batch ID: {temp_batch_id} ('{temp_batch['name']}')")

    # 8b: Delete standalone batch without sessions
    del_res = client.delete(
        f"/api/batches/{temp_batch_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert del_res.status_code == 200, f"Failed to delete batch: {del_res.text}"
    print(f"   [OK] Standalone Batch Deleted: Status {del_res.status_code}")

    # 8c: Create another batch with a session linked to it
    create_res2 = client.post(
        "/api/batches",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "TEMPORARY TEST BATCH BETA",
            "class_category": "9TH",
            "syllabus": "CBSE"
        }
    )
    assert create_res2.status_code == 200
    temp_batch2 = create_res2.json()
    temp_batch2_id = temp_batch2["id"]

    sess_res = client.post(
        "/api/sessions",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "batch_id": temp_batch2_id,
            "class_category": "9TH",
            "topic": "Test Session for Batch Beta",
            "class_date": "2026-08-21",
            "start_time": "19:00",
            "zoom_link": "https://zoom.us/j/999888777",
            "meeting_id": "999 888 777",
            "passcode": "654321"
        }
    )
    assert sess_res.status_code == 200
    print(f"   [OK] Created Batch with Linked Session (ID: {sess_res.json()['id']})")

    # 8d: Delete without force should fail with 400
    del_fail_res = client.delete(
        f"/api/batches/{temp_batch2_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert del_fail_res.status_code == 400, f"Expected 400, got {del_fail_res.status_code}"
    print(f"   [OK] Delete without force rejected as expected: {del_fail_res.json()['detail']}")

    # 8e: Delete with force=true should succeed
    del_force_res = client.delete(
        f"/api/batches/{temp_batch2_id}?force=true",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert del_force_res.status_code == 200, f"Force delete failed: {del_force_res.text}"
    print(f"   [OK] Force Delete succeeded: {del_force_res.json()['detail']}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_all()
