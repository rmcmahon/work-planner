"""Task endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import verify_token
from app.models import User, TaskPriority, TaskStatus
from app.schemas import TaskResponse, TaskListResponse, TaskCreate, TaskUpdate, TaskReorderRequest
from app.services import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse)
def list_tasks(
    owner_id: Optional[str] = Query(None, description="Filter by task owner"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    status: Optional[str] = Query(None, description="Filter by status (todo, in_progress, in_review, done)"),
    project_id: Optional[str] = Query(None, description="Filter by project"),
    delivery_date_from: Optional[datetime] = Query(None, description="Filter tasks with delivery >= date"),
    delivery_date_to: Optional[datetime] = Query(None, description="Filter tasks with delivery <= date"),
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """
    Get all tasks with optional filtering.
    
    **Query Parameters:**
    - `owner_id`: Filter by task owner ID
    - `priority`: Filter by priority (low, medium, high)
    - `status`: Filter by status (todo, in_progress, in_review, done)
    - `project_id`: Filter by project ID
    - `delivery_date_from`: Filter tasks with delivery >= date (ISO format)
    - `delivery_date_to`: Filter tasks with delivery <= date (ISO format)
    
    **Returns:**
    - `tasks`: List of tasks ordered by priority DESC, position ASC
    - `total`: Total number of tasks matching filters
    
    Tasks are ordered by:
    1. Priority (HIGH → MEDIUM → LOW)
    2. Position (for manual ordering/drag-drop)
    """
    # Build filter dictionary
    filters = {}
    
    if owner_id:
        filters["owner_id"] = owner_id
    
    if priority:
        try:
            filters["priority"] = TaskPriority(priority.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid priority: {priority}",
            )
    
    if status:
        try:
            filters["status"] = TaskStatus(status.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}",
            )
    
    if project_id:
        filters["project_id"] = project_id
    
    if delivery_date_from:
        filters["delivery_date_from"] = delivery_date_from
    
    if delivery_date_to:
        filters["delivery_date_to"] = delivery_date_to
    
    # Get filtered and ordered tasks
    tasks = TaskService.filter_tasks(db, filters)
    
    # Convert to response schema
    task_responses = [TaskResponse.from_orm(task) for task in tasks]
    
    return TaskListResponse(
        tasks=task_responses,
        total=len(tasks),
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """
    Create a new task.
    
    **Request Body:**
    - `name`: Task name (required)
    - `description`: Task description (optional)
    - `priority`: Priority level (low, medium, high)
    - `project_id`: Project ID (required)
    - `delivery_date`: Delivery date (optional, ISO format)
    - `status`: Task status (todo, in_progress, in_review, done)
    - `parent_task_id`: Parent task ID for subtasks (optional)
    
    **Returns:** Created task with ID and timestamps
    """
    try:
        # Convert string enums to model enums
        priority = TaskPriority(task_data.priority.lower())
        status = TaskStatus(task_data.status.lower())
        
        task = TaskService.create_task(
            db=db,
            name=task_data.name,
            description=task_data.description,
            priority=priority,
            owner_id=current_user.id,
            project_id=task_data.project_id,
            delivery_date=task_data.delivery_date,
            status=status,
            parent_task_id=task_data.parent_task_id,
            created_by=current_user.id,
        )
        
        return TaskResponse.from_orm(task)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """
    Update a task.
    
    **Path Parameters:**
    - `task_id`: Task ID
    
    **Request Body:**
    - `name`: New task name (optional)
    - `description`: New task description (optional)
    - `priority`: New priority (optional)
    - `status`: New status (optional)
    - `delivery_date`: New delivery date (optional)
    
    **Returns:** Updated task
    """
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check if user can edit this task
    from app.services import Permission
    if not Permission.can_edit_task(current_user, task.owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this task",
        )
    
    try:
        update_data = task_data.dict(exclude_unset=True)
        
        # Convert enum strings to enum values
        if "priority" in update_data and update_data["priority"]:
            update_data["priority"] = TaskPriority(update_data["priority"].lower())
        
        if "status" in update_data and update_data["status"]:
            update_data["status"] = TaskStatus(update_data["status"].lower())
        
        task = TaskService.update_task(db, task_id, **update_data)
        return TaskResponse.from_orm(task)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/{task_id}/position", response_model=TaskResponse)
def reorder_task(
    task_id: str,
    request: TaskReorderRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """
    Reorder a task and optionally change its parent (for drag-drop, make-subtask).
    
    **Path Parameters:**
    - `task_id`: Task ID
    
    **Request Body:**
    - `position`: New position (float, allows fractional insertion)
    - `parent_task_id`: New parent task ID (optional, null to remove parent)
    
    **Returns:** Updated task with new position/parent
    """
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check if user can edit this task
    from app.services import Permission
    if not Permission.can_edit_task(current_user, task.owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to reorder this task",
        )
    
    try:
        task = TaskService.reorder_task(
            db=db,
            task_id=task_id,
            new_position=request.position,
            new_parent_id=request.parent_task_id,
        )
        return TaskResponse.from_orm(task)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """
    Delete a task (soft delete - marks as deleted).
    Admin only.
    
    **Path Parameters:**
    - `task_id`: Task ID
    """
    from app.services import Permission
    
    if not Permission.can_delete_task(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete tasks",
        )
    
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    TaskService.soft_delete_task(db, task_id)
    return None
