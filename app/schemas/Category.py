from app.schemas.Finance import Finance



class Category(Finance):
    
    title_category:str
    
     
class CreateCategory(Category):#???????
    
    pass
    
    
class CategoryOut(Category):
    
    id:int
    
class UpdateCategory(Category):pass
    
    
    