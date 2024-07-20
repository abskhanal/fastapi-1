
from pydantic import BaseModel, EmailStr
from datetime import datetime

    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    createdat: datetime
    user: UserOut
    
    class Config:
        orm_mode = True
    
class PostOut(BaseModel):
    Post: Post
    votes:int
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: str
    
class Vote(BaseModel):
    postid: int
    vote: int