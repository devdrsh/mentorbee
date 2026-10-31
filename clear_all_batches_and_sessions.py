import sys
import os

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.history import SessionChangeHistory
from app.models.session import ClassSession
from app.models.batch import Batch

def clear_all():
    if "--confirm-wipe-all-data" not in sys.argv:
        print("[BLOCKED] Database wipe aborted. Batch and session persistence is enabled.")
        print("To intentionally clear the database, pass flag: python clear_all_batches_and_sessions.py --confirm-wipe-all-data")
        return
    print("=" * 60)
    print("CLEARING ALL BATCHES AND SESSIONS FROM DATABASE")
    print("=" * 60)

    db = SessionLocal()
    try:
        history_count = db.query(SessionChangeHistory).count()
        sessions_count = db.query(ClassSession).count()
        batches_count = db.query(Batch).count()

        print(f"Current records found:")
        print(f"- Session Change History: {history_count}")
        print(f"- Class Sessions: {sessions_count}")
        print(f"- Batches: {batches_count}")

        print("\nDeleting session change history records...")
        db.query(SessionChangeHistory).delete()

        print("Deleting class sessions...")
        db.query(ClassSession).delete()

        print("Deleting batches...")
        db.query(Batch).delete()

        db.commit()
        print("\n[SUCCESS] All existing batches and sessions have been permanently cleared from the database!")

        remaining_batches = db.query(Batch).count()
        remaining_sessions = db.query(ClassSession).count()
        print(f"Verification: Batches remaining = {remaining_batches}, Sessions remaining = {remaining_sessions}")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Failed to clear database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clear_all()
