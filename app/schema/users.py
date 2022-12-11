from pydantic import BaseModel, ValidationError, validator,EmailStr



class Users(BaseModel):
    email:EmailStr
    first_name:str
    last_name: str
    business_name:str
    industry:str
    password:str
    
    class config:
        orm_mode= True
    

class Login(BaseModel):
     email:EmailStr
     password:str
    
     class config:
        orm_mode= True
        
class ForgotPassword(BaseModel):
     email:EmailStr