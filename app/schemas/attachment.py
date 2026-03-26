from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AttachmentBase(BaseModel):
    file_name: str
    file_url: str


class AttachmentCreate(AttachmentBase):
    task_id: int


class AttachmentResponse(BaseModel):
    id: int
    file_name: str
    file_url: str
    task_id: int
    uploaded_by_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True