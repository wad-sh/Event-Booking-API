from database.database import SessionLocal
from models.user import User
from models.reservation import Reservation
from models.event import Event
from auth.security import hash_pw
from enums.adminuser import AdminUser
from getpass import getpass

db = SessionLocal()
try :
    usernameA = input("Enter username: ")
    emailA = input("Enter email: ")
    passwordA = getpass("Enter password: ")

    ex_un = db.query(User).filter(User.username == usernameA).first()
    ex_em = db.query(User).filter(User.email == emailA).first()
    if ex_un is not None:
        raise ValueError("Username exists already")
    if ex_em is not None:
        raise ValueError("Email exists already")
    
    admin = User(
        username = usernameA,
        email = emailA,
        hashed_password = hash_pw(passwordA),
        role = AdminUser.admin
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"Admin created successfully: {admin.username}")
except Exception as e:
    db.rollback()
    print(e)
finally:
    db.close()