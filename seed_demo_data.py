import sys
import os
from datetime import date, time

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.batch import Batch
from app.models.session import ClassSession
from app.models.admin import AdminUser

def seed():
    db = SessionLocal()
    
    demo_batches = [
        "12TH CBSE SCIENCE KL - BATCH",
        "10TH CBSE MATHEMATICS",
        "NEET REPEATER BATCH 2026",
        "JEE ADVANCED CRASH COURSE",
        "9TH ICSE FOUNDATION"
    ]
    
    created_batches = []
    for name in demo_batches:
        existing = db.query(Batch).filter(Batch.name == name).first()
        if not existing:
            b = Batch(name=name, is_active=True)
            db.add(b)
            db.commit()
            db.refresh(b)
            created_batches.append(b)
            print(f"Created batch: {name}")
        else:
            created_batches.append(existing)
            print(f"Batch already exists: {name}")

    # Ensure demo session if none exists
    admin = db.query(AdminUser).first()
    admin_id = admin.id if admin else 1

    session_count = db.query(ClassSession).count()
    if session_count == 0 and created_batches:
        s = ClassSession(
            batch_id=created_batches[0].id,
            topic="CHEMISTRY - ORGANIC REACTION MECHANISMS",
            class_date=date.today(),
            start_time=time(19, 0),
            zoom_link="https://zoom.us/j/92399684884?pwd=demo123passcode",
            meeting_id="923 9968 4884",
            passcode="mentorbee",
            is_active=True,
            created_by=admin_id,
            updated_by=admin_id
        )
        db.add(s)
        db.commit()
        print("Created demo session for today.")

    db.close()

if __name__ == "__main__":
    seed()
