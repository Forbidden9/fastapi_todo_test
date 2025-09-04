from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from api.task.enum import StateTask


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    state: StateTask

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)
