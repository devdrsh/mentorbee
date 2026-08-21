import sys
import os

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import engine, Base, SessionLocal
from populate_all_batches import populate as populate_batches
from setup_coordinators import setup as setup_coordinators

def bootstrap():
    print("=" * 65)
    print("MENTORBEE PRODUCTION SYSTEM BOOTSTRAP")
    print("=" * 65)
    
    print("\n[Step 1/3] Initializing Database Schema...")
    Base.metadata.create_all(bind=engine)
    print("-> Database schema verified/created successfully.")

    print("\n[Step 2/3] Populating Standard Batches (State & CBSE)...")
    populate_batches()
    print("-> Batches populated successfully.")

    print("\n[Step 3/3] Setting Up Super Admin & Class Coordinators...")
    setup_coordinators()
    print("-> Admin and Coordinator accounts ready.")

    print("\n" + "=" * 65)
    print("BOOTSTRAP COMPLETE: SYSTEM READY FOR PRODUCTION HOSTING")
    print("=" * 65)

if __name__ == "__main__":
    bootstrap()
