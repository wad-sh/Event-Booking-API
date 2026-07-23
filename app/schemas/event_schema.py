from pydantic import BaseModel,ConfigDict
from datetime import datetime

class EventCreate ( BaseModel) :
    title :str
    description : str | None = None
    date : datetime
    capacity : int

class EventRespShort ( BaseModel ) :
    id: int
    title :str
    model_config = ConfigDict(from_attributes=True)

class EventRespLong (BaseModel) :
    id: int
    title :str
    description : str | None = None
    date : datetime
    capacity : int
    remaining  : int
    model_config = ConfigDict(from_attributes=True)

class EventUp(BaseModel) :
    title :str | None = None
    description : str | None = None
    date : datetime | None = None
    capacity : int | None = None