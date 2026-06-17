from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_stats()

@router.get("/files-over-time")
def get_files_over_time(db: Session = Depends(get_db)):
    service = DashboardService(db)
    results = service.get_files_over_time()
    return [{"date": str(r.date), "count": r.count} for r in results]

@router.get("/emails-over-time")
def get_emails_over_time(db: Session = Depends(get_db)):
    service = DashboardService(db)
    results = service.get_emails_over_time()
    return [{"date": str(r.date), "count": r.count} for r in results]