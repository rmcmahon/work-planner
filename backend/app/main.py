"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.init_db import init_db
from app.api import router

# Import models to register them with SQLAlchemy
from app.models import User, Task, Project, TaskAudit  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"Starting {settings.app_name} - Environment: {settings.environment}")
    Base.metadata.create_all(bind=engine)
    
    # Initialize database with default data
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Team Task Manager REST API",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.environment}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
