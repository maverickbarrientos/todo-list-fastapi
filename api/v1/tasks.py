from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from db.session import get_session
from db.base import Tasks, User
from schemas.task_schema import TaskBase, TaskCreate, TaskResponse, TaskUpdate

from services.task_service import TaskService
from models.users import current_active_user

tasks = APIRouter()
#FINISH NOTIFICATION SERVICE AND NOTIFICATION LOGIC

#DEPENDENCIES
def task_service_dependency(session: AsyncSession = Depends(get_session)) -> TaskService:
    return TaskService(session)

@tasks.get("/", response_model=dict[str, list[TaskResponse]])
async def get_tasks(
    limit: int = 1, 
    category: Optional[str] = None,
    task_service: TaskService = Depends(task_service_dependency),
    user: User = Depends(current_active_user)
):
    
    tasks = await task_service.filter_tasks(category, limit, user.id)
    
    return { "tasks" : tasks }

@tasks.get("/get_task/{task_id}", response_model=dict[str, TaskResponse])
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(task_service_dependency),
    user: User = Depends(current_active_user)
):
    task = await task_service.get_task(task_id, user.id)
    return { "task" : task }
    
@tasks.post("/new_task", response_model=TaskResponse)
async def new_task(
    task: TaskCreate,
    task_service: TaskService = Depends(task_service_dependency),
    user: User = Depends(current_active_user)
):
    new_task = await task_service.new_task(task, user.id)
    return new_task

@tasks.patch("/update_task/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    task_service: TaskService = Depends(task_service_dependency),
    user: User = Depends(current_active_user)
):
    task = await task_service.task_update(task_id, payload, user.id)
    return task

@tasks.delete("/delete_task/{task_id}", response_model=dict[str, str])
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(task_service_dependency),
    user: User = Depends(current_active_user)
):
    task = await task_service.task_delete(task_id, user.id)
    
    return { "status" : task["status"]}


#FILTERING - DONE
#LIMITER - DONE
