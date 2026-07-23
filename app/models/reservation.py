from database.database import Base
from sqlalchemy import Column,Integer,DateTime,func,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship

class Reservation (Base) :
    __tablename__ = "reservations"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="uq_user_event"
        ),
    )

    id = Column(
        Integer,
        primary_key=True
    )


    user_id= Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    event_id= Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )


    created_at= Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="reservations"
    )

    event = relationship(
        "Event",
        back_populates="reservations"
    )