from database.database import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,String,func
from sqlalchemy.orm import relationship

class Event (Base) :

    __tablename__ = "events"


    id = Column(
        Integer,
        primary_key=True
    )


    title= Column(
        String,
        nullable=False
    )


    description= Column(
        String
    )


    date= Column(
        DateTime,
        nullable=False
    )


    capacity= Column(
        Integer,
        nullable=False
    )


    created_by= Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    created_at= Column(
        DateTime,
        server_default=func.now(),
        nullable=False

    )

    reservations= relationship(
        "Reservation",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    creator = relationship(
        "User",
        back_populates="events"
    )