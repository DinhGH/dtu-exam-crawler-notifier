from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.schemas.exam import (
    ExamFileResponse,
    ExamFileDetailResponse,
    PaginatedResponse,
)
from app.utils.logger import log

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ExamFileResponse])
def get_exam_files(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """
    Retrieve a paginated list of crawled exam files.
    """
    log.info(f"Fetching exam files: page={page}, page_size={page_size}")
    
    query = db.query(ExamFile).order_by(ExamFile.crawl_time.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items,
    }

@router.get("/{file_id}", response_model=ExamFileDetailResponse)
def get_exam_file_detail(file_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the details of a specific exam file, including the total number of records.
    """
    log.info(f"Fetching details for file_id: {file_id}")
    
    exam_file = db.query(ExamFile).filter(ExamFile.id == file_id).first()
    
    if not exam_file:
        log.warning(f"File with id {file_id} not found.")
        raise HTTPException(status_code=404, detail="File not found")
        
    total_records = db.query(ExamSchedule).filter(ExamSchedule.exam_file_id == file_id).count()
    
    return ExamFileDetailResponse(
        **exam_file.__dict__,
        total_records=total_records
    )