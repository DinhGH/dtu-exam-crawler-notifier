from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.crawler_service import CrawlerService
from app.utils.logger import log, crawler_logger

def crawl_and_process_job():
    """
    Job to crawl for new exam files (every 1 hour).
    Deletes existing data and crawls 100 most recent files.
    """
    log.info("Starting scheduled crawl job...")
    db: Session = SessionLocal()
    try:
        # Crawl - always deletes existing data and crawls 100 files
        crawler_service = CrawlerService(db)
        new_files = crawler_service.crawl_exam_files(crawl_latest_only=True)
        
        if new_files:
            log.info(f"Successfully crawled {len(new_files)} new files.")
        else:
            log.info("No new files found.")

    except Exception as e:
        log.error(f"An error occurred in the crawl job: {e}")
    finally:
        db.close()
        log.info("Scheduled crawl job finished.")
