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
from app.services.crawler_service import CrawlerService
from fastapi.responses import RedirectResponse

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

@router.get("/{file_id}/download")
def download_exam_file(file_id: int, db: Session = Depends(get_db)):
    """
    Redirect to the direct download link of the exam file.
    """
    log.info(f"Getting download link for file_id: {file_id}")
    
    exam_file = db.query(ExamFile).filter(ExamFile.id == file_id).first()
    
    if not exam_file:
        log.warning(f"File with id {file_id} not found.")
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return a redirect to the direct download link
    return RedirectResponse(url=exam_file.download_link)

@router.get("/{file_id}", response_model=ExamFileDetailResponse)
def get_exam_file_detail(file_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the details of a specific exam file.
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

@router.post("/crawl")
def crawl_exam_files(
    crawl_latest_only: bool = Query(False, description="Delete existing data and crawl 100 most recent files only"),
    db: Session = Depends(get_db),
):
    """
    Trigger a manual crawl of exam files.
    """
    log.info(f"Triggering manual crawl with crawl_latest_only={crawl_latest_only}")
    
    try:
        crawler_service = CrawlerService(db)
        new_files = crawler_service.crawl_exam_files(crawl_latest_only=crawl_latest_only)
        
        return {
            "success": True,
            "message": f"Crawl completed. Found {len(new_files)} new files.",
            "new_files_count": len(new_files)
        }
    except Exception as e:
        log.error(f"Error during manual crawl: {e}")
        raise HTTPException(status_code=500, detail=str(e))
