from pydantic import BaseModel,ConfigDict
from datetime import datetime


class ReservResp (BaseModel) :
    id : int
    user_id : int
    event_id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)


