from fastapi import Depends
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum, Text, SmallInteger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, relationship
from schemas.task_schema import TaskEnum
from schemas.user_schemas import NotificationEnum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase, mapped_column, Mapped

from db.session import get_session, engine

from datetime import date, datetime

class Base(DeclarativeBase):
    pass

class Tasks(Base):
    __tablename__ = "tasks"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    task_name: str = Column(String(255))
    description: str = Column(Text)
    category: str = Column(String(255))
    date_created: date = Column(DateTime, default=datetime.now())
    due_date: date = Column(Date)   
    status: TaskEnum = Column(Enum(TaskEnum))
    notified: int = Column(SmallInteger, default=0)
    last_notified: datetime = Column(DateTime)
    
    user = relationship("User", back_populates="tasks")
        
class UserInformation(Base):
    __tablename__ = "user_information"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    profile_url = Column(String(255))
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    
    user = relationship("User", back_populates="user_information")
    
class User(SQLAlchemyBaseUserTable, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notification_enabled: Mapped[str] = mapped_column(Enum(NotificationEnum), default="disabled")
    
    tasks = relationship("Tasks", back_populates="user")
    user_information = relationship("UserInformation", back_populates="user")
    
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
        
hello_world = "Hello, World!"