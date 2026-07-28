from services.user_service import user_login,user_reg
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schema import UserResp,UserReg
from database.database import get_db
from  schemas.token_schema import Token



user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@user_router.post("/register", response_model=UserResp)
def register(
    data: UserReg,
    db:Session = Depends(get_db) 
) :
    return user_reg(db,data)


@user_router.post("/login", response_model=Token)
def login(
    data: OAuth2PasswordRequestForm= Depends(),
    db:Session = Depends(get_db) 
) :
    return user_login(db,data)