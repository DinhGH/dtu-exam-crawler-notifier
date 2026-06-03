from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BASE_URL: str = "https://pdaotao.duytan.edu.vn/"

    class Config:
        env_file = ".env"

settings = Settings()