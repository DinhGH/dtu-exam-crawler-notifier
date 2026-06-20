from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.jobs import crawl_and_process_job
from app.utils.logger import log

scheduler = BackgroundScheduler(timezone="Asia/Saigon")

def start_scheduler():
    """
    Starts the scheduler and adds the jobs.
    """
    log.info("Starting scheduler...")
    if not scheduler.running:
        scheduler.add_job(
            crawl_and_process_job,
            "interval",
            minutes=4,
            id="crawl_and_process_job",
            replace_existing=True,
        )
        scheduler.start()
        log.info("Scheduler started successfully.")
    else:
        log.warning("Scheduler is already running.")

def stop_scheduler():
    """
    Stops the scheduler.
    """
    if scheduler.running:
        log.info("Stopping scheduler...")
        scheduler.shutdown()
        log.info("Scheduler stopped.")