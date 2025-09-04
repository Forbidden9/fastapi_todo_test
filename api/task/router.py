from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.task import repository
from api.task.schema import Task, TaskCreate, TaskUpdate

from api.user.model import User
from core.database.session import get_db
from core.oauth.oauth import get_current_user
from core.settings.logging import setup_logging

task = APIRouter()
logger = setup_logging()


@task.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Creating a new task to user: {current_user.username}")
    return repository.create_user_task(db=db, task=task, user_id=current_user.id)

@task.get("/tasks", response_model=List[Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Listing tasks for user: {current_user.username}")
    tasks = repository.get_user_tasks(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@task.get("/tasks/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Getting task {task_id} to user: {current_user.username}")
    task = repository.get_task(db, task_id=task_id)
    if not task:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        logger.warning(f"User {current_user.username} tried to access task {task_id} not his own")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permissions to access this task")
    return task

@task.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Updating task {task_id} to user: {current_user.username}")
    task = repository.get_task(db, task_id=task_id)
    if not task:
        logger.warning(f"Task {task_id} not found to update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        logger.warning(f"User {current_user.username} tried to update task {task_id} not his own")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permissions to update this task")
    return repository.update_task(db=db, task_id=task_id, task_update=task_update)

@task.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Deleting task {task_id} to user: {current_user.username}")
    task = repository.get_task(db, task_id=task_id)
    if not task:
        logger.warning(f"Task {task_id} not found to delete")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        logger.warning(f"User {current_user.username} tried to delete task {task_id} not his own")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permissions to delete this task")
    repository.delete_task(db=db, task_id=task_id)
    return None
