"""API router configuration"""
from fastapi import APIRouter

# Create main router
router = APIRouter(prefix="/api/v1")

# Placeholder for endpoint routers - will be added in Phase 2
# from app.api.endpoints import auth, tasks, admin
#
# router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
# router.include_router(admin.router, prefix="/admin", tags=["Admin"])
