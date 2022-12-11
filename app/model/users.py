from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class UsersModel(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer(), primary_key=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    first_name= Column(String(255), nullable=True)
    last_name= Column(String(255), nullable=True)
    business_name=Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    password= Column(String(255), nullable=True)
    is_verified=Column(Boolean(), default=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    
    
    
