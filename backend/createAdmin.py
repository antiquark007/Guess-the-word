# Creates an administrator account in the database.
from backend.database.connection import SessionLocal
from backend.database.models import User
from backend.auth.security import hash_password


db = SessionLocal()

admin = User(
    username="name",
    password_hash=hash_password("Admin1$"),
    role="ADMIN"
)

db.add(admin)
db.commit()

print("Admin created successfully.")

db.close()