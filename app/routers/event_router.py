from app.services.event_service import *
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.event_schema import *
from app.database.database import get_db
from app.auth.dep import req_admin
from app.models.user import User
from typing import List


event_router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@event_router.post("",status_code=201,response_model=EventRespLong)
def e_create (
    data: EventCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(req_admin)
): 
    return create_event(db,data,admin.id)

@event_router.get("",response_model=List[EventRespShort])
def get_e_all (
    db: Session = Depends(get_db)
) : return get_events(db)

@event_router.get("/{id}",response_model=EventRespLong)
def get_e_one (
    id: int,
    db: Session = Depends(get_db)
) :
    return get_event(db,id)

@event_router.put("/{id}",response_model=EventRespLong) 
def e_update (
    id: int,
    data: EventUp,
    db: Session = Depends(get_db),
    admin: User = Depends(req_admin)
) :
    return up_event(db,id,data)

@event_router.delete("/{id}",response_model=dict)
def e_delete (
    id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(req_admin) 
) :
    return delete_event(db,id)