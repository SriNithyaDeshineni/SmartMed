from getpass import getpass
from passlib.context import CryptContext
from database import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

name = input("Enter admin name: ").strip()
email = input("Enter admin email: ").strip().lower()
password = getpass("Create admin password: ")
confirm = getpass("Confirm admin password: ")

if not name or not email:
    raise SystemExit("Name and email are required.")

if password != confirm:
    raise SystemExit("Passwords do not match.")

if len(password.encode("utf-8")) > 72:
    raise SystemExit("Password must be 72 bytes or fewer.")

if len(password) < 12:
    raise SystemExit("Use a password with at least 12 characters.")

password_hash = pwd_context.hash(password)

conn = get_db_connection()
try:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO admins (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING admin_id, name, email
            """,
            (name, email, password_hash)
        )
        admin = cur.fetchone()
    conn.commit()
    print("Admin account created successfully:")
    print(admin)
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
