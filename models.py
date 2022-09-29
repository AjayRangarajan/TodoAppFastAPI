from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    username = Column(String(256), unique=True)
    password = Column(String(256))
    todos = relationship(
        "Todo",
        cascade="all,delete-orphan",
        back_populates="user",
        uselist=True,
    )

class Todo(Base):
    __tablename__ = "Todo"
    id = Column(Integer, primary_key=True)
    task = Column(String(512))
    user_id = Column(Integer(), ForeignKey('User.id'), nullable=False)
    user = relationship("User", back_populates="todos")