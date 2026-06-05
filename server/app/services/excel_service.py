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
            # Try reading with openpyxl engine for better handling of complex Excel files
            df = pd.read_excel(file_path, engine='openpyxl', header=None)
            
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
        Scans row by row to find time/room info and student information.
        """
        schedules = []
        
        # Pattern to match "Thời gian: ... Phòng: ..."
        # Handle variations like "Thời gian:  15h30 - 31/05/2026                Phòng:           NaN"
        time_room_pattern = re.compile(r'Thời\s+gian:\s*(.+?)\s*Phòng:\s*(.+)', re.IGNORECASE)
        
        # Track current time and room info
        current_time_info = ""
        current_room_info = ""
        blank_line_count = 0
        
        for idx, row in df.iterrows():
            # Convert row to list of strings
            row_values = row.tolist()
            
            # Join all values to check for blank line (excluding NaN)
            row_str = ' '.join(str(val) for val in row_values if str(val).lower() != 'nan' and str(val).strip() != '')
            
            # Check if this is a blank line
            is_blank = len(row_str.strip()) == 0
            
            if is_blank:
                blank_line_count += 1
                # If we have 10 consecutive blank lines, we've reached the end
                if blank_line_count >= 10:
                    log.info(f"Found end of data after {blank_line_count} blank lines")
                    break
                continue
            
            # Reset blank line counter when we find non-blank data
            blank_line_count = 0
            
            # Check for time and room info (like "Thời gian: 15h30 - 31/05/2026 Phòng: 304/1 - K7/25 Quang Trung")
            row_full_str = ' '.join(str(val).strip() for val in row_values)
            time_room_match = time_room_pattern.search(row_full_str)
            
            if time_room_match:
                current_time_info = time_room_match.group(1).strip()
                # Clean up room info - remove NaN values and extra spaces
                room_part = time_room_match.group(2).strip()
                # Remove "nan" strings (case insensitive) - match whole word "nan"
                current_room_info = re.sub(r'\bnan\b', '', room_part, flags=re.IGNORECASE).strip()
                # Clean up multiple spaces
                current_room_info = re.sub(r'\s+', ' ', current_room_info).strip()
                log.debug(f"Found time/room: {current_time_info} - {current_room_info}")
                continue
            
            # Look for student data rows
            # Student ID is usually numeric (10-12 digits), name is in columns 3 and 4
            # Use simple check: if column 2 (index 2) looks like an integer, it's probably STT
            # And column 3 (index 3) has 10-12 digits, it's probably student ID
            
            # Try to find student ID in columns
            student_id = None
            for col_idx, val in enumerate(row_values):
                val_str = str(val).strip()
                if re.match(r'^\d{10,12}$', val_str):
                    # Found a student ID
                    student_id = val_str
                    
                    # Try to build the student name from columns
                    student_name = ""
                    
                    # Look for name parts in nearby columns
                    name_parts = []
                    # Check column 3 (index 3) for first name part
                    if 3 < len(row_values):
                        part1 = str(row_values[3]).strip()
                        if part1 and part1 != 'nan':
                            name_parts.append(part1)
                    
                    # Check column 4 (index 4) for second name part  
                    if 4 < len(row_values):
                        part2 = str(row_values[4]).strip()
                        if part2 and part2 != 'nan':
                            name_parts.append(part2)
                    
                    if name_parts:
                        student_name = ' '.join(name_parts)
                        # Only accept if name has at least 2 characters
                        if len(student_name.strip()) >= 2:
                            # Extract subject code
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
                            log.debug(f"Found student: {student_name} ({student_id}) - Room: {current_room_info}")
                    break  # Found student ID, move to next row
        
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