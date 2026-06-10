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
from app.services.subscription_service import SubscriptionService
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ExamFileResponse])
def get_exam_files(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=105),
    q: str | None = Query(None, description="Search query to match file name or subject code"),
):
    """
    Retrieve a paginated list of crawled exam files.
    Supports optional search by file name or exam subject code.
    """
    log.info(f"Fetching exam files: page={page}, page_size={page_size}, q={q!r}")
    
    query = db.query(ExamFile)
    
    # If a search query is provided, filter by file_name (case-insensitive)
    # and by exam_subject_code if that attribute exists on the model/table.
    if q and q.strip():
        q_val = f"%{q.strip()}%"
        try:
            # Try to filter by both file_name and exam_subject_code (if present)
            if hasattr(ExamFile, "exam_subject_code"):
                query = query.filter(
                    (ExamFile.file_name.ilike(q_val)) |
                    (ExamFile.exam_subject_code.ilike(q_val))
                )
            else:
                query = query.filter(ExamFile.file_name.ilike(q_val))
        except Exception:
            # Fallback: only filter by file_name if anything goes wrong
            query = query.filter(ExamFile.file_name.ilike(q_val))
    
    query = query.order_by(ExamFile.crawl_time.asc())
    
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
        
        # Process subscriptions after crawling
        subscription_service = SubscriptionService(db)
        processed_count = subscription_service.process_pending_subscriptions()
        log.info(f"Processed {processed_count} subscriptions after manual crawl.")
        
        return {
            "success": True,
            "message": f"Crawl completed. Found {len(new_files)} new files. Processed {processed_count} subscriptions.",
            "new_files_count": len(new_files),
            "processed_subscriptions": processed_count
        }
    except Exception as e:
        log.error(f"Error during manual crawl: {e}")
        raise HTTPException(status_code=500, detail=str(e))
