from fastapi import APIRouter
from app.api.routes import files, exam_schedules

api_router = APIRouter()

api_router.include_router(files.router, prefix="/files", tags=["Exam Files"])
api_router.include_router(exam_schedules.router, prefix="/exam-schedules", tags=["Exam Schedules"])