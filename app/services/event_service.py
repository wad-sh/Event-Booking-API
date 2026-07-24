from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.event import Event
from schemas.event_schema import *


def create_event (db: Session,data: EventCreate,user_id:int) : 
    new_event = Event(
        title = data.title,
        description = data.description,
        created_by = user_id,
        date = data.date,
        capacity= data.capacity
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


def get_events(db: Session) : 
    events = db.query(Event).all()
    return events
    


def get_event (db: Session,event_id: int) : 
    event = db.query(Event).filter(Event.id == event_id).first()
    if  not event :
        raise HTTPException(
            status_code=404,
            detail="can't find event"
        )
    return event


def up_event(db: Session,user_id: int,data: EventUp) : 
    e = db.query(Event).filter(Event.created_by==user_id, Event.id == data.id).first()
    if not e :
            raise HTTPException(
                status_code=404,
                detail="can't find event"
            ) 

    if data.title is None and data.description is None and  data.date is None and data.capacity is None:
         raise HTTPException(
                         status_code=400 ,
                         detail="no change"
                     ) 
    if data.capacity > 0 :
          raise HTTPException(
                                   status_code=401 ,
                                   detail="positive numbers only from capacity"
                               ) 
    if data.title is not None:
         e.title = data.title
    if data.description is not None:
             e.description = data.description
    if data.date is not None:
             e.date = data.date
    if data.capacity is not None:
             e.capacity = data.capacity

    db.commit()
    db.refresh(e)
    return e

def delete_event (db: Session,user_id: int,event_id: int) : 
    event = db.query(Event).filter(Event.created_by==user_id, Event.id == event_id).first()
    if  not event :
            raise HTTPException(
                status_code=404,
                detail="can't find event"
            )
    db.delete(event)
    db.commit()
    return {
    "message": "Event deleted"
}



