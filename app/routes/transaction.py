from fastapi import APIRouter, Depends
from app.Exception import TransactionException
from app.models import Transaction
from app.core.database import get_session
from app.repository import SearchCatTrans, SearchEveryTrans, SearchOneTrans, addUni, deleteUni, pathUni
from app.schemas.Transaction import TransactionCreate, TransactionUpdate, TransactionOut
from app.core.security import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/transaction/create", summary="СОЗДАТЬ ТРАНЗАКЦИЮ", tags=["ТРАНЗАКЦИИ"])
async def transaction_create(transaction:TransactionCreate, db:AsyncSession = Depends(get_session), user_check = Depends(get_current_user)):
    
    category = await SearchCatTrans(transaction, db)
    
    if not category:
        raise TransactionException(status_code=404, detail="НЕТ ТАКОЙ КАТЕГОРИИ") 
    
    transaction_data = transaction.model_dump()
    new_transaction = Transaction(**transaction_data, user_id = user_check.id)
    
    return await addUni(new_transaction,db)  
       
  
@router.get("/transactions", response_model=list[TransactionOut], summary="ПОКАЗАТЬ ВСЕ ТРАНЗАКЦИИ", tags=["ТРАНЗАКЦИИ"])
async def show_transactions(db = Depends(get_session), user_check = Depends(get_current_user)):
    
    return await SearchEveryTrans(db, user_check)


@router.get("/transactions/{transaction_id}", response_model= TransactionOut, summary="ПОКАЗАТЬ ТРАНЗАКЦИЮ ПО ID", tags=["ТРАНЗАКЦИИ"])
async def show_transaction(transaction_id: int, db = Depends(get_session), user_check = Depends(get_current_user)):####??????
    
    return await SearchOneTrans(transaction_id, db, user_check)


@router.delete("/transactions/{transaction_id}", summary="УДАЛЕНИЕ ТРАНЗАКЦИИ ПО ID", tags=["ТРАНЗАКЦИИ"])
async def delete_transaction(transaction_id: int, db:AsyncSession = Depends(get_session), user_check = Depends(get_current_user)):
    
    dbtransaction = await SearchOneTrans(transaction_id, db, user_check)
    
    if not dbtransaction:
        raise TransactionException(status_code=404, detail="НЕЧЕГО УДАЛЯТЬ")
    
    return await deleteUni(dbtransaction, db)


@router.patch("/transactions/{transaction_id}", summary="ИЗМЕНИТЬ ТРАНЗАКЦИЮ", tags=["ТРАНЗАКЦИИ"])
async def path_transaction(transaction_id:int, transaction:TransactionUpdate, db = Depends(get_session),
                           user_check = Depends(get_current_user)):
    
    dbtransaction = await SearchOneTrans(transaction_id, db, user_check)
    
    if not dbtransaction:
        raise TransactionException(status_code=404, detail="НЕТ ТАКОЙ ТРАНЗАКЦИИ")
    
    return  await pathUni(transaction, dbtransaction, db)

    # try:
        
    #     new_description = transaction.Description
     
    #     new_type_transaction = transaction.type_transaction
    
    #     new_summa = transaction.summa
        
    #     if new_description is not None:
            
    #         dbtransaction.Description = new_description
            
            
    #     if new_type_transaction is not None :
            
    #         dbtransaction.type_transaction = new_type_transaction
            
               
    #     if new_summa is not None:
            
    #         dbtransaction.summa = new_summa
        
            
    #     await db.commit()
    #     await db.refresh(dbtransaction)
    #     return dbtransaction
            
    # except:
    #     raise HTTPException(status_code=404, detail="НЕ УДАЛОСЬ ОБНОВИТЬ ТРАНЗАКЦИЮ")
            
    