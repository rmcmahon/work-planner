"""Task audit model for tracking task changes""""""Project model for organizing tasks"""




























        return f"<TaskAudit(id={self.id}, task_id={self.task_id}, action={self.action})>"    def __repr__(self):    )        Index('idx_task_audit_timestamp', 'timestamp'),        Index('idx_task_audit_user_id', 'user_id'),        Index('idx_task_audit_task_id', 'task_id'),    __table_args__ = (    # Indexes    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)    new_value = Column(String(500), nullable=True)    old_value = Column(String(500), nullable=True)    field_changed = Column(String(100), nullable=True)  # field name if action is update    action = Column(String(50), nullable=False)  # create, update, delete, move    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)    task_id = Column(String(36), ForeignKey('tasks.id'), nullable=False, index=True)    id = Column(String(36), primary_key=True, index=True)    __tablename__ = "task_audits"    """Audit trail for task changes"""class TaskAudit(Base):from app.core.database import Basefrom sqlalchemy import Column, String, DateTime, Index, ForeignKeyfrom datetime import datetimefrom datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    """Project model for grouping and organizing tasks"""
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metadata for future extensibility
    metadata_json = Column(JSON, default={}, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_project_name', 'name'),
    )

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"
