from sqlalchemy import Column, Integer, String
from app.dataBases.base import Base

class Task(Base):
    __tablename__ = "task"
    __table_args__ = {'schema': 'schedule'}
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
