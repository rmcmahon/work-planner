"""Task model for task management"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, Index, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    """Task status enumeration"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class Task(Base):
    """Task model for task management and hierarchical subtasks"""
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False, index=True)
    delivery_date = Column(DateTime, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    
    # Subtask hierarchy: self-referential foreign key for parent-child relationships
    parent_task_id = Column(String(36), ForeignKey('tasks.id'), nullable=True)
    
    # Position for manual ordering (float allows fractional insertion for drag-drop)
    position = Column(Float, nullable=False, default=0.0)
    
    # Soft delete support
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Audit trail
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=False)  # User ID who created this task
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], backref="owned_tasks")
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")
    project = relationship("Project", back_populates="tasks")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_task_owner_id', 'owner_id'),
        Index('idx_task_project_id', 'project_id'),
        Index('idx_task_priority', 'priority'),
        Index('idx_task_status', 'status'),
        Index('idx_task_delivery_date', 'delivery_date'),
        Index('idx_task_parent_task_id', 'parent_task_id'),
        Index('idx_task_is_deleted', 'is_deleted'),
        Index('idx_task_created_at', 'created_at'),
        # Composite index for ordering dashboard tasks
        Index('idx_task_priority_position', 'priority', 'position'),
    )

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, priority={self.priority}, status={self.status})>"
