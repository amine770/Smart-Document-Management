from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models import UserRole
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(
        ..., # mean requrired not optionnal
        min_length= 8,
        max_length= 100,
        description= "Password must be at least 8 charachter"
    )

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Confing:
        from_attributs = True #allows the converstion from sqlalchamy model
    
#=====================
#---Token response --- 
#======================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None
    
