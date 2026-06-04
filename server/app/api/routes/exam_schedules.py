from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.exam_schedule import ExamSchedule
from app.schemas.exam import PaginatedResponse, ExamScheduleResponse
from app.utils.logger import log

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ExamScheduleResponse])
def search_exam_schedules(
    db: Session = Depends(get_db),
    student_name: str = Query(None, description="Search by student name"),
    student_id: str = Query(None, description="Search by student ID"),
    subject_code: str = Query(None, description="Search by subject code"),
    subject_name: str = Query(None, description="Search by subject name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=105),
):
    """
    Search for exam schedules with pagination.
    """
    log.info(f"Searching exam schedules with queries: student_name={student_name}, student_id={student_id}, subject_code={subject_code}, subject_name={subject_name}")
    
    query = db.query(ExamSchedule)
    
    if student_name:
        query = query.filter(ExamSchedule.student_name.ilike(f"%{student_name}%"))
    if student_id:
        query = query.filter(ExamSchedule.student_id.ilike(f"%{student_id}%"))
    if subject_code:
        query = query.filter(ExamSchedule.subject_code.ilike(f"%{subject_code}%"))
    if subject_name:
        query = query.filter(ExamSchedule.subject_name.ilike(f"%{subject_name}%"))
        
    total = query.count()
    items = query.order_by(ExamSchedule.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items,
    }