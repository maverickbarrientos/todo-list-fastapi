
"""

User Schema

Validation of incoming data types from the request.
Ensures data types and structure matches 
the database fields

"""

from fastapi_users import schemas
from pydantic import BaseModel
import enum

class UserRead(schemas.BaseUser[int]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class NotificationEnum(enum.Enum):
    enabled = "enabled"
    disabled = "disabled"