from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.comment import Comment
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/comments", tags=["Comments"])

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

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check task ownership (via project)
    task = get_user_task(db, comment_data.task_id, current_user.id)

    new_comment = Comment(
        content=comment_data.content,
        task_id=comment_data.task_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/task/{task_id}", response_model=List[CommentResponse])
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Ensure user owns the task
    get_user_task(db, task_id, current_user.id)

    comments = db.query(Comment).filter(
        Comment.task_id == task_id
    ).all()

    return comments

@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    comment = db.query(Comment).join(Task).join(Project).filter(
        Comment.id == comment_id,
        Project.owner_id == current_user.id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.content = comment_data.content

    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    comment = db.query(Comment).join(Task).join(Project).filter(
        Comment.id == comment_id,
        Project.owner_id == current_user.id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    db.delete(comment)
    db.commit()

    return