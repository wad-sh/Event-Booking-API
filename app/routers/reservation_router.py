from services.reservation_service import *
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.reservation_schema import *
from database.database import get_db
from auth.dep import get_crr_u
from models.user import User

res_router = APIRouter(
    tags=["reservations"]
)

@res_router.post("/events/{event_id}/reserve",response_model=ReservResp)
def r_create (
    event_id: int,
    user: User = Depends(get_crr_u),
    db:Session = Depends(get_db)
) :
    return create_reserv (db,user.id,event_id)

@res_router.delete("/events/{event_id}/reserve",response_model=dict)
def r_delete (
    event_id: int,
    user: User = Depends(get_crr_u),
    db:Session = Depends(get_db) 
) :
    return delete_reserv (db,user.id,event_id )