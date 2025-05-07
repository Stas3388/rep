from pydantic import BaseModel,EmailStr, Field



class UserBase(BaseModel):
    name:str
    

class CreateUser(UserBase):
    email:EmailStr
    password:str = Field(..., min_length=5, description="МИН ДЛИНА 5")
    
    
class UserinDB(UserBase):
    hach_password:str
    

class UserLogin(CreateUser):
    pass