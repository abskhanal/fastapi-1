from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(String(50), nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    createdat = Column(DateTime, nullable=False, default=func.now())
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    createdat = Column(DateTime, nullable=False, default=func.now())
    

class Vote(Base):
    __tablename__ = 'votes'
    
    postid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),  primary_key=True)
    userid = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"),  primary_key=True, nullable=True)
