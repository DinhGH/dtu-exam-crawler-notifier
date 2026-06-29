import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.utils.logger import log
import re


class ExcelService:
    def __init__(self, db: Session):
        self.db = db
        self.storage_path = Path("storage/excel")
        self.column_mapping = {
            "mã sv": "student_id",
            "họ và tên": "student_name",
            "mã học phần": "subject_code",
            "tên học phần": "subject_name",
            "ngày thi": "exam_date",
            "giờ thi": "exam_time",
            "phòng thi": "exam_room",
        }

    def process_exam_file(self, exam_file: ExamFile):
        """
        Processes a downloaded Excel file to extract and save exam schedules.
        Uses custom parsing logic to handle the complex Excel layout.
        """
        file_path = self.storage_path / exam_file.file_name
        log.info(f"Processing Excel file: {file_path}")

        try:
            # Detect engine based on file extension
            engine = 'xlrd' if file_path.suffix.lower() == '.xls' else 'openpyxl'
            df = pd.read_excel(file_path, engine=engine, header=None)
            
            # Forward fill to handle merged cells
            df = df.ffill().fillna('')
            
            # Convert all cells to string for easier parsing
            df = df.astype(str)
            
            # Parse the file using custom logic
            schedules = self._parse_excel_custom(df, exam_file.id)
            
            if not schedules:
                log.warning(f"No schedules found in {exam_file.file_name}")
                return

            # Bulk insert and handle duplicates
            try:
                self.db.bulk_save_objects(schedules, return_defaults=True)
                self.db.commit()
                log.info(f"Successfully processed and saved {len(schedules)} records from {exam_file.file_name}")
            except IntegrityError:
                self.db.rollback()
                log.warning(f"Duplicates found in {exam_file.file_name}. Inserting one by one.")
                self._insert_schedules_individually(schedules)

        except FileNotFoundError:
            log.error(f"File not found: {file_path}")
        except Exception as e:
            log.error(f"Error processing file {file_path}: {e}")

    def _parse_excel_custom(self, df: pd.DataFrame, exam_file_id: int) -> list[ExamSchedule]:
        """
        Custom parsing logic to extract exam schedules from Excel file.
        Scans block of rows/columns to find time/room info and student information.
        """
        schedules = []
        
        # Enhanced patterns for flexible extraction
        # Matches: "Thời gian: 9h30 - Ngày 30/05/2026 - Phòng: 408 - cơ sở: ..."
        # Searches across merged text block
        full_text_pattern = re.compile(
            r'Thời\s*gian:\s*(?P<time>.+?)\s*-?\s*Phòng:\s*(?P<room>.+?)(?:\s*-?\s*cơ\s*sở:\s*(?P<location>.+?))?$', 
            re.IGNORECASE
        )
        
        # Track current time and room info
        current_time_info = ""
        current_room_info = ""
        
        # 1. First pass: Try to find schedule info in the first 15 rows (scan A-E)
        search_df = df.iloc[:15, :5]
        for _, row in search_df.iterrows():
            row_str = ' '.join([str(v) for v in row if str(v).lower() != 'nan'])
            match = full_text_pattern.search(row_str)
            if match:
                current_time_info = match.group('time').strip()
                full_room = match.group('room').strip()
                location = match.group('location') or ""
                current_room_info = f"{full_room} - {location}".strip(" -")
                break
        
        # 2. Second pass: Parse student rows
        for idx, row in df.iterrows():
            row_values = [str(val).strip() for val in row.tolist()]
            
            # Try to find student ID (10-12 digits) anywhere in the row
            student_id = None
            student_col_idx = -1
            for i, val in enumerate(row_values):
                if re.match(r'^\d{10,12}$', val):
                    student_id = val
                    student_col_idx = i
                    break
            
            if student_id:
                # Attempt to find name in adjacent columns
                name_parts = []
                for i in [student_col_idx + 1, student_col_idx + 2, student_col_idx - 1]:
                    if 0 <= i < len(row_values) and row_values[i] and row_values[i].lower() != 'nan':
                        if not re.match(r'^\d{10,12}$', row_values[i]) and not re.match(r'^[A-Z]{2,4}\s+\d{3}$', row_values[i]):
                            name_parts.append(row_values[i])
                
                student_name = ' '.join(name_parts)
                if len(student_name.strip()) >= 2:
                    subject_code = self._extract_subject_code(row_values)
                    schedule = ExamSchedule(
                        exam_file_id=exam_file_id,
                        student_id=student_id,
                        student_name=student_name,
                        subject_code=subject_code,
                        subject_name="",
                        exam_date=None,
                        exam_time=current_time_info,
                        exam_room=current_room_info,
                    )
                    schedules.append(schedule)
        
        return schedules

    def _extract_subject_code(self, row_values: list) -> str:
        """
        Extract subject code from row values.
        Subject code pattern: letters followed by space and numbers (e.g., "OB 253")
        """
        # Try to find subject code in row values
        for val in row_values:
            val_str = str(val).strip()
            # Subject code pattern: 2-4 uppercase letters followed by space and 3 digits
            if re.match(r'^[A-Z]{2,4}\s+\d{3}$', val_str):
                return val_str
        
        return ""

    def _insert_schedules_individually(self, schedules: list[ExamSchedule]):
        """
        Inserts schedules one by one, skipping duplicates.
        """
        saved_count = 0
        for schedule in schedules:
            try:
                self.db.add(schedule)
                self.db.commit()
                saved_count += 1
            except IntegrityError:
                self.db.rollback()
                log.debug(f"Skipping duplicate schedule: {schedule.student_id} - {schedule.subject_code}")
            except Exception as e:
                self.db.rollback()
                log.error(f"Error saving individual schedule: {e}")
        log.info(f"Saved {saved_count} new records individually.")