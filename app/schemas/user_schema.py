from pydantic import BaseModel,ConfigDict

class UserResp (BaseModel) :
    id : int
    username : str
    email : str
    model_config = ConfigDict(from_attributes=True)

class UserReg (BaseModel) :
    username : str
    email : str
    password : str

