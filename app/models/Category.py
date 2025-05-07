from sqlalchemy import ForeignKey, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .Base import Base

class Category(Base):
    __tablename__= "category"
    
    title_category = Column(String, nullable=False)
    
    type_transaction = Column(Enum("income", "expense", name="type_transaction"))#
    
    Description = Column(String,nullable=True)#
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="category", lazy="selectin")
    
    transaction = relationship("Transaction", back_populates="category", lazy="selectin") 