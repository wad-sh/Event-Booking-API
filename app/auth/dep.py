from fastapi import HTTPException,Depends
from auth.jwt_handler import verify_token
from sqlalchemy.orm import Session
from models.user import User
from database.database import get_db
from fastapi.security import OAuth2PasswordBearer
from enums.adminuser import AdminUser



token_reader = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)



def get_crr_u (db:Session = Depends(get_db) ,token: str = Depends(token_reader)):
    payload = verify_token(token)

    if payload is None :
        raise HTTPException(
            status_code=401,
            detail="invalid token"
        )
    
    user_id = payload.get("sub")
    if user_id is None :
        raise HTTPException(
                    status_code=401,
                    detail="invalid token"
                )
    
    user_id = int(user_id)
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code= 401,
            detail="user not found"
        )
    
    return user

def req_admin (crr_u: User = Depends(get_crr_u)):
    if crr_u.role != AdminUser.admin:
        raise HTTPException(
            status_code=403,
            detail="you are not an admin"
        )
    return crr_u