"""API router configuration"""
from fastapi import APIRouter
from app.api.endpoints import auth

# Create main router
router = APIRouter(prefix="/api/v1")

# Include endpoint routers
router.include_router(auth.router)
