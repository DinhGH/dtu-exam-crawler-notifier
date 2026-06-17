from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. Import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.router import api_router
from app.scheduler.scheduler import start_scheduler, stop_scheduler
from app.utils.logger import log
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    log.info("Creating database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    log.info("Tables created successfully (if not already present).")
    start_scheduler()
    yield
    log.info("Shutting down...")
    stop_scheduler()

app = FastAPI(lifespan=lifespan)

# 3. Thêm CORSMiddleware vào ứng dụng của bạn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],            # Cho phép các origin được cấu hình
    allow_credentials=True,
    allow_methods=["*"],              # Cho phép tất cả các HTTP Methods (GET, POST, PUT, DELETE,...)
    allow_headers=["*"],              # Cho phép tất cả các Headers gửi lên (Content-Type, Authorization,...)
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "DTU Exam Notifier API",
        "status": "running"
    }