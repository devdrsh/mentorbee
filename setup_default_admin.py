import sys
import os

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.admin import AdminUser
from app.routers.admin import get_password_hash

def main():
    email = "admin@mentorbee.com"
    password = "password123"
    name = "Default Admin"

    db = SessionLocal()
    existing = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not existing:
        admin = AdminUser(email=email, name=name, password_hash=get_password_hash(password))
        db.add(admin)
        db.commit()
        print(f"Admin {email} created successfully.")
    else:
        print("Admin already exists.")
    db.close()

if __name__ == "__main__":
    main()
