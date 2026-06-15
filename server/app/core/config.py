from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BASE_URL: str = "https://pdaotao.duytan.edu.vn/"
    ALLOWED_ORIGINS: list[str] = ["*"]
    crawl_interval: int = 60  # seconds, optional override from .env

    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str | None = None
    SMTP_PASSWORD: str | None = None
    FROM_EMAIL: str | None = None
    FROM_NAME: str = "Hệ thống Thông báo Danh Sách Thi"

    class Config:
        env_file = ".env"

settings = Settings()
