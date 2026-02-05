"""Authentication middleware for JWT token verification"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.core.database import get_db
from app.models import User
from app.services import AuthService

security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Verify JWT token and return authenticated user.
    Can be used as a dependency in route handlers.
    """
    token = credentials.credentials
    payload = decode_token(token)
    user_id: str = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = AuthService.get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


def require_role(*allowed_roles):
    """
    Dependency to require specific user roles.
    Usage: @router.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """

    async def role_checker(current_user: User = Depends(verify_token)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker
