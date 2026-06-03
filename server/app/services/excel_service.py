import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.utils.logger import log

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
        """
        file_path = self.storage_path / exam_file.file_name
        log.info(f"Processing Excel file: {file_path}")

        try:
            df = pd.read_excel(file_path)
            
            # Normalize column names
            df.columns = df.columns.str.lower().str.strip()
            df = df.rename(columns=self.column_mapping)
            
            # Filter for required columns
            required_cols = list(self.column_mapping.values())
            df = df[[col for col in required_cols if col in df.columns]]

            # Data cleaning
            df.dropna(how="all", inplace=True)
            df = df.astype(str)

            schedules_to_add = []
            for _, row in df.iterrows():
                schedule_data = row.to_dict()
                schedule_data["exam_file_id"] = exam_file.id
                
                # Create schedule object without adding to session yet
                schedules_to_add.append(ExamSchedule(**schedule_data))

            # Bulk insert and handle duplicates
            try:
                self.db.bulk_save_objects(schedules_to_add, return_defaults=True)
                self.db.commit()
                log.info(f"Successfully processed and saved {len(schedules_to_add)} records from {exam_file.file_name}")
            except IntegrityError:
                self.db.rollback()
                log.warning(f"Duplicates found in {exam_file.file_name}. Inserting one by one.")
                self._insert_schedules_individually(schedules_to_add)

        except FileNotFoundError:
            log.error(f"File not found: {file_path}")
        except Exception as e:
            log.error(f"Error processing file {file_path}: {e}")

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
                self.db.rollback()  # Rollback the single failed transaction
                log.debug(f"Skipping duplicate schedule: {schedule.student_id} - {schedule.subject_code}")
            except Exception as e:
                self.db.rollback()
                log.error(f"Error saving individual schedule: {e}")
        log.info(f"Saved {saved_count} new records individually.")