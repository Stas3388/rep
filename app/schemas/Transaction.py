from app.schemas.Finance import Finance
from pydantic import field_validator


class Transaction(Finance):
    
    summa:float
    
    category_id:int
    
    @field_validator("summa")
    def validator_summa(cls, summa:float):
        
        if summa <= 0:
            raise ValueError("сумма не может быть меньше 0")
        return summa
       
    @field_validator("category_id")
    def validator_category(cls, category_id:int):
        
        if category_id <= 0:
            raise ValueError("ID категории не может быть меньше 0")
        return category_id
    
class TransactionCreate(Transaction):pass#

class TransactionUpdate(Transaction):pass# а надо ли????
    
class TransactionOut(Transaction):pass#