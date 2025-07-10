# init_db.py

from database import Base, engine, SessionLocal
import models.user  # to register the User model with Base

Base.metadata.create_all(bind=engine)  # Create tables in the database

from models.user import User
from utils.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        admin = User(
            email="admin@example.com",
            hashed_password=hash_password("adminpassword"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Admin user created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
