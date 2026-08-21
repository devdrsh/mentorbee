import sys
import os

# Add root dir to sys path
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.admin import AdminUser
from app.routers.admin import get_password_hash

def main():
    print("MentorBee Admin Setup")
    print("---------------------")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    name = input("Enter admin name: ")

    db = SessionLocal()
    existing = db.query(AdminUser).filter(AdminUser.email == email).first()
    if existing:
        print("User already exists!")
        sys.exit(1)
    
    admin = AdminUser(email=email, name=name, password_hash=get_password_hash(password))
    db.add(admin)
    db.commit()
    print(f"Admin {email} created successfully.")
    db.close()

if __name__ == "__main__":
    main()
