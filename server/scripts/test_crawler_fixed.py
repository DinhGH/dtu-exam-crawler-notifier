#!/usr/bin/env python3
"""
Test script for the updated crawler service.
This script tests the new crawler logic that stores only links instead of downloading files.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.exam_file import ExamFile
from app.services.crawler_service import CrawlerService

def test_crawler():
    """Test the crawler service."""
    print("Testing updated crawler service...")
    
    # Create database tables if they don't exist
    ExamFile.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Create crawler service
        crawler_service = CrawlerService(db)
        
        # Test crawling without deleting existing data
        print("\n1. Testing crawl_exam_files(crawl_latest_only=False)...")
        new_files = crawler_service.crawl_exam_files(crawl_latest_only=False)
        print(f"Found {len(new_files)} new files")
        
        if new_files:
            for i, file in enumerate(new_files[:3], 1):
                print(f"\n  File {i}:")
                print(f"    ID: {file.id}")
                print(f"    File name: {file.file_name}")
                print(f"    Download link: {file.download_link}")
                print(f"    Crawl time: {file.crawl_time}")
        
        # Count total files in database
        total_files = db.query(ExamFile).count()
        print(f"\nTotal files in database: {total_files}")
        
        # Test crawling with deleting existing data (500 most recent)
        print("\n2. Testing crawl_exam_files(crawl_latest_only=True)...")
        new_files = crawler_service.crawl_exam_files(crawl_latest_only=True)
        print(f"Added {len(new_files)} new files (after deleting old data)")
        
        if new_files:
            for i, file in enumerate(new_files[:3], 1):
                print(f"\n  File {i}:")
                print(f"    ID: {file.id}")
                print(f"    File name: {file.file_name[:100]}...")
                print(f"    Download link: {file.download_link[:100]}...")
                print(f"    Crawl time: {file.crawl_time}")
        
        total_files = db.query(ExamFile).count()
        print(f"\nTotal files in database after crawl_latest_only: {total_files}")
        
        print("\n✅ Crawler test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during crawler test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_crawler()