#from asyncio.log import logger
from typing import TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.Exception import BaseAppException, CategoryException, TransactionException
from app.models import Category, User, Transaction


T = TypeVar("T")


async def addUni(obj: T, db: AsyncSession, commit: bool = True, refresh: bool = True):
    name = obj.__class__.__name__
    try:
        db.add(obj)
        if commit:
            await db.commit()
            if refresh:
                await db.refresh(obj)
        return {"УСПЕШНОЕ ДОБАВЛЕНИЕ": name}
    except Exception as e:
        if commit:
            await db.rollback()
        raise BaseAppException(status_code=500, detail=f"ОШИБКА ПРИ ДОБАВЛЕНИИ {name}:{e}")
    
    
async def deleteUni(obj: T, db: AsyncSession, commit: bool = True):
    name = obj.__class__.__name__
    if not obj:
        raise BaseAppException(status_code=500, detail=f"ОШИБКА ПРИ УДАЛЕНИИ {name}: нечего удалять")
    try:
        await db.delete(obj)
        if commit:
            await db.commit()
        return {"УСПЕШНОЕ УДАЛЕНИЕ": name}
    except Exception as e:
        if commit:
            await db.rollback()
        raise BaseAppException(status_code=500, detail=f"ОШИБКА ПРИ УДАЛЕНИИ {name}:{e}")
    
    
async def pathUni(obj: T, result: T, db: AsyncSession, commit: bool = True, refresh: bool = True):
    name = result.__class__.__name__
    
    try:
        
        for key, value in obj.__dict__.items():   ###
            if not key.startswith('_') and value is not None and hasattr(result, key):   ###
                setattr(result, key, value)   ###
                   
        if commit:
            await db.commit()
            if refresh:
                await db.refresh(result)
        return {"УСПЕШНОЕ ИЗМЕНЕНИЕ": name}
    
    except Exception as e:
        if commit:
            await db.rollback()
        raise BaseAppException(status_code=500, detail=f"ОШИБКА ПРИ ИЗМЕНЕНИИ {name}:{e}")
    
    
#Transaction   
async def SearchEveryTrans(db: AsyncSession, user_check):
    '''поиск всех транзакций в бд'''
    try:
        
        result = await db.execute(select(Transaction).where(Transaction.user_id == user_check.id))
        TransactionEvery = result.scalars().all()
        
        return TransactionEvery
    
    except Exception as e:
        raise TransactionException(status_code=500, detail=f"НЕОЖИДАННАЯ ОШИБКА:{e}") 


async def SearchOneTrans(TransOne:int, db: AsyncSession, user_check):
    '''поиск транзакции в бд по ид'''
    try:
        
        result = await db.execute(select(Transaction).where(Transaction.user_id == user_check.id, Transaction.id == TransOne))
        TransactionOne = result.scalars().first()
        
        if TransactionOne is None:
            raise TransactionException(status_code=404, detail="ТРАНЗАКЦИЯ НЕ НАЙДЕНА")
        
        return TransactionOne
    
    except Exception as e:
        raise TransactionException(status_code=500, detail=f"ОШИБКА : {str(e)}")


async def SearchCatTrans(CatTrans:T, db: AsyncSession):
    '''поиск категории в бд для добавления транзакции'''
        
    result = await db.execute(select(Category).where(Category.id ==  CatTrans.category_id))
    CategoryTrans = result.scalars().first()
    
    return CategoryTrans
    
        


#Category
async def SearchEveryCat(db: AsyncSession, user_check):
    '''поиск всех категорий в бд'''
    try:
        
        result = await db.execute(select(Category).where(Category.user_id == user_check.id))
        CategoryEvery = result.scalars().all()
        
        return CategoryEvery
    
    except Exception as e:
        raise CategoryException(status_code=500, detail=f"НЕОЖИДАННАЯ ОШИБКА:{e}")


async def SearchOneCat(CatOne:int, db: AsyncSession, user_check):
    '''поиск категорий в бд по ид'''
    try:
        
        result = await db.execute(select(Category).where(Category.user_id == user_check.id, Category.id == CatOne))
        CategoryOne = result.scalars().first()
        
        if CategoryOne is None:
            raise CategoryException(status_code=404, detail="КАТЕГОРИЯ НЕ НАЙДЕНА")
        
        return CategoryOne
    except Exception as e:
        raise CategoryException(status_code=500, detail=f"НЕОЖИДАННАЯ ОШИБКА:{e}")
    
        
async def SearchCatTitle(CatTitle:int, db: AsyncSession):  # not try except
    '''поиск категорий в бд по имени'''
    
    result = await db.execute(select(Category).where(Category.title_category == CatTitle.title_category))
    CategoryOne = result.scalars().first()
    
    return CategoryOne


async def SearchUser(user:T, db: AsyncSession): # not try except
    '''поиск юзера по имей в бд'''
    result = await db.execute(select(User).where(User.email == user.email))
    userEmail = result.scalars().first()
    
    return userEmail
        
    
    
