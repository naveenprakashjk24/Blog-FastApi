from typing import List
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class BlogBase(Blog):
    id: int
    title: str
    body: str
    class Config():
        from_attributes = True  
        
class User(BaseModel):
    name: str
    email: str
    password : str

class UserBase(User):
    name: str
    email: str
    class Config():
        from_attributes = True
    
class ShowUser(BaseModel):
    id :int
    name: str
    email: str
    class Config():
        from_attributes = True 
    
class ShowUserBlog(BaseModel):
    name: str
    email: str
    blogs : List[BlogBase]
    class Config():
        from_attributes = True

class ShowBlogUser(BaseModel):
    title: str
    body: str
    creator : ShowUser
    class Config():
        from_attributes = True    
        
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class Todo(BaseModel):
    title : str
    description :str
    priority : int

class showTodo(Todo):
    completed : str
    owner_id : ShowUser
    
    class Config():
        from_attributes = True


class TokenData(BaseModel):
    email: str | None = None