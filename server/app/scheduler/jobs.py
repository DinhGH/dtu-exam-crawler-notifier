from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.crawler_service import CrawlerService
from app.services.excel_service import ExcelService
from app.utils.logger import log, crawler_logger

def crawl_and_process_job():
    """
    Job to crawl for new exam files and process them.
    """
    log.info("Starting scheduled crawl and process job...")
    db: Session = SessionLocal()
    try:
        # Step 1: Crawl for new exam files
        crawler_service = CrawlerService(db)
        new_files = crawler_service.crawl_exam_files()

        # Step 2: Process each new file
        if new_files:
            excel_service = ExcelService(db)
            for exam_file in new_files:
                excel_service.process_exam_file(exam_file)
            log.info(f"Successfully processed {len(new_files)} new files.")
        else:
            log.info("No new files to process.")

    except Exception as e:
        log.error(f"An error occurred in the crawl and process job: {e}")
    finally:
        db.close()
        log.info("Scheduled job finished.")