from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.router import api_router
from app.scheduler.scheduler import start_scheduler, stop_scheduler
from app.utils.logger import log

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

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "DTU Exam Notifier API",
        "status": "running"
    }
