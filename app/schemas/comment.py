from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 🔹 Base
class CommentBase(BaseModel):
    content: str


# 🔹 Create
class CommentCreate(CommentBase):
    task_id: int


# 🔹 Update
class CommentUpdate(BaseModel):
    content: Optional[str] = None


# 🔹 Response
class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True