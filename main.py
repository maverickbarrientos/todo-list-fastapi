
"""

Application Entry Point

Initializes the FastAPI application, sets up database tables, 
authentication, routes, and scheduled background tasks.

Features:
- JWT authentication and user registration via FastAPI Users
- Task management endpoints (CRUD operations)
- Asynchronous database sessions using SQLAlchemy AsyncSession
- Background notifications for pending tasks
- Scheduled jobs for resetting task notifications and sending alerts
- Lifespan management to create database tables on startup

Schedulers:
- `schedule_notification`: Sends notifications for pending tasks every minute
- `schedule_reset_notified_task`: Resets the `notified` flag for tasks every minute

Dependencies:
- `NotificationService` injected via FastAPI Depends
- Current active user obtained with `current_active_user`

"""


from fastapi import FastAPI, Depends

from contextlib import asynccontextmanager
from db.base import create_tables
from models.users import auth_backend, fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession

#ROUTES
from api.v1.tasks import tasks

#SCHEMAS
from schemas.user_schemas import UserRead, UserCreate

#DEPENDENCY
from services.notification_service import NotificationService
from db.session import get_session, session_maker
from models.users import fastapi_users, current_active_user
from fastapi_apscheduler.scheduler import AsyncIOScheduler
import asyncio

#MODELS
from db.base import User

def notification_dependency(session: AsyncSession = Depends(get_session)):
    return NotificationService(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

@asynccontextmanager
async def get_session_context():
    async with session_maker() as session:
        yield session
    
async def schedule_notification():
    async with get_session_context() as session:
        service = NotificationService(session)
        await service.notify_users()
        
async def schedule_reset_notified_task():
    async with get_session_context() as session:
        service = NotificationService(session)
        await service.reset_notified_tasks()

app = FastAPI(lifespan=lifespan)
scheduler = AsyncIOScheduler()

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])

app.include_router(tasks, tags=["tasks"], prefix="/tasks")

@app.on_event("startup")
async def notify_startup():  
    
    scheduler.add_job(
        func=schedule_reset_notified_task,
        trigger="interval",
        minutes=1,
        max_instances=1,
        misfire_grace_time=60,
        id="reset_notified_task"
    )
    
    scheduler.add_job(
        func=schedule_notification,
        trigger="interval",
        minutes=1,
        max_instances=1,
        misfire_grace_time=60,
        id="send_notification"
    )
    
    scheduler.start()
    
    return { "message" : "Notification schedulers started" }
    
@app.patch("/set_notification")
async def set_notification(
  setting: str,
  notification_dependency: NotificationService = Depends(notification_dependency),
  user: User = Depends(current_active_user)
):
    setting = await notification_dependency.set_notification(user.id, setting)
    
    return setting

@app.get("/")
def index():
    return {
        "message" : "Welcome to my To Do List API!",
        "developer" : "Maverick Jade Barrientos"
        }