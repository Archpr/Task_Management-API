from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReminderBase(BaseModel):
    remind_at: datetime


class ReminderCreate(ReminderBase):
    task_id: int


class ReminderUpdate(BaseModel):
    remind_at: Optional[datetime] = None


class ReminderResponse(BaseModel):
    id: int
    remind_at: datetime

    task_id: int
    user_id: int


    class Config:
        from_attributes = True