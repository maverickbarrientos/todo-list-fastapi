
"""

Task Service

Handles the task-related database operation such as creating, retrieving,
updating, and deletion of tasks.

Raises client-facing HTTPExceptions for
invalid operations or rule violations.


"""


from fastapi import HTTPException
from sqlalchemy import select, delete
from db.base import Tasks

from schemas.task_schema import TaskResponse, TaskCreate, TaskUpdate


class TaskService():
    def __init__(self, session):
        self.session = session
        

    async def filter_tasks(self, category: str, limit: int, user_id: int) -> list[TaskResponse]:
        
        stmt = select(Tasks).where(Tasks.user_id == user_id).limit(limit)
                
        if limit < 0:
            raise HTTPException(status_code=400, detail="Limit must be positive")
        
        if category and limit > 0:
            stmt = select(Tasks).where(Tasks.user_id == user_id, Tasks.category == category).limit(limit)
        
        result = await self.session.execute(stmt)
        task = result.scalars().all()

        return task

    async def get_task(self, task_id: int, user_id: int) -> TaskResponse:
                
        stmt = select(Tasks).where(Tasks.id == task_id and Tasks.user_id == user_id)
        result = await self.session.execute(stmt)
        
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return task
    
    async def new_task(self, task_model: TaskCreate, user_id: int) -> TaskResponse:
                
        new_task = Tasks(**task_model.model_dump(), user_id=user_id)
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        
        return new_task
    
    async def task_update(self, task_id: int, payload: TaskUpdate, user_id: int) -> TaskResponse:
                
        stmt = select(Tasks).where(Tasks.id == task_id and Tasks.user_id == user_id)
        result = await self.session.execute(stmt)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
            
        await self.session.commit()
        await self.session.refresh(task)
        
        return task
    
    async def task_delete(self, task_id: int, user_id: int):
        
        if not task_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        stmt = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        
        return { "status" : "deleted" }