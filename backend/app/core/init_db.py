"""Database initialization and seeding"""
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.auth import AuthService
from app.models import User, UserRole


def init_db(db: Session):
    """Initialize database with default data"""
    # Check if admin user already exists
    admin_user = AuthService.get_user_by_username(db, settings.admin_username)
    
    if admin_user is None:
        # Create default admin user
        AuthService.create_user(
            db=db,
            username=settings.admin_username,
            email=settings.admin_email,
            password=settings.admin_password,
            display_name="Administrator",
            role=UserRole.ADMIN,
        )
        print(f"✓ Created default admin user: {settings.admin_username}")
    else:
        print(f"✓ Admin user already exists: {settings.admin_username}")


def reset_db(db: Session):
    """Reset database (drop and recreate all tables with seeding)"""
    from app.core.database import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db(db)
    print("✓ Database reset complete")
