import sys
import os
from datetime import date, time, timedelta

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.batch import Batch
from app.models.session import ClassSession
from app.models.admin import AdminUser

def seed():
    db = SessionLocal()
    admin = db.query(AdminUser).first()
    admin_id = admin.id if admin else 1

    # Find a sample state batch and cbse batch
    state_batch_1 = db.query(Batch).filter(Batch.name == "10TH STATE ONLINE EVNG BATCH").first()
    state_batch_2 = db.query(Batch).filter(Batch.name == "12TH STATE SCI ONLINE EVNG BATCH").first()
    cbse_batch_1 = db.query(Batch).filter(Batch.name == "10TH CBSE EVNG KL BATCH").first()
    cbse_batch_2 = db.query(Batch).filter(Batch.name == "12TH CBSE SCI EVNG KL BATCH").first()

    today = date.today()
    tomorrow = today + timedelta(days=1)

    sessions_to_add = [
        (state_batch_1, "MATHEMATICS - QUADRATIC EQUATIONS", today, time(18, 0), "https://zoom.us/j/84201928374?pwd=state10demo", "842 0192 8374", "state10"),
        (state_batch_2, "PHYSICS - CURRENT ELECTRICITY", today, time(19, 30), "https://zoom.us/j/89102938475?pwd=state12demo", "891 0293 8475", "state12"),
        (cbse_batch_1, "SCIENCE - LIGHT REFLECTION & REFRACTION", today, time(17, 30), "https://zoom.us/j/91283746501?pwd=cbse10demo", "912 8374 6501", "cbse10"),
        (cbse_batch_2, "CHEMISTRY - ELECTROCHEMISTRY & REDOX", today, time(19, 0), "https://zoom.us/j/92399684884?pwd=cbse12demo", "923 9968 4884", "mentorbee"),
        
        # Upcoming
        (state_batch_1, "SOCIAL SCIENCE - INDIAN NATIONALISM", tomorrow, time(18, 0), "https://zoom.us/j/84201928374?pwd=state10demo", "842 0192 8374", "state10"),
        (cbse_batch_2, "BIOLOGY - GENETICS & PRINCIPLES OF INHERITANCE", tomorrow, time(19, 0), "https://zoom.us/j/92399684884?pwd=cbse12demo", "923 9968 4884", "mentorbee"),
    ]

    for batch, topic, c_date, s_time, z_link, m_id, p_code in sessions_to_add:
        if not batch:
            continue
        exists = db.query(ClassSession).filter(
            ClassSession.batch_id == batch.id,
            ClassSession.class_date == c_date,
            ClassSession.topic == topic
        ).first()
        if not exists:
            s = ClassSession(
                batch_id=batch.id,
                topic=topic,
                class_date=c_date,
                start_time=s_time,
                zoom_link=z_link,
                meeting_id=m_id,
                passcode=p_code,
                is_active=True,
                created_by=admin_id,
                updated_by=admin_id
            )
            db.add(s)
            print(f"Added session: [{batch.syllabus}] {batch.name} - {topic}")

    db.commit()
    db.close()
    print("Demo sessions created successfully!")

if __name__ == "__main__":
    seed()
