"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decode_token, create_access_token
from app.schemas import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse, UserInfo
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login endpoint - authenticate user and return JWT tokens.
    
    **Request body:**
    - `username`: User username
    - `password`: User password
    
    **Returns:**
    - `access_token`: JWT access token (valid for 30 minutes)
    - `refresh_token`: JWT refresh token (valid for 7 days)
    - `token_type`: Always "bearer"
    - `user`: User information (id, username, email, role)
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens
    tokens = AuthService.generate_tokens(user)

    return LoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            role=user.role.value,
            is_active=user.is_active,
        ),
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.
    
    **Request body:**
    - `refresh_token`: Valid refresh token from login
    
    **Returns:**
    - `access_token`: New JWT access token
    - `token_type`: Always "bearer"
    """
    try:
        payload = decode_token(request.refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user = AuthService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Generate new access token
        access_token = create_access_token(
            {"sub": user.id, "username": user.username},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )

        return RefreshTokenResponse(
            access_token=access_token,
            token_type="bearer",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
