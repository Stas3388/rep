from fastapi import APIRouter,Depends
from passlib.context import CryptContext
from app.Exception import PasswordException, UserException
from app.core.database import get_session
from app.models import User
from app.repository import SearchUser, addUni
from app.schemas.User import CreateUser, UserLogin
from app.core.security import create_token


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/registration", summary="РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ", tags=["ПОЛЬЗОВАТЕЛИ"])#response_model=UserCreate)????????
async def registration(user:CreateUser, db = Depends(get_session)):
    
    user_in_db = await SearchUser(user, db)#
    
    if user_in_db:
        raise UserException (status_code=409, detail="Ошибка: пользователь уже существует")
    
    hashed_password = pwd_context.hash(user.password)
    
    db_user = User(name=user.name,email=user.email, hash_password = hashed_password)
    
    await addUni(db_user, db)#
    
    return {"Вас зовут":user.name, "Ваш имейл":user.email}

@router.post("/login", summary="АУТЕНТИФИКАЦИЯ И ОТДАЧА ТОКЕНА", tags=["ПОЛЬЗОВАТЕЛИ"])
async def LoginUser(user:UserLogin, db = Depends(get_session)):
    
    db_user = await SearchUser(user, db)#
    
    if not db_user:
        raise UserException (status_code=404, detail="Ошибка: пользователя не существует")
        
        
    if not pwd_context.verify(user.password, db_user.hash_password):#???правильно ли?
        raise PasswordException(status_code=401, detail="Ошибка:пароли не совпадают")
    
    
    token_user = create_token(db_user.id, db_user.name)#????????
    
    return{"token_user": token_user, "token_type":"bearer"}
    
    

    