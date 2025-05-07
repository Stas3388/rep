from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column,Integer

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    

