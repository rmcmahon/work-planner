"""User model for authentication and authorization"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, Index, Enum as SQLEnum
from sqlalchemy.dialects.sqlite import JSON
from app.core.database import Base


class UserRole(str, Enum):
    """User role enumeration for access control"""
    VIEWER = "viewer"
    WORKER = "worker"
    ADMIN = "admin"


class User(Base):
    """User model for authentication and role-based access control"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Metadata for future extensibility
    metadata_json = Column(JSON, default={}, nullable=False)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
        Index('idx_user_is_active', 'is_active'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
