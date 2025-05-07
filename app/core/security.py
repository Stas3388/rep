from sqlalchemy import select
from typing import Optional
from jose import jwt
from fastapi import Depends
from app.Exception import TokenException
from app.core.config import SECRET_KEY
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.database import get_session
from app.models.User import User

from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import SECRET_KEY,time



def create_token(user_id: int, username: str):
    data_token = {"sub":str(user_id), "name":username, "iat":datetime.now(timezone.utc),
              "exp":datetime.now(timezone.utc) + timedelta(hours=time)}
    
    token = jwt.encode(data_token, SECRET_KEY, algorithm='HS256')
    
    
    return token


security = HTTPBearer()

def get_jwt_from_header(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[str]:
    if not credentials:
        raise TokenException(status_code=401, message="Missing authorization credentials")
    if credentials.scheme.lower() != "bearer":
        raise TokenException(status_code=401, message="Invalid authorization scheme")
    return credentials.credentials
    
    
    

ALGORITHM = "HS256"

def decode_token(token:str):
    
    try:
        result =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]})#????exp sub или все
        
        return result
        
    except:
        raise TokenException(
        status_code=401,
        detail="ТОКЕН НЕ КОРРЕКТЕН")
    
    
async def check_token(token: str , db = Depends(get_session)):
    
    check = decode_token(token)
    user_id = check.get("sub")
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    
    
    if not user:
        raise TokenException(status_code=404, detail="НЕ НАЙДЕН в базе по токену")
    
    
    return user



async def get_current_user(
    token: str = Depends(get_jwt_from_header),
    db = Depends(get_session)) -> User:
       
    user = await check_token(token, db) 
    
    return user