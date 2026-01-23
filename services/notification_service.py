
"""

Notification Service

Manages all the notification-related logic for tasks.
Filters all of the pending and not notified tasks
for the specific user and sends the notification.

Sets the notified to false if the task is still pending
after notifying the user.


"""

from sqlalchemy import select, update
from db.base import Tasks
from datetime import datetime, timedelta, timezone, date
import asyncio, aiofiles

from db.base import User

class NotificationService():
    def __init__(self, session):
        self.session = session
            
    async def notify_users(self):
        
        stmt = select(User).where(User.notification_enabled == "enabled")
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        
        for user in users:
            await self._send_notification(user)
        
    async def _send_notification(self, user: User):
        
        if user.notification_enabled:
            
            print("Due Tasks!")
                        
            stmt = (update(Tasks)
                    .where(Tasks.user_id == user.id, 
                            Tasks.due_date >= date.today(), 
                            Tasks.notified == 0, 
                            Tasks.status != "done")
                    .values(notified=1, last_notified=datetime.now()))
            
            await self.session.execute(stmt)
            await self.session.commit()
            
            asyncio.create_task(self.write_notification(user.email))

        return "notification sent!"
    
    async def _write_notification(email: str, message="Hello, World!"):
        async with aiofiles.open("log.txt", mode="a") as email_file:
            content = f"notification for {email}: {message}"
            await email_file.write(content)
    
    async def reset_notified_tasks(self):
        
        threshold = datetime.now(timezone.utc) - timedelta(minutes=1)
        
        stmt = (update(Tasks)
                .where(Tasks.notified == 1, 
                       Tasks.due_date <= datetime.now(timezone.utc),
                        Tasks.last_notified <= threshold)
                .values(notified=0)
                )
        await self.session.execute(stmt)
        await self.session.commit()
        
        return { "message" : "Task running" }
            
    async def set_notification(self, user_id, setting):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        setattr(user, "notification_enabled", setting)
        
        await self.session.commit()
        await self.session.refresh(user)
        
        return user