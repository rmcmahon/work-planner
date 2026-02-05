"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration"""

    # Database
    database_url: str = "sqlite:///./planner.db"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Application
    environment: str = "development"
    debug: bool = True
    app_name: str = "Planner API"
    api_version: str = "v1"

    # Admin seed user
    admin_username: str = "admin"
    admin_password: str = "p@ssw0rd!"
    admin_email: str = "admin@planner.local"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
