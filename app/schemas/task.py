from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# 🔹 Base (shared fields)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None
    assigned_to_id: Optional[int] = None


# 🔹 Create
class TaskCreate(TaskBase):
    project_id: int


# 🔹 Update (PATCH-style)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    assigned_to_id: Optional[int] = None



# 🔹 Response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[date]
    project_id: int
    assigned_to_id: Optional[int]
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True  # for SQLAlchemy (Pydantic v2)

  