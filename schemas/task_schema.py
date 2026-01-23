
"""

Task Schema

Defines data validation.
Ensuring incoming requests have the correct data types
and structure matching to database fields.


"""


from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import enum

class TaskEnum(enum.Enum):
    pending = "pending"
    done = "done"

class TaskBase(BaseModel):
    task_name: str
    description: Optional[str]
    category: str
    date_created: datetime = datetime.now()
    due_date: date
    status: TaskEnum = TaskEnum.pending

    
class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    user_id: int
    notified: int
    last_notified: Optional[datetime] = None

class TaskUpdate(BaseModel):
    user_id: Optional[int] = None
    task_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    date_created: Optional[datetime] = None
    due_date: Optional[date] = None
    status: Optional[TaskEnum]