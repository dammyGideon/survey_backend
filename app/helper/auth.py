import jwt
import time
from typing import Dict
from dotenv import dotenv_values
from app.model.users import UsersModel
from fastapi import HTTPException, status
configure = dotenv_values(".env")


async def very_token(token:str):
    try:
        payload = jwt.decode(token, configure['secret'], configure['algorithm'])
        user= await UsersModel.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            header={"WWW-Authenticate":"Bearer"}                
            )
    return user



def token_response(token: str):
    return {
        "access_token": token
    }



def signJwt(id:str) -> Dict[str, str]:
    payload ={
        "id":id,
        "expires":time.time() + 600
    }
    
    token = jwt.encode(payload, algorithm="HS256")
    return token_response(token)