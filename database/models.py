from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)
    vless_key = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String)
    status = Column(String, default="pending")