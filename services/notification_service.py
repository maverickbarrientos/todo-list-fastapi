from sqlalchemy import select
from db.base import Tasks
from datetime import datetime
import asyncio

from db.base import User

"""
------------------- NOTIFICATION SYSTEM LOGIC -------------------

1️⃣ Database & Models:
    - User model:
        * notification_enabled (bool) → is the user opted-in for notifications
    - Task model:
        * due_time (datetime) → when the task is due
        * notified (bool) → whether the notification has already been sent
        * last_notified_at (datetime) → timestamp of the last notification

2️⃣ Authentication:
    - Use FastAPI's `current_user` dependency
    - Only proceed if current_user exists and current_user.id is valid

3️⃣ Scheduler / Background Task:
    - Runs periodically (recommended 30s–1min)
    - NOT every 1 second to avoid spamming
    - Can be implemented using BackgroundTasks or APScheduler

4️⃣ Notification Logic:
    - Fetch users with notification_enabled=True
    - For each user:
        * Fetch tasks where due_time <= now()
        * For each task:
            - Check notified or last_notified_at
            - Send notification if eligible
            - Update task: set notified=True or last_notified_at=now()

5️⃣ Reset Logic (Recurring Notifications):
    - Periodically check tasks where last_notified_at <= now() - 24h
    - Reset task.notified = False
    - Ensures daily reminders can be sent again

6️⃣ Services & Responsibilities:
    - TaskService:
        * Queries due tasks
        * Checks and updates notified / last_notified_at
    - NotificationService:
        * Sends notifications to users
    - Scheduler:
        * Orchestrates fetching users and calling services

7️⃣ Optional Enhancements:
    - Make timestamps timezone-aware
    - Configurable reminder intervals per user
    - Optimize DB queries with bulk updates for multiple tasks

------------------- END OF NOTIFICATION SYSTEM LOGIC -------------------
"""


class NotificationService():
    def __init__(self, session):
        self.session = session
            
    async def get_due_tasks(self):
        stmt = select(Tasks).where(Tasks.due_date >= datetime)
        result = await self.session.execute(stmt)
        
        return result.scalars().all()
        
    async def notification(self, user_id):
        
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        print(user)
                        
        # while True:
        #     if user.notification_enabled:
        #         due_tasks = await self.get_due_tasks()
                
        #         print(due_tasks)
        #         return due_tasks
            
        #     await asyncio.sleep(1)
        
        return user
            
    async def set_notification(self, user_id, setting):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        setattr(user, "notification_enabled", setting)
        
        await self.session.commit()
        await self.session.refresh(user)
        
        return user