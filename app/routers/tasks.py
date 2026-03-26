from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# 🔹 Helper: get task owned by current user (via project)
def get_user_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


# 🔹 Create Task
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check project ownership
    project = db.query(Project).filter(
        Project.id == task_data.project_id,
        Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add tasks to this project"
        )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        assigned_to_id=task_data.assigned_to_id,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_by_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# 🔹 Get Tasks (optionally filter by project)
@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Task).join(Project).filter(
        Project.owner_id == current_user.id
    )

    if project_id:
        query = query.filter(Task.project_id == project_id)

    return query.all()


# 🔹 Get Single Task
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_user_task(db, task_id, current_user.id)


# 🔹 Update Task
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = get_user_task(db, task_id, current_user.id)

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    if task_data.assigned_to_id is not None:
        task.assigned_to_id = task_data.assigned_to_id

    db.commit()
    db.refresh(task)

    return task


# 🔹 Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = get_user_task(db, task_id, current_user.id)

    db.delete(task)
    db.commit()

    return