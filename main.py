from fastapi import FastAPI, Depends

from contextlib import asynccontextmanager
from db.base import create_tables
from models.users import auth_backend, fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession

#ROUTES
from api.v1.tasks import tasks

#SCHEMAS
from schemas.user_schemas import UserRead, UserCreate, UserUpdate

#DEPENDENCY
from services.notification_service import NotificationService
from db.session import get_session
from models.users import fastapi_users, current_active_user

#MODELS
from db.base import User

def notification_dependency(session: AsyncSession = Depends(get_session)):
    return NotificationService(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])

app.include_router(tasks, tags=["tasks"], prefix="/tasks")

@app.on_event("startup")
async def notify(
    notification_dependency: NotificationService = Depends(notification_dependency),
    user: User = Depends(current_active_user)
):
    result = await notification_dependency.notification(user)
    return { "message" : result}

@app.get("/get_user")
async def get_user(
    notification_dependency: NotificationService = Depends(notification_dependency),
    user: User = Depends(current_active_user)
):
    result = await notification_dependency.notification(user.id)
    return result
    
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
    
#REFLECTION 
#REMINDERS - If the task is overdue, notify user. If task is not done yet within the due date, it will notify the user
#CHATBOT 

#FRONTEND
#CHECKBOX 
#WIDGETS ON THE FRONTEND