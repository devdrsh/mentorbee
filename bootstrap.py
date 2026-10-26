import sys
import os

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from populate_all_batches import populate as populate_batches
from setup_coordinators import setup as setup_coordinators
from app.models.history import SessionChangeHistory
from app.models.session import ClassSession
from app.models.batch import Batch

def clear_existing_batches_and_sessions_once():
    db = SessionLocal()
    try:
        db.execute(text("CREATE TABLE IF NOT EXISTS system_flags (key VARCHAR(64) PRIMARY KEY, value VARCHAR(255))"))
        row = db.execute(text("SELECT value FROM system_flags WHERE key = 'batches_sessions_cleared_v1'")).fetchone()
        if not row:
            print("\n[One-time Cleanup] Clearing all existing batches and class sessions...")
            db.query(SessionChangeHistory).delete()
            db.query(ClassSession).delete()
            db.query(Batch).delete()
            db.execute(text("INSERT INTO system_flags (key, value) VALUES ('batches_sessions_cleared_v1', 'done')"))
            db.commit()
            print("-> Successfully cleared all existing batches and sessions.")
        else:
            print("\n-> Batches & sessions cleanup already performed.")
    except Exception as e:
        db.rollback()
        print(f"-> Error checking/clearing batches: {e}")
    finally:
        db.close()

def bootstrap():
    print("=" * 65)
    print("MENTORBEE PRODUCTION SYSTEM BOOTSTRAP")
    print("=" * 65)
    
    print("\n[Step 1/3] Initializing Database Schema...")
    Base.metadata.create_all(bind=engine)
    print("-> Database schema verified/created successfully.")

    # Execute one-time cleanup on deployment so any old batches/sessions are removed
    clear_existing_batches_and_sessions_once()

    print("\n[Step 2/3] Checking Batch Population...")
    if os.getenv("POPULATE_DEFAULT_BATCHES", "false").lower() in ("true", "1", "yes"):
        print("-> POPULATE_DEFAULT_BATCHES enabled: Seeding standard batches...")
        populate_batches()
        print("-> Batches populated successfully.")
    else:
        print("-> Standard batch auto-population is disabled (fresh clean slate mode).")
        print("   (Run 'python populate_all_batches.py' manually if default batches are needed).")

    print("\n[Step 3/3] Setting Up Super Admin & Class Coordinators...")
    setup_coordinators()
    print("-> Admin and Coordinator accounts ready.")

    print("\n" + "=" * 65)
    print("BOOTSTRAP COMPLETE: SYSTEM READY FOR PRODUCTION HOSTING")
    print("=" * 65)

if __name__ == "__main__":
    bootstrap()

