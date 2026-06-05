import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "server")))

from app.core.database import SessionLocal
from app.services.subscription_service import SubscriptionService

file_path = "d:/Excel/DS Tổng quan Hành vi Tổ chức trong Du lịch OB 253 B-D-F_2.xlsx"

db = SessionLocal()
try:
    service = SubscriptionService(db)
    
    # Test with full name
    print("Testing with 'Phan Văn An':")
    result = service._extract_user_exam_info(file_path, "Phan Văn An")
    print(f"Found {len(result)} matches:")
    for r in result:
        print(f"  - Student: {r['student_name']} (ID: {r['student_id']})")
        print(f"    Time: {r['exam_date_time']}")
        print(f"    Room: {r.get('exam_room', '')}")
        print(f"    Location: {r.get('exam_location', '')}")
    
    print("\n" + "=" * 60)
    print("Testing with 'Mai Hoài An':")
    result = service._extract_user_exam_info(file_path, "Mai Hoài An")
    print(f"Found {len(result)} matches:")
    for r in result:
        print(f"  - Student: {r['student_name']} (ID: {r['student_id']})")
        print(f"    Time: {r['exam_date_time']}")
        print(f"    Room: {r.get('exam_room', '')}")
        print(f"    Location: {r.get('exam_location', '')}")
        
finally:
    db.close()