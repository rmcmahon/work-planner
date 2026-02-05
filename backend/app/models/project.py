"""Project model for organizing tasks"""
from datetime import datetime
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
