import os
import re
import requests
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session

from pypdf import PdfReader
import pandas as pd

from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.utils.logger import log
from app.core.config import settings


class FileService:
    """
    Service to handle both Excel and PDF exam files.
    Downloads files from URLs and processes them to extract exam schedules.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.storage_path = Path("storage/excel")
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def download_file(self, exam_file: ExamFile) -> Optional[Path]:
        """
        Download an exam file (Excel or PDF) from the download link.
        Returns the path to the downloaded file or None if download fails.
        """
        try:
            log.info(f"Downloading file: {exam_file.file_name}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(exam_file.download_link, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Use sanitized filename for storage
            sanitized_name = self._sanitize_filename(exam_file.file_name)
            file_path = self.storage_path / sanitized_name
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            log.info(f"Downloaded file: {exam_file.file_name} as {sanitized_name}")
            return file_path
            
        except Exception as e:
            log.error(f"Failed to download file {exam_file.download_link}: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to be valid for Windows file system.
        Replaces invalid characters with underscores.
        Preserves the file extension.
        """
        invalid_chars = r'[<>:"|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        # Remove backslashes (not for path separators, just remove them)
        sanitized = sanitized.replace('\\', '')
        # Replace date format slashes (e.g., 31/05/2026 -> 31-05-2026)
        sanitized = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1-\2-\3', sanitized)
        return sanitized
    
    def get_file_type(self, file_path: Path, download_url: Optional[str] = None) -> str:
        """
        Determine if the file is Excel or PDF based on extension.
        Returns 'excel' or 'pdf'.
        """
        extension = file_path.suffix.lower()
        if extension in ['.xlsx', '.xls', '.xlsm']:
            return 'excel'
        elif extension == '.pdf':
            return 'pdf'
        
        # If extension is empty, try to get it from the download URL
        if download_url:
            url_extension = Path(download_url).suffix.lower()
            if url_extension == '.pdf':
                return 'pdf'
        
        return 'unknown'
    
    def process_file(self, exam_file: ExamFile) -> list[ExamSchedule]:
        """
        Process an exam file (Excel or PDF) and extract exam schedules.
        Returns a list of ExamSchedule objects.
        """
        file_path = self.storage_path / self._sanitize_filename(exam_file.file_name)
        
        if not file_path.exists():
            log.warning(f"File not found: {file_path}")
            return []
        
        file_type = self.get_file_type(file_path, exam_file.download_link)
        log.info(f"Processing {file_type} file: {file_path}")
        
        try:
            if file_type == 'excel':
                return self._process_excel(file_path, exam_file.id)
            elif file_type == 'pdf':
                return self._process_pdf(file_path, exam_file.id)
            else:
                log.error(f"Unsupported file type: {file_path}")
                return []
                
        except Exception as e:
            log.error(f"Error processing file {file_path}: {e}")
            return []
    
    def _process_excel(self, file_path: Path, exam_file_id: int) -> list[ExamSchedule]:
        """
        Process an Excel file and extract exam schedules.
        Uses the existing Excel parsing logic from excel_service.py
        """
        from app.services.excel_service import ExcelService
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl', header=None)
            df = df.astype(str)
            
            # Use a temporary ExcelService instance to parse
            excel_service = ExcelService(self.db)
            schedules = excel_service._parse_excel_custom(df, exam_file_id)
            
            log.info(f"Processed {len(schedules)} schedules from Excel file: {file_path}")
            return schedules
            
        except Exception as e:
            log.error(f"Error processing Excel file {file_path}: {e}")
            return []
    
    def _process_pdf(self, file_path: Path, exam_file_id: int) -> list[ExamSchedule]:
        """
        Process a PDF file and extract exam schedules.
        Similar logic to Excel processing but adapted for PDF text extraction.
        """
        schedules = []
        
        try:
            # Read PDF text
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Parse PDF content similar to Excel
            schedules = self._parse_pdf_content(text, file_path, exam_file_id)
            
            log.info(f"Processed {len(schedules)} schedules from PDF file: {file_path}")
            return schedules
            
        except Exception as e:
            log.error(f"Error processing PDF file {file_path}: {e}")
            return []
    
    def _parse_pdf_content(self, text: str, file_path: Path, exam_file_id: int) -> list[ExamSchedule]:
        """
        Parse PDF text content to extract exam schedules.
        Similar logic to _parse_excel_custom but for text-based parsing.
        """
        schedules = []
        
        # Pattern to match "Thời gian: ... Phòng: ..."
        time_room_pattern = re.compile(r'Thời\s+gian:\s*(.+?)\s*Phòng:\s*(.+)', re.IGNORECASE)
        
        # Track current time and room info
        current_time_info = ""
        current_room_info = ""
        blank_line_count = 0
        
        # Split text into lines
        lines = text.split('\n')
        
        for idx, line in enumerate(lines):
            # Clean up the line
            line_stripped = line.strip()
            
            # Check if this is a blank line
            is_blank = len(line_stripped) == 0
            
            if is_blank:
                blank_line_count += 1
                # If we have 10 consecutive blank lines, we've reached the end
                if blank_line_count >= 10:
                    log.info(f"Found end of data after {blank_line_count} blank lines")
                    break
                continue
            
            # Reset blank line counter when we find non-blank data
            blank_line_count = 0
            
            # Check for time and room info
            time_room_match = time_room_pattern.search(line_stripped)
            
            if time_room_match:
                current_time_info = time_room_match.group(1).strip()
                # Clean up room info
                room_part = time_room_match.group(2).strip()
                current_room_info = re.sub(r'\bnan\b', '', room_part, flags=re.IGNORECASE).strip()
                current_room_info = re.sub(r'\s+', ' ', current_room_info).strip()
                log.debug(f"Found time/room: {current_time_info} - {current_room_info}")
                continue
            
            # Look for student data in PDF
            # PDF format: "STT MÃ SINH VIÊN HỌ VÀ TÊN LỚP MÔN..."
            # We need to extract student info from the text
            
            # Split line into parts (by multiple spaces or tabs)
            parts = re.split(r'\s{2,}', line_stripped)
            
            # Try to find student ID (10-12 digits)
            student_id = None
            student_col_idx = -1
            for i, part in enumerate(parts):
                part_stripped = part.strip()
                if re.match(r'^\d{10,12}$', part_stripped):
                    student_id = part_stripped
                    student_col_idx = i
                    break
            
            if student_id:
                # Extract student name (usually in parts around student_id)
                name_parts = []
                for i in [student_col_idx + 1, student_col_idx + 2, student_col_idx - 1]:
                    if 0 <= i < len(parts):
                        val = parts[i].strip()
                        if val and val.lower() != 'nan' and not re.match(r'^\d{10,12}$', val) and not re.match(r'^[A-Z]{2,4}\s+\d{3}$', val):
                            name_parts.append(val)
                
                student_name = ' '.join(name_parts)
                
                if student_name and len(student_name.strip()) >= 2:
                    # Extract subject code
                    subject_code = self._extract_subject_code_from_parts(parts)
                    
                    schedule = ExamSchedule(
                        exam_file_id=exam_file_id,
                        student_id=student_id,
                        student_name=student_name.strip(),
                        subject_code=subject_code,
                        subject_name="",
                        exam_date=None,
                        exam_time=current_time_info,
                        exam_room=current_room_info,
                    )
                    schedules.append(schedule)
                    log.debug(f"Found student in PDF: {student_name} ({student_id}) - Room: {current_room_info}")
        
        return schedules
    
    def _extract_subject_code_from_parts(self, parts: list[str]) -> str:
        """
        Extract subject code from PDF parts.
        Subject code pattern: letters followed by space and numbers (e.g., "OB 253")
        """
        for part in parts:
            part_stripped = part.strip()
            # Subject code pattern: 2-4 uppercase letters followed by space and 3 digits
            if re.match(r'^[A-Z]{2,4}\s+\d{3}$', part_stripped):
                return part_stripped
        
        return ""
    
    def process_all_pending_files(self, crawl_latest_only: bool = False) -> int:
        """
        Process all pending exam files that haven't been processed yet.
        Downloads files and extracts schedules.
        Returns the number of files processed.
        """
        from sqlalchemy.exc import IntegrityError
        
        # Query for files that need processing
        query = self.db.query(ExamFile)
        
        if crawl_latest_only:
            # Only process the most recent 100 files
            files = query.order_by(ExamFile.crawl_time.desc()).limit(100).all()
        else:
            files = query.all()
        
        processed_count = 0
        total_schedules = 0
        
        for exam_file in files:
            try:
                # Download the file
                file_path = self.download_file(exam_file)
                if not file_path:
                    log.warning(f"Could not download file: {exam_file.file_name}")
                    continue
                
                # Process the file
                schedules = self.process_file(exam_file)
                
                if schedules:
                    # Bulk insert schedules
                    try:
                        self.db.bulk_save_objects(schedules, return_defaults=True)
                        self.db.commit()
                        total_schedules += len(schedules)
                        log.info(f"Saved {len(schedules)} schedules from {exam_file.file_name}")
                    except IntegrityError:
                        self.db.rollback()
                        log.warning(f"Duplicates found in {exam_file.file_name}. Inserting one by one.")
                        self._insert_schedules_individually(schedules)
                        total_schedules += len(schedules)
                
                processed_count += 1
                
            except Exception as e:
                log.error(f"Error processing file {exam_file.file_name}: {e}")
                self.db.rollback()
        
        log.info(f"Processed {processed_count} files with {total_schedules} total schedules")
        return processed_count
    
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