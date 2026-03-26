from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.attachment import Attachment
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.attachment import AttachmentCreate, AttachmentResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/attachments", tags=["Attachments"])


def get_user_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
def create_attachment(
    attachment_data: AttachmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    get_user_task(db, attachment_data.task_id, current_user.id)

    new_attachment = Attachment(
        file_name=attachment_data.file_name,
        file_url=attachment_data.file_url,
        task_id=attachment_data.task_id,
        uploaded_by_id=current_user.id
    )

    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)

    return new_attachment


@router.get("/task/{task_id}", response_model=List[AttachmentResponse])
def get_attachments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    get_user_task(db, task_id, current_user.id)

    return db.query(Attachment).filter(
        Attachment.task_id == task_id
    ).all()


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    attachment = db.query(Attachment).join(Task).join(Project).filter(
        Attachment.id == attachment_id,
        Project.owner_id == current_user.id
    ).first()

    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    db.delete(attachment)
    db.commit()

    return