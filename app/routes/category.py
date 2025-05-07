# from asyncio.log import logger
from fastapi import APIRouter, Depends
from app.Exception import CategoryException
from app.models import Category
from app.core.database import get_session
from app.repository import SearchCatTitle, SearchEveryCat, SearchOneCat, addUni, deleteUni, pathUni
from app.schemas.Category import CreateCategory, CategoryOut, UpdateCategory
from app.core.security import get_current_user




router = APIRouter()


@router.post("/category/new", summary="СОЗДАНИЕ КАТЕГОРИИ", tags=["КАТЕГОРИИ"])
async def create_category(category:CreateCategory, db = Depends(get_session), user_check = Depends(get_current_user)):
    
    check_category = await SearchCatTitle(category, db)
    
    if check_category is not None:
        raise CategoryException(status_code=409, detail="ЕСТЬ ТАКАЯ КАТЕГОРИЯ")
    
    category_data = category.model_dump()   
    new_category = Category(**category_data, user_id = user_check.id)
        
    return await addUni(new_category,db)
    
       
@router.get("/categories", response_model=list[CategoryOut], summary="ПОКАЗАТЬ ВСЕ КАТЕГОРИИ", tags=["КАТЕГОРИИ"])
async def add_category(db = Depends(get_session), user_check = Depends(get_current_user)):
    
    return await SearchEveryCat(db, user_check)
    
@router.delete("/categories/{category_id}", summary="УДАЛЕНИЕ КАТЕГОРИИ ПО ID", tags=["КАТЕГОРИИ"])
async def delete_category(category_id:int, db = Depends(get_session), user_check = Depends(get_current_user)):
     
    dbcategory = await SearchOneCat(category_id, db, user_check)
    
    return await deleteUni(dbcategory, db)
    

@router.patch("/category/{category_id}", summary="ИЗМЕНИТЬ КАТЕГОРИЮ", tags=["КАТЕГОРИИ"])
async def change_category(category_id:int, category:UpdateCategory, db = Depends(get_session), 
                          user_check = Depends(get_current_user)):
    
    dbcategory = await SearchOneCat(category_id, db, user_check)
    
    return  await pathUni(category, dbcategory, db)
    
    
    # try:
        
    #     new_description = category.Description
     
    #     new_type_transaction = category.type_transaction
    
    #     new_title_category = category.title_category
        
    #     if new_description is not None:
            
    #         dbcategory.Description = new_description
            
            
    #     if new_type_transaction is not None:
            
    #         dbcategory.type_transaction = new_type_transaction
            
               
    #     if new_title_category is not None:
            
            
    #         dbcategory.title_category = new_title_category
            
            
    #     await db.commit()
    #     await db.refresh(dbcategory)
    #     return dbcategory
            
    # except:
    #     raise HTTPException(status_code=404, detail="НЕ УДАЛОСЬ ОБНОВИТЬ КАТЕГОРИЮ")#######
    
    
    
    