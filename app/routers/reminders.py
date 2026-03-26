from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.reminder import Reminder
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/reminders", tags=["Reminders"])


def get_user_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    get_user_task(db, reminder_data.task_id, current_user.id)

    new_reminder = Reminder(
        remind_at=reminder_data.remind_at,
        task_id=reminder_data.task_id,
        user_id=current_user.id
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    return new_reminder


@router.get("/task/{task_id}", response_model=List[ReminderResponse])
def get_reminders(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    get_user_task(db, task_id, current_user.id)

    return db.query(Reminder).filter(
        Reminder.task_id == task_id
    ).all()


@router.patch("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    reminder = db.query(Reminder).join(Task).join(Project).filter(
        Reminder.id == reminder_id,
        Project.owner_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    if reminder_data.remind_at is not None:
        reminder.remind_at = reminder_data.remind_at

    db.commit()
    db.refresh(reminder)

    return reminder


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    reminder = db.query(Reminder).join(Task).join(Project).filter(
        Reminder.id == reminder_id,
        Project.owner_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()

    return