import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mentorbee.db")

def migrate():
    print(f"Migrating SQLite DB at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check and add columns to admin_users
    cursor.execute("PRAGMA table_info(admin_users)")
    admin_cols = [col[1] for col in cursor.fetchall()]
    if "role" not in admin_cols:
        cursor.execute("ALTER TABLE admin_users ADD COLUMN role VARCHAR DEFAULT 'COORDINATOR'")
        print("Added 'role' to admin_users")
    if "assigned_classes" not in admin_cols:
        cursor.execute("ALTER TABLE admin_users ADD COLUMN assigned_classes VARCHAR DEFAULT 'ALL'")
        print("Added 'assigned_classes' to admin_users")

    # Check and add columns to batches
    cursor.execute("PRAGMA table_info(batches)")
    batch_cols = [col[1] for col in cursor.fetchall()]
    if "class_category" not in batch_cols:
        cursor.execute("ALTER TABLE batches ADD COLUMN class_category VARCHAR")
        print("Added 'class_category' to batches")

    # Check and add columns to class_sessions
    cursor.execute("PRAGMA table_info(class_sessions)")
    session_cols = [col[1] for col in cursor.fetchall()]
    if "class_category" not in session_cols:
        cursor.execute("ALTER TABLE class_sessions ADD COLUMN class_category VARCHAR")
        print("Added 'class_category' to class_sessions")

    # Check and add columns to mentor_users
    cursor.execute("PRAGMA table_info(mentor_users)")
    mentor_cols = [col[1] for col in cursor.fetchall()]
    if "username" not in mentor_cols:
        cursor.execute("ALTER TABLE mentor_users ADD COLUMN username VARCHAR")
        print("Added 'username' to mentor_users")
    if "password_hash" not in mentor_cols:
        cursor.execute("ALTER TABLE mentor_users ADD COLUMN password_hash VARCHAR")
        print("Added 'password_hash' to mentor_users")

    # Create class_mentor_accounts if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_mentor_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_category VARCHAR UNIQUE NOT NULL,
        username VARCHAR UNIQUE NOT NULL,
        password_hash VARCHAR NOT NULL,
        display_title VARCHAR NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Ensured 'class_mentor_accounts' table exists")

    # Create mentor_access_logs if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mentor_access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_name VARCHAR NOT NULL,
        assigned_class VARCHAR NOT NULL,
        session_id INTEGER,
        batch_name VARCHAR,
        action VARCHAR NOT NULL,
        ip_address VARCHAR,
        details TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Ensured 'mentor_access_logs' table exists")

    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
