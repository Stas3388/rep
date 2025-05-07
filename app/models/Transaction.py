from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .Base import Base

# - вводит юзер
class Transaction(Base):


    __tablename__= "transaction"

    summa = Column(Float)
    
    type_transaction = Column(Enum("income", "expense", name="type_transaction"))#
    
    Description = Column(String,nullable=True)#
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    category_id = Column(Integer,ForeignKey("category.id"))
    
    date_transaction = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))#Column(DateTime,default=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="transaction", lazy="selectin")#lazy
    
    category = relationship("Category", back_populates="transaction", lazy="selectin")