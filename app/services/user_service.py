from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from schemas.token_schema import Token
from auth.security import hash_pw,ver_pw
from schemas.user_schema import UserReg
from fastapi.security import OAuth2PasswordRequestForm
from enums.adminuser import AdminUser
from auth.jwt_handler import create_access_token


def user_reg (db: Session,data: UserReg) :
    ex_un = db.query(User).filter(User.username == data.username).first()
    ex_em = db.query(User).filter(User.email == data.email).first()

    if ex_un :
        raise HTTPException (
            status_code= 409,
            detail="username already exists"
        )

    if ex_em :
        raise HTTPException (
            status_code=409,
            detail="email already exists"
        )

    hashed_pw = hash_pw(data.password)

    new_user = User(
        username = data.username,
        email = data.email,
        hashed_password = hashed_pw,
        role=AdminUser.user
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def user_login (db:Session, data: OAuth2PasswordRequestForm) :
    user = db.query(User).filter(User.email == data.username).first()
    if not user :
        raise HTTPException (
            status_code=401,
            detail="wrong email or password"
        )
    hashed = user.hashed_password
    pw = ver_pw (data.password,hashed)
    if not pw :
        raise HTTPException (
                    status_code=401,
                    detail="wrong email or password"
                )
    access_token = create_access_token({"sub" : str(user.id)})

    return{
        "access_token" : access_token,
        "token_type" : "bearer"
    }

