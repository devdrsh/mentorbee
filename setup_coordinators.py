import sys
import os
import bcrypt

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import engine, Base, SessionLocal
from app.models.admin import AdminUser
from app.models.mentor import MentorUser, MentorAccessLog
from app.models.batch import Batch
from app.models.session import ClassSession
from app.models.history import SessionChangeHistory

# Create any missing tables
Base.metadata.create_all(bind=engine)

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

COORDINATORS = [
    {
        "name": "Super Admin",
        "email": "admin@mentorbee.com",
        "password": "AdminPassword@123",
        "role": "SUPER_ADMIN",
        "assigned_classes": "ALL"
    },
    {
        "name": "ABIN M M",
        "email": "abin@mentorbee.com",
        "password": "AbinPassword@8th",
        "role": "COORDINATOR",
        "assigned_classes": "8TH"
    },
    {
        "name": "ABHIJITH M B",
        "email": "abhijith@mentorbee.com",
        "password": "AbhijithPassword@9th",
        "role": "COORDINATOR",
        "assigned_classes": "9TH"
    },
    {
        "name": "SREEHARI R",
        "email": "sreehari@mentorbee.com",
        "password": "SreehariPassword@10th",
        "role": "COORDINATOR",
        "assigned_classes": "10TH"
    },
    {
        "name": "PAVIN PAULSON",
        "email": "pavin@mentorbee.com",
        "password": "PavinPassword@11sci",
        "role": "COORDINATOR",
        "assigned_classes": "11TH SCI"
    },
    {
        "name": "AKASH",
        "email": "akash@mentorbee.com",
        "password": "AkashPassword@11com",
        "role": "COORDINATOR",
        "assigned_classes": "11TH COM"
    },
    {
        "name": "MURALI",
        "email": "murali@mentorbee.com",
        "password": "MuraliPassword@12th",
        "role": "COORDINATOR",
        "assigned_classes": "12TH SCI,12TH COM"
    },
]

def setup():
    db = SessionLocal()
    print("=" * 60)
    print("SETTING UP ADMINS & CLASS COORDINATORS")
    print("=" * 60)

    for coord in COORDINATORS:
        existing = db.query(AdminUser).filter(AdminUser.email == coord["email"]).first()
        pwd_hash = get_password_hash(coord["password"])
        
        if existing:
            existing.name = coord["name"]
            existing.password_hash = pwd_hash
            existing.role = coord["role"]
            existing.assigned_classes = coord["assigned_classes"]
            existing.is_active = True
            print(f"[UPDATED] {coord['name']} ({coord['email']}) -> Classes: {coord['assigned_classes']}")
        else:
            new_user = AdminUser(
                name=coord["name"],
                email=coord["email"],
                password_hash=pwd_hash,
                role=coord["role"],
                assigned_classes=coord["assigned_classes"],
                is_active=True
            )
            db.add(new_user)
            print(f"[CREATED] {coord['name']} ({coord['email']}) -> Classes: {coord['assigned_classes']}")

    db.commit()
    db.close()
    print("=" * 60)
    print("Setup completed successfully!")

if __name__ == "__main__":
    setup()
