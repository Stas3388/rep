from typing import Literal
from pydantic import BaseModel


class Finance(BaseModel):
     
     Description:str
     
     type_transaction:Literal["income","expense"]