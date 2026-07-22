from database.database import Base
from sqlalchemy import Column,Integer,String,Enum as SQLEnum
from sqlalchemy.orm import relationship
from enums.adminuser import AdminUser

class User (Base) :
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key = True
    )

    username = Column(
        String,
        index =True,
        unique = True,
        nullable=False
    )

    email = Column(
        String,
        index =True,
        unique = True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable = False
    )

    role = Column(
        SQLEnum(AdminUser),
        default=AdminUser.user,
        nullable = False
    )

    reservations = relationship(
        "Reservation",
        back_populates="user",
        cascade="all, delete-orphan"
    )