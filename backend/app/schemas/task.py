"""Task request and response schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskCreate(BaseModel):
    """Create task schema"""

    name: str
    description: Optional[str] = None
    priority: str = "medium"
    project_id: str
    delivery_date: Optional[datetime] = None
    status: str = "todo"
    parent_task_id: Optional[str] = None


class TaskUpdate(BaseModel):
    """Update task schema"""

    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    delivery_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    """Task response schema"""

    id: str
    name: str
    description: Optional[str] = None
    priority: str
    owner_id: str
    project_id: str
    delivery_date: Optional[datetime] = None
    status: str
    parent_task_id: Optional[str] = None
    position: float
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Task list response schema"""

    tasks: List[TaskResponse]
    total: int


class TaskReorderRequest(BaseModel):
    """Task reorder/reparent request schema"""

    position: float
    parent_task_id: Optional[str] = None
