"""Authentication request and response schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    """Login request schema"""

    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""

    refresh_token: str


class UserInfo(BaseModel):
    """User information schema"""

    id: str
    username: str
    email: str
    display_name: Optional[str] = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response schema"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema"""

    sub: str
    exp: int
