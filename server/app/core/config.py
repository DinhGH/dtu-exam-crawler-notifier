from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BASE_URL: str = "https://pdaotao.duytan.edu.vn/"
    crawl_interval: int = 60  # seconds, optional override from .env

    class Config:
        env_file = ".env"

settings = Settings()
