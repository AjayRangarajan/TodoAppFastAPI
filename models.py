from sqlalchemy import Column, Integer, String
from database import Base


class Todo(Base):
    __tablename__ = "Todo"
    id = Column(Integer, primary_key=True)
    task = Column(String(256))