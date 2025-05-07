

class BaseAppException(Exception):
    """Base app exeption. Internal Server Error"""
    code: str = "APP_ERROR"

    def __init__(self, detail: str = "", status_code: int = 500):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        
    
class RepositoryException(BaseAppException):
    code = "REPOSITORY_EXCEPTION"
    
    
class PasswordException(BaseAppException):...
    

class CategoryException(BaseAppException):...


class TransactionException(BaseAppException):...


class UserException(BaseAppException):...


class TokenException(BaseAppException):...
         

    
    
    

    