import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from app.services.excel_service import ExcelService
from app.core.database import SessionLocal

# Test reading the Excel file
file_path = "d:/Excel/DS Tổng quan Hành vi Tổ chức trong Du lịch OB 253 B-D-F_2.xlsx"

print(f"Reading file: {file_path}")
df = pd.read_excel(file_path, sheet_name='DS_THI', header=None)
print(f"Shape: {df.shape}")

# Test the parsing function
db = SessionLocal()
try:
    service = ExcelService(db)
    schedules = service._parse_excel_custom(df, 1)
    
    print(f"\n\nFound {len(schedules)} schedules:")
    for s in schedules[:5]:  # Show first 5
        print(f"  - {s.student_name} ({s.student_id}) - Room: {s.exam_room}")
    if len(schedules) > 5:
        print(f"  ... and {len(schedules) - 5} more")
    
    # Check for specific student
    phan_van_an = [s for s in schedules if "Phan Văn An" in s.student_name]
    print(f"\n\nPhan Văn An found: {len(phan_van_an)}")
    for s in phan_van_an:
        print(f"  - {s.student_name} ({s.student_id}) - Room: {s.exam_room}")
        
    # Check a few more names
    print("\n\nSample of names found:")
    for s in schedules[10:15]:
        print(f"  - {s.student_name} ({s.student_id})")
        
finally:
    db.close()