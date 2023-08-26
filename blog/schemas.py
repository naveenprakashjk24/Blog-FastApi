from typing import List
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class BlogBase(Blog):
    title: str
    body: str
    class Config():
        orm_mode = True  
        
class User(BaseModel):
    name: str
    email: str
    password : str
    
class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True  
    
class ShowBlogUser(BaseModel):
    name: str
    email: str
    blogs : List[BlogBase]
    class Config():
        orm_mode = True    
        
class ShowBlog(BaseModel):
    title: str
    body: str
    creator : ShowUser
    
    class Config():
        orm_mode = True
        
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None