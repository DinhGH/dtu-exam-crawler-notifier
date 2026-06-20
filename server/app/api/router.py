from fastapi import APIRouter
from app.api.routes import files, exam_schedules, subscriptions, auth, dashboard, users

api_router = APIRouter()

api_router.include_router(files.router, prefix="/files", tags=["Exam Files"])
api_router.include_router(exam_schedules.router, prefix="/exam-schedules", tags=["Exam Schedules"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
