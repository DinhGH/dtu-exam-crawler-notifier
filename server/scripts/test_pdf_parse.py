#!/usr/bin/env python3
"""
Test script for PDF parsing.
This script tests the PDF parsing functionality with a sample PDF file.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.file_service import FileService
from app.models.exam_file import ExamFile
from datetime import datetime

def test_pdf_parse():
    """Test PDF parsing functionality."""
    print("Testing PDF parsing...")
    
    # Test with the sample PDF from the website
    sample_pdf_url = "https://pdaotao.duytan.edu.vn/uploads/Exam/31052026-9h30-KOR%20206%20(B-D-F-H-J-L).pdf"
    
    db: Session = SessionLocal()
    try:
        # Create a test exam file record
        exam_file = ExamFile(
            file_name="Đọc 2 - KOR 206 (B-D-F-H-J-L)",
            download_link=sample_pdf_url,
            crawl_time=datetime.now(),
        )
        db.add(exam_file)
        db.commit()
        db.refresh(exam_file)
        print(f"Created test exam file with ID: {exam_file.id}")
        
        # Test the file service
        file_service = FileService(db)
        
        # Download the file
        print(f"\nDownloading PDF from: {sample_pdf_url}")
        file_path = file_service.download_file(exam_file)
        if not file_path:
            print("Failed to download PDF file")
            return
        
        print(f"Downloaded to: {file_path}")
        
        # Process the file
        print(f"\nProcessing PDF file...")
        schedules = file_service.process_file(exam_file)
        print(f"Found {len(schedules)} schedules")
        
        # Show first 5 schedules
        if schedules:
            print("\nFirst 5 schedules:")
            for s in schedules[:5]:
                print(f"  - {s.student_name} ({s.student_id}) - Room: {s.exam_room} - Time: {s.exam_time}")
        
        # Test extracting specific student
        print("\nSearching for student: 'Đỗ Phương Anh'")
        for schedule in schedules:
            if "Đỗ Phương Anh" in schedule.student_name or "Do Phuong Anh" in schedule.student_name.lower():
                print(f"  Found: {schedule.student_name} ({schedule.student_id}) - Room: {schedule.exam_room}")
        
        print("\n✅ PDF parsing test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during PDF parsing test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_pdf_parse()