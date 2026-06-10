from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.crawler_service import CrawlerService
from app.services.subscription_service import SubscriptionService
from app.utils.logger import log

def crawl_and_process_job():
    """
    Job tự động chạy định kỳ (mỗi 1 giờ):
    - Chỉ cào metadata (tên file, link download) để đồng bộ vào Database.
    - KHÔNG tự ý tải file về storage/excel để tránh lãng phí tài nguyên và tràn bộ nhớ.
    - Việc tải file sẽ do SubscriptionService tự kích hoạt khi có người dùng đăng ký trúng file.
    """
    log.info("Starting scheduled crawl job...")
    db: Session = SessionLocal()
    try:
        # Thực hiện cào thông tin danh sách môn thi mới từ cổng thông tin
        crawler_service = CrawlerService(db)
        new_files = crawler_service.crawl_exam_files(crawl_latest_only=True)
        
        if new_files:
            log.info(f"Successfully crawled and updated {len(new_files)} files to database.")
        else:
            log.info("No new exam files discovered on portal.")
        
        # Quét các đăng ký chờ sau khi cào file mới
        subscription_service = SubscriptionService(db)
        processed = subscription_service.process_pending_subscriptions()
        if processed > 0:
            log.info(f"Processed {processed} pending subscriptions after crawl.")

    except Exception as e:
        log.error(f"An error occurred in the crawl job: {e}")
    finally:
        db.close()
        log.info("Scheduled crawl job finished.")