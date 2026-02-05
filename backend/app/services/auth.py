"""Authentication and authorization services"""
import uuid
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models import User, UserRole


class AuthService:
    """Service for authentication and authorization operations"""

    @staticmethod
    def create_user(
        db: Session,
        username: str,
        email: str,
        password: str,
        display_name: Optional[str] = None,
        role: UserRole = UserRole.VIEWER,
    ) -> User:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=hash_password(password),
            display_name=display_name or username,
            role=role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = AuthService.get_user_by_username(db, username)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def generate_tokens(user: User) -> Dict[str, str]:
        """Generate access and refresh tokens for user"""
        access_token = create_access_token({"sub": user.id, "username": user.username})
        refresh_token = create_refresh_token({"sub": user.id})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def update_user_role(db: Session, user_id: str, new_role: UserRole) -> Optional[User]:
        """Update user role (admin only)"""
        user = AuthService.get_user_by_id(db, user_id)
        if user:
            user.role = new_role
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users (paginated)"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> Optional[User]:
        """Deactivate a user"""
        user = AuthService.get_user_by_id(db, user_id)
        if user:
            user.is_active = False
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def activate_user(db: Session, user_id: str) -> Optional[User]:
        """Activate a user"""
        user = AuthService.get_user_by_id(db, user_id)
        if user:
            user.is_active = True
            db.commit()
            db.refresh(user)
        return user
