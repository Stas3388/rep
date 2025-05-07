from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .Base import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
       
    name = Column(String)
    
    email = Column(String)
    
    hash_password = Column(String)
    
    user_data_reg = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))#&&&&
    
    transaction = relationship("Transaction", back_populates="user", lazy="selectin")
    
    category = relationship("Category", back_populates="user", lazy="selectin")