from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str
    
    # Email Configuration
    smtp_email: str
    smtp_password: str
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    # Application
    app_name: str = "DTU Exam Crawler Notifier"
    debug: bool = False
    
    # Crawler settings
    crawl_interval: int = 60  # minutes

    class Config:
        env_file = ".env"


settings = Settings()
