__all__ = [
    "User",
    "Base",
    "Ref",
]

# Про ORM-паттерн асинхронного sqlalchemy и модели
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm

# декларативная модель базы данных python
# https://metanit.com/python/database/3.2.php
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DATE, Integer, VARCHAR, DateTime
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=False)
    reg_date = Column(DATE, default=datetime.now())
    yatoken = Column(VARCHAR(64), unique=False, nullable=True)
    status = Column(VARCHAR (8), unique=False, nullable=False)
    
class Ref(Base):
    __tablename__ = "ref_table"
    
    user_id = Column(Integer, primary_key=True)
    refferer_id = Column(Integer, unique=False, nullable=True)
    
class Folder(Base):
    __tablename__ = "folder_table"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=False, nullable=False)
    folder_path = Column(VARCHAR(64), unique=False, nullable=False)
    check_date = Column(DateTime, default=datetime.now(timezone.utc), unique=False)