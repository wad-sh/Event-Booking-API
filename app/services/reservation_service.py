from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.reservation import Reservation
from models.event import Event
from schemas.reservation_schema import *

def create_reserv (db:Session,user_id: int,event_id: int) : 
    try:
        e = db.query(Event).filter(Event.id == event_id).with_for_update().first()
        if not e :
            raise HTTPException(
                status_code=404,
                detail="no event has been found"
            )
        ex = db.query(Reservation).filter(Reservation.event_id == event_id, Reservation.user_id == user_id).first()
        if ex is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Reservation already existed"
                )
        r_count = db.query(Reservation).filter(Reservation.event_id == event_id).count()
        if r_count >= e.capacity:
            raise HTTPException(
                        status_code=409,
                        detail="no room left"
                    )
        new_res = Reservation(
            user_id=user_id,
            event_id=event_id
        )

        db.add(new_res)
        db.commit()
        db.refresh(new_res)

        return new_res
    except HTTPException:
        db.rollback
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
def delete_reserv (db:Session,user_id: int,event_id: int) : 
    res = db.query(Reservation).filter(Reservation.event_id == event_id, Reservation.user_id == user_id).first()
    if res is None:
            raise HTTPException(
                    status_code=404,
                    detail="Reservation not found"
                )
    db.delete(res)
    db.commit()
    return {
    "message": "Reservation deleted"
}