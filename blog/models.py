from sqlalchemy import  Column, Integer, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    creator = relationship('User', back_populates='blogs')
    
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    
    blogs = relationship('Blog', back_populates='creator')
    todos = relationship('Todo', back_populates='owner')
    
class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship('User', back_populates='todos')