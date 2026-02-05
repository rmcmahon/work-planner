"""Project request and response schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    """Create project schema"""

    name: str
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Project response schema"""

    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Project list response schema"""

    projects: List[ProjectResponse]
    total: int
