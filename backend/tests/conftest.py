"""Test fixtures and utilities"""
import pytest


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)


@pytest.fixture
def db():
    """Create test database session"""
    from app.core.database import SessionLocal, Base, engine
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_user(db):
    """Create admin test user"""
    from app.core.security import hash_password
    from app.models.user import User  # To be created in Phase 2
    
    admin = User(
        username="admin",
        email="admin@test.local",
        password_hash=hash_password("p@ssw0rd!"),
        role="admin",
        is_active=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
