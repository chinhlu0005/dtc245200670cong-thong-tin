from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="reader")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    content = Column(Text)
    category = Column(String, default="thoisu")
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)