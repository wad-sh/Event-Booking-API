from schemas.token_schema import Token
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from config import ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY



def create_access_token (data: dict):
    to_enc = data.copy()
    exp = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enc.update({
        "exp" : exp
    })

    token = jwt.encode(
        to_enc,
        SECRET_KEY,
        ALGORITHM
    )
    return token

def verify_token (token: Token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        return payload
    except JWTError :
        return None