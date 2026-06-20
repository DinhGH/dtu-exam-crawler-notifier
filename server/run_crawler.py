import sys
from app.scheduler.jobs import crawl_and_process_job
from app.utils.logger import log


def main():
    try:
        log.info("Starting crawler cron job...")
        crawl_and_process_job()
        log.info("Crawler cron job completed successfully.")
        sys.exit(0)

    except Exception:
        log.exception("Crawler cron job failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()