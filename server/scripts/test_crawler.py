import sys
import os
# Ensure 'server' package is importable when running this script from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.services.crawler_service import CrawlerService

def main():
    db = SessionLocal()
    try:
        crawler = CrawlerService(db)
        files = crawler.crawl_exam_files()
        print(f"\nTotal new files found: {len(files)}")
        for f in files:
            print(f" - {f.title}: {f.file_name}")
    finally:
        db.close()

if __name__ == "__main__":
    main()