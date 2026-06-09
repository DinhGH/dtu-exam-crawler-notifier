import os
import smtplib
import base64
import re
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.models.subscription import Subscription
from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.models.email_log import EmailLog
from app.utils.logger import log
from email.header import Header
import logging

# Import pypdf for PDF processing
try:
    from pypdf import PdfReader
    PDF_SUPPORTED = True
except ImportError:
    PDF_SUPPORTED = False




class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        self.storage_path = Path("storage/excel")
        self.email_config = {
            "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "smtp_user": os.getenv("SMTP_EMAIL"),
            "smtp_password": os.getenv("SMTP_PASSWORD"),
            "from_email": os.getenv("FROM_EMAIL", os.getenv("SMTP_EMAIL")),
            "from_name": os.getenv("FROM_NAME", "Hệ thống Thông báo Danh Sách Thi"),
        }

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to be valid for Windows file system.
        Replaces invalid characters with underscores.
        Preserves the file extension.
        """
        # Invalid characters for Windows filenames: < > : " / \ | ? *
        invalid_chars = r'[<>:"|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        # Remove backslashes (not for path separators, just remove them)
        sanitized = sanitized.replace('\\', '')
        # Replace date format slashes (e.g., 31/05/2026 -> 31-05-2026)
        sanitized = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\1-\2-\3', sanitized)
        return sanitized

    def _get_excel_file_path(self, file_name: str) -> Path:
        """Get the full path to an Excel file in storage."""
        sanitized_name = self._sanitize_filename(file_name)
        return self.storage_path / sanitized_name

    def _download_excel_file(self, exam_file: ExamFile) -> Path | None:
        """
        Download an Excel file from the download link and save it to storage.
        Returns the path to the downloaded file or None if download fails.
        """
        import requests

        try:
            response = requests.get(exam_file.download_link, timeout=30)
            response.raise_for_status()

            # Use sanitized filename for storage
            sanitized_name = self._sanitize_filename(exam_file.file_name)
            file_path = self.storage_path / sanitized_name
            self.storage_path.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'wb') as f:
                f.write(response.content)

            log.info(f"Downloaded Excel file: {exam_file.file_name} as {sanitized_name}")
            return file_path

        except Exception as e:
            log.error(f"Failed to download Excel file {exam_file.download_link}: {e}")
            return None

    def _find_matching_exam_files(self, subject_code: Optional[str], subject_name: Optional[str]) -> List[ExamFile]:
        """
        Find exam files that match the given subject code and/or subject name.
        Searches in the file_name field which contains subject information.
        """
        query = self.db.query(ExamFile)

        if subject_code:
            query = query.filter(ExamFile.file_name.ilike(f"%{subject_code}%"))

        if subject_name:
            query = query.filter(ExamFile.file_name.ilike(f"%{subject_name}%"))

        # If no filters provided, return all files
        if not subject_code and not subject_name:
            return query.order_by(ExamFile.crawl_time.desc()).limit(10).all()

        return query.order_by(ExamFile.crawl_time.desc()).all()

    log = logging.getLogger(__name__)

    def _extract_user_exam_info(self, excel_file_path: str, user_full_name: str) -> list:
        """
        Quét file Excel từ trên xuống theo logic cuốn chiếu (Scanner):
        - Tự động nhận diện và cập nhật thông tin Phòng/Thời gian thi khi bắt gặp.
        - Khắc phục triệt để lỗi ghi đè ô thông tin giữa phòng và thời gian.
        - Tìm kiếm sinh viên chính xác từ đầu, giữa đến cuối danh sách.
        - Tự động dừng khi gặp 15 dòng trống liên tiếp để tối ưu hiệu năng.
        """
        # Determine file type based on extension
        file_path = Path(excel_file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return self._extract_user_exam_info_from_pdf(excel_file_path, user_full_name)
        
        try:
            # 1. Đọc toàn bộ file Excel dưới dạng bảng thô (Matrix) để tránh cơ chế ngầm của Pandas
            df_raw = pd.read_excel(excel_file_path, header=None)
            raw_matrix = df_raw.values.tolist()
            
            # Khởi tạo các biến trạng thái lưu tạm dữ liệu phòng và thời gian
            current_room_number = ""
            current_location = ""
            current_time = ""
            
            # Đọc thông tin môn học cố định (thường ở dòng 2 hoặc 3 đầu file)
            subject_info = str(df_raw.iloc[1, 2]) if df_raw.shape[0] > 2 else ""

            # Chuẩn hóa tên tìm kiếm: viết thường, xóa khoảng trắng thừa
            search_name = " ".join(user_full_name.lower().split())
            result = []
            
            # Biến đếm dòng trống liên tiếp để ngắt vòng lặp thông minh
            empty_row_counter = 0

            # 2. Duyệt từng dòng một từ trên xuống dưới
            for row_list in raw_matrix:
                # Chuyển đổi toàn bộ ô trong dòng về chuỗi sạch (Xử lý an toàn cho cả float/nan)
                clean_cells = []
                for cell in row_list:
                    if pd.isna(cell) or cell is None:
                        clean_cells.append("")
                    else:
                        clean_cells.append(str(cell).strip())
                
                # Gộp dòng thành một chuỗi duy nhất để nhận diện khối thông tin mục lớn
                row_combined = " ".join([c.lower() for c in clean_cells if c])
                
                # KIỂM TRA DÒNG TRỐNG: Nếu dòng không có ký tự nào
                if not row_combined:
                    empty_row_counter += 1
                    if empty_row_counter >= 15:  # Gặp 15 dòng trống liên tiếp thì dừng quét file
                        break
                    continue
                else:
                    empty_row_counter = 0  # Reset bộ đếm nếu dòng có dữ liệu

                # CHUYỂN ĐỔI NGỮ CẢNH: Tìm thấy dòng chứa cấu trúc Phòng thi / Thời gian
                if 'thời gian:' in row_combined or 'thoi gian:' in row_combined:
                    # Process time info first
                    for cell_val in clean_cells:
                        val_lower = cell_val.lower()
                        if not val_lower:
                            continue
                        
                        # Ô chứa thời gian thi chuẩn (Có định dạng giờ 'h' và ngày thi '/')
                        # Time format: "Thời gian:  15h30 - 31/05/2026                Phòng:"
                        # We need to extract just the time portion
                        if 'h' in val_lower and '/' in val_lower:
                            # Extract time portion from the string
                            # Example: "Thời gian:  15h30 - 31/05/2026                Phòng:"
                            # We want to get "15h30 - 31/05/2026"
                            if 'thời gian:' in val_lower:
                                # Split by "Thời gian:" and take the second part
                                parts = cell_val.split('Thời gian:', 1)
                                if len(parts) > 1:
                                    time_part = parts[1].strip()
                                    # Now remove the "Phòng:" part if it exists
                                    if 'Phòng:' in time_part:
                                        time_part = time_part.split('Phòng:', 1)[0].strip()
                                    elif 'phòng:' in time_part:
                                        time_part = time_part.split('phòng:', 1)[0].strip()
                                    current_time = time_part
                                else:
                                    current_time = cell_val
                            else:
                                current_time = cell_val
                    
                    # Process room/location info - Column G (index 6) = Room, Column H (index 7) = Location
                    if len(clean_cells) > 7:
                        room_val = clean_cells[6].strip()
                        location_val = clean_cells[7].strip()
                        
                        log.debug(f"DEBUG: Room val='{room_val}', Location val='{location_val}'")
                        
                        # Room number is from column G (e.g., "304/1", "403")
                        if room_val and '/' in room_val:
                            current_room_number = room_val
                        
                        # Location is from column H - always extract it (remove leading dash if present)
                        # Examples: "- K7/25 Quang Trung", "-K7/25 Quang Trung", "K7/25 Quang Trung"
                        if location_val:
                            if location_val.startswith('- '):
                                location_val = location_val[2:].strip()
                            elif location_val.startswith('-'):
                                location_val = location_val[1:].strip()
                            current_location = location_val
                    
                    continue  # Trích xuất xong dòng cấu trúc ngữ cảnh thì chuyển ngay sang dòng tiếp theo

                # SO KHỚP TÊN SINH VIÊN: Sử dụng index cột cố định theo form danh sách thi Duy Tân
                # Định vị: Cột 0 (STT), Cột 1 (STT duplicates), Cột 2 (Mã SV), Cột 3 (Họ và), Cột 4 (Tên)
                if len(clean_cells) >= 5:
                    ho_val = clean_cells[3]
                    ten_val = clean_cells[4]
                    stt_val = clean_cells[0]     # Số thứ tự thí sinh trong phòng đó
                    student_id = clean_cells[2]  # Mã sinh viên (cột 2)

                    # Loại bỏ các dòng tiêu đề lặp lại (STT, HỌ VÀ, TÊN) hoặc dòng rác cuối bảng
                    if not ho_val or not ten_val or 'họ' in ho_val.lower() or 'tên' in ten_val.lower():
                        continue
                    
                    # Ghép Họ và Tên đầy đủ từ hai cột riêng biệt
                    full_name_in_file = f"{ho_val} {ten_val}"
                    full_name_clean = " ".join(full_name_in_file.lower().split())
                    
                    # Tiến hành so khớp chuỗi tên tìm kiếm
                    if search_name in full_name_clean:
                        # Lấy thông tin lớp sinh hoạt nằm ở các cột kế tiếp (thường từ index 4 đến 6)
                        class_name = ""
                        for c in clean_cells[4:7]:
                            if c and ('k2' in c.lower() or 'k3' in c.lower()):
                                class_name = c
                                break

                        # Điền thông tin tìm thấy vào mảng kết quả
                        result.append({
                            'student_no': stt_val,
                            'student_name': full_name_in_file,
                            'student_id': student_id,
                            'exam_date_time': current_time if current_time else "Xem trong file",
                            'exam_room': current_room_number if current_room_number else "Xem trong file",
                            'exam_location': current_location if current_location else "Xem trong file",
                            'subject_meta': subject_info
                        })
                        
                        # GỢI Ý TỐI ƯU: Nếu một sinh viên chắc chắn chỉ xuất hiện 1 lần duy nhất trong cả file, 
                        # bạn có thể mở comment lệnh dưới đây để hàm trả về kết quả luôn mà không cần quét tiếp:
                        # return result

            return result

        except Exception as e:
            log.error(f"Lỗi khi xử lý trích xuất file Excel {excel_file_path}: {e}")
            return []

        except Exception as e:
            log.error(f"Lỗi khi xử lý file Excel {excel_file_path}: {e}")
            return []

    def _extract_user_exam_info_from_pdf(self, pdf_file_path: str, user_full_name: str) -> list:
        """
        Extract user's exam information from a PDF file.
        Similar logic to Excel extraction but adapted for PDF text extraction.
        """
        if not PDF_SUPPORTED:
            log.error("PDF support not available. Please install pypdf.")
            return []
        
        try:
            # Read PDF text
            reader = PdfReader(pdf_file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Normalize name for searching
            search_name = " ".join(user_full_name.lower().split())
            result = []
            
            # Track current time and room info
            current_room_number = ""
            current_location = ""
            current_time = ""
            blank_line_count = 0
            
            # Split text into lines
            lines = text.split('\n')
            
            for line in lines:
                # Clean up the line
                line_stripped = line.strip()
                
                # Check if this is a blank line
                is_blank = len(line_stripped) == 0
                
                if is_blank:
                    blank_line_count += 1
                    if blank_line_count >= 10:
                        break
                    continue
                
                # Reset blank line counter
                blank_line_count = 0
                
                # Check for time and room info
                time_room_match = re.search(r'Thời\s+gian:\s*(.+?)\s*Phòng:\s*(.+)', line_stripped, re.IGNORECASE)
                
                if time_room_match:
                    current_time = time_room_match.group(1).strip()
                    room_part = time_room_match.group(2).strip()
                    current_room_number = re.sub(r'\bnan\b', '', room_part, flags=re.IGNORECASE).strip()
                    current_room_number = re.sub(r'\s+', ' ', current_room_number).strip()
                    log.debug(f"Found time/room: {current_time} - {current_room_number}")
                    continue
                
                # Split line into parts (by multiple spaces)
                parts = re.split(r'\s{2,}', line_stripped)
                
                if len(parts) >= 5:
                    # Try to find student ID (10-12 digits)
                    student_id = None
                    for part in parts:
                        part_stripped = part.strip()
                        if re.match(r'^\d{10,12}$', part_stripped):
                            student_id = part_stripped
                            break
                    
                    if student_id:
                        # Extract student name
                        student_name = ""
                        if len(parts) > 3:
                            part3 = parts[3].strip() if parts[3] else ""
                            part4 = parts[4].strip() if len(parts) > 4 and parts[4] else ""
                            
                            if part3 and part3.lower() != 'nan':
                                student_name = part3
                            if part4 and part4.lower() != 'nan':
                                student_name = f"{student_name} {part4}" if student_name else part4
                        
                        if student_name and len(student_name.strip()) >= 2:
                            # Check if this is the user
                            full_name_clean = " ".join(student_name.lower().split())
                            
                            if search_name in full_name_clean:
                                result.append({
                                    'student_no': parts[0].strip() if parts else "",
                                    'student_name': student_name.strip(),
                                    'student_id': student_id,
                                    'exam_date_time': current_time if current_time else "Xem trong file",
                                    'exam_room': current_room_number if current_room_number else "Xem trong file",
                                    'exam_location': current_location if current_location else "Xem trong file",
                                    'subject_meta': ""
                                })
            
            log.info(f"Found {len(result)} exam entries for {user_full_name} in PDF")
            return result
            
        except Exception as e:
            log.error(f"Lỗi khi xử lý trích xuất file PDF {pdf_file_path}: {e}")
            return []
    
    def _create_email_message(
        self,
        to_email: str,
        user_full_name: str,
        exam_files_data: List[Dict[str, Any]]
    ) -> MIMEMultipart:
        """
        Create the email message with Excel file attachment and user's exam information.
        """
        from email.header import Header

        msg = MIMEMultipart()
        msg['From'] = f"{self.email_config['from_name']} <{self.email_config['from_email']}>"
        msg['To'] = to_email
        msg['Subject'] = f"[Thông báo] Danh sách thi của {user_full_name}"

        # Email body HTML
        html_content = self._generate_email_html(user_full_name, exam_files_data)
        msg.attach(MIMEText(html_content, 'html'))

        # Attach Excel files
        for file_data in exam_files_data:
            if 'file_path' in file_data and Path(file_data['file_path']).exists():
                try:
                    file_path_obj = Path(file_data['file_path'])
                    with open(file_path_obj, 'rb') as f:
                        # SỬA TẠI ĐÂY: Thay 'application/octet-stream' thành định dạng chuẩn của Excel (.xlsx)
                        part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        
                        filename_raw = file_path_obj.name
                        # Đảm bảo tên file đính kèm gửi đi bắt buộc phải kết thúc bằng đuôi .xlsx
                        if not filename_raw.lower().endswith('.xlsx'):
                            filename_raw += '.xlsx'
                            
                        encoded_filename = Header(filename_raw, 'utf-8').encode()
                        
                        part.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=encoded_filename
                        )
                        
                        msg.attach(part)
                        log.info(f"Attached file với đuôi chuẩn: {filename_raw}")
                except Exception as e:
                    log.error(f"Failed to attach file {file_data['file_path']}: {e}")

        return msg

    def _generate_email_html(
        self,
        user_full_name: str,
        exam_files_data: List[Dict[str, Any]]
    ) -> str:
        """
        Generate the HTML content for the email based on new scanner format.
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

                * {{ box-sizing: border-box; margin: 0; padding: 0; }}

                body {{
                    font-family: 'Be Vietnam Pro', Arial, sans-serif;
                    background-color: #f0f0f0;
                    color: #1a1a1a;
                    line-height: 1.65;
                    -webkit-font-smoothing: antialiased;
                }}

                .wrapper {{
                    background-color: #f0f0f0;
                    padding: 36px 16px;
                }}

                .container {{
                    max-width: 680px;
                    margin: 0 auto;
                    background: #ffffff;
                    border-radius: 4px;
                    overflow: hidden;
                    box-shadow: 0 2px 12px rgba(0,0,0,0.10);
                }}

                /* ── HEADER ── */
                .header {{
                    background-color: #111111;
                    padding: 32px 36px;
                    display: flex;
                    align-items: center;
                    gap: 16px;
                }}

                .header-logo {{
                    width: 44px;
                    height: 44px;
                    background: #ffffff;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                    font-size: 20px;
                    line-height: 1;
                }}

                .header-text {{}}

                .header-eyebrow {{
                    font-size: 10px;
                    font-weight: 600;
                    letter-spacing: 2.5px;
                    text-transform: uppercase;
                    color: #999999;
                    margin-bottom: 4px;
                }}

                .header h1 {{
                    font-size: 18px;
                    font-weight: 700;
                    color: #ffffff;
                    letter-spacing: -0.2px;
                    line-height: 1.2;
                }}

                /* ── BODY ── */
                .body {{
                    padding: 36px;
                }}

                .greeting {{
                    margin-bottom: 28px;
                    padding-bottom: 24px;
                    border-bottom: 1px solid #ebebeb;
                }}

                .greeting-name {{
                    font-size: 20px;
                    font-weight: 700;
                    color: #111111;
                    margin-bottom: 8px;
                }}

                .greeting p {{
                    font-size: 14px;
                    color: #555555;
                    line-height: 1.7;
                }}

                /* ── FILE CARD ── */
                .file-card {{
                    background: #fafafa;
                    border: 1px solid #e8e8e8;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    overflow: hidden;
                }}

                .file-card-header {{
                    background: #f4f4f4;
                    border-bottom: 1px solid #e8e8e8;
                    padding: 12px 18px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}

                .file-icon {{
                    font-size: 14px;
                    line-height: 1;
                }}

                .file-label {{
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    color: #888888;
                    margin-right: 6px;
                }}

                .file-name {{
                    font-size: 13px;
                    font-weight: 600;
                    color: #222222;
                    word-break: break-all;
                }}

                .file-card-body {{
                    padding: 16px 18px;
                }}

                /* ── TABLE ── */
                .info-table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 13px;
                }}

                .info-table thead tr {{
                    background-color: #111111;
                }}

                .info-table th {{
                    padding: 10px 12px;
                    text-align: left;
                    color: #ffffff;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    white-space: nowrap;
                }}

                .info-table td {{
                    padding: 11px 12px;
                    color: #333333;
                    border-bottom: 1px solid #efefef;
                    vertical-align: top;
                    line-height: 1.5;
                }}

                .info-table tbody tr:last-child td {{
                    border-bottom: none;
                }}

                .info-table tbody tr:hover td {{
                    background-color: #f7f7f7;
                }}

                .cell-name {{
                    font-weight: 700;
                    color: #111111;
                }}

                .cell-id {{
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    color: #444444;
                    font-weight: 600;
                }}

                .cell-room {{
                    font-weight: 700;
                    color: #111111;
                }}

                /* ── EMPTY STATE ── */
                .empty-state {{
                    padding: 18px 0 4px;
                    display: flex;
                    align-items: flex-start;
                    gap: 10px;
                }}

                .empty-icon {{
                    font-size: 16px;
                    margin-top: 1px;
                    flex-shrink: 0;
                }}

                .empty-text {{
                    font-size: 13px;
                    color: #777777;
                    font-style: italic;
                    line-height: 1.6;
                }}

                /* ── NOTICE BOX ── */
                .notice {{
                    background: #f9f9f9;
                    border: 1px solid #e8e8e8;
                    border-left: 3px solid #111111;
                    border-radius: 4px;
                    padding: 20px 22px;
                    margin-top: 28px;
                }}

                .notice-title {{
                    font-size: 12px;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    color: #111111;
                    margin-bottom: 12px;
                }}

                .notice ul {{
                    padding-left: 18px;
                    list-style: none;
                }}

                .notice ul li {{
                    font-size: 13px;
                    color: #555555;
                    margin-bottom: 8px;
                    position: relative;
                    padding-left: 14px;
                    line-height: 1.6;
                }}

                .notice ul li::before {{
                    content: '—';
                    position: absolute;
                    left: 0;
                    color: #aaaaaa;
                    font-size: 11px;
                    top: 1px;
                }}

                .notice ul li:last-child {{
                    margin-bottom: 0;
                }}

                .notice ul li b {{
                    color: #111111;
                    font-weight: 700;
                }}

                /* ── FOOTER ── */
                .footer {{
                    background: #f7f7f7;
                    border-top: 1px solid #ebebeb;
                    padding: 20px 36px;
                    text-align: center;
                }}

                .footer p {{
                    font-size: 11.5px;
                    color: #aaaaaa;
                    line-height: 1.8;
                }}

                .footer .timestamp {{
                    font-size: 11px;
                    color: #cccccc;
                    margin-top: 4px;
                    font-family: 'Courier New', monospace;
                }}
            </style>
        </head>
        <body>
            <div class="wrapper">
            <div class="container">

                <!-- HEADER -->
                <div class="header">
                    <div class="header-logo">🎓</div>
                    <div class="header-text">
                        <div class="header-eyebrow">Hệ thống thông báo tự động</div>
                        <h1>Lịch Thi — Đại Học Duy Tân</h1>
                    </div>
                </div>

                <!-- BODY -->
                <div class="body">

                    <div class="greeting">
                        <div class="greeting-name">Xin chào, {user_full_name}!</div>
                        <p>Hệ thống đã quét thành công file dữ liệu công bố mới nhất.<br>
                        Dưới đây là thông tin phòng thi &amp; lịch thi tìm thấy theo đăng ký của bạn.</p>
                    </div>

        """

        # Thêm thông tin lịch thi dựa trên từng file trùng khớp
        for file_data in exam_files_data:
            exam_info = file_data.get('exam_info', [])
            file_name = file_data.get('file_name', 'Danh sách thi')

            html += f"""
                    <div class="file-card">
                        <div class="file-card-header">
                            <span class="file-icon">📄</span>
                            <span class="file-label">File gốc</span>
                            <span class="file-name">{file_name}</span>
                        </div>
                        <div class="file-card-body">
            """

            if exam_info:
                html += """
                        <table class="info-table">
                            <thead>
                                <tr>
                                    <th style="width:26%;">Họ và Tên</th>
                                    <th style="width:16%;">Mã SV</th>
                                    <th style="width:26%;">Thời Gian Thi</th>
                                    <th style="width:14%;">Phòng</th>
                                    <th style="width:18%;">Địa Điểm</th>
                                </tr>
                            </thead>
                            <tbody>
                """

                for info in exam_info:
                    html += f"""
                                <tr>
                                    <td class="cell-name">{info.get('student_name', '')}</td>
                                    <td class="cell-id">{info.get('student_id', '')}</td>
                                    <td>{info.get('exam_date_time', 'Xem file đính kèm')}</td>
                                    <td class="cell-room">{info.get('exam_room', 'Xem file đính kèm')}</td>
                                    <td>{info.get('exam_location', 'Xem file đính kèm')}</td>
                                </tr>
                    """
                html += """
                            </tbody>
                        </table>
                """
            else:
                html += """
                        <div class="empty-state">
                            <span class="empty-icon">⚠️</span>
                            <span class="empty-text">Không tìm thấy thông tin số báo danh hoặc phòng thi của bạn trong file này. Có thể bạn nằm ở danh sách phòng thi thuộc file khác.</span>
                        </div>
                """

            html += """
                        </div>
                    </div>
            """

        html += f"""
                    <!-- NOTICE -->
                    <div class="notice">
                        <div class="notice-title">💡 Lưu ý quan trọng</div>
                        <ul>
                            <li>Kiểm tra kỹ <b>Mã Sinh Viên</b> và đối chiếu với file Excel đính kèm để đảm bảo tính chính xác.</li>
                            <li>Bắt buộc mang theo <b>Thẻ sinh viên</b> hoặc giấy tờ tùy thân có dán ảnh hợp lệ.</li>
                            <li>Có mặt tại địa điểm thi trước giờ thi tối thiểu <b>15 phút</b> để hoàn tất thủ tục vào phòng.</li>
                        </ul>
                    </div>

                </div><!-- /body -->

                <!-- FOOTER -->
                <div class="footer">
                    <p>Email tự động từ DTU Exam Notifier — Vui lòng không phản hồi.</p>
                    <p>Chúc bạn hoàn thành kỳ thi thật tốt! 🎓</p>
                    <p class="timestamp">Cập nhật lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>

            </div><!-- /container -->
            </div><!-- /wrapper -->
        </body>
        </html>
        """

        return html

    def _send_email(self, msg: MIMEMultipart, to_email: str) -> bool:
        """
        Send the email using SMTP.
        Returns True if successful, False otherwise.
        """
        try:
            server = smtplib.SMTP(
                self.email_config['smtp_host'],
                self.email_config['smtp_port']
            )
            server.starttls()
            server.login(
                self.email_config['smtp_user'],
                self.email_config['smtp_password']
            )

            text = msg.as_string()
            server.sendmail(
                self.email_config['from_email'],
                to_email,
                text
            )
            server.quit()

            log.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            log.error(f"Failed to send email to {to_email}: {e}")
            return False

    def _log_email(self, subscription_id: int, exam_info: Dict[str, Any], status: str):
        """Log the email sending status to database."""
        try:
            email_log = EmailLog(
                subscription_id=subscription_id,
                email=exam_info.get('email', ''),
                status=status,
                sent_at=datetime.now()
            )
            self.db.add(email_log)
            self.db.commit()
        except Exception as e:
            log.error(f"Failed to log email: {e}")
            self.db.rollback()

    def subscribe_and_notify(
        self,
        full_name: str,
        email: str,
        subject_code: Optional[str] = None,
        subject_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main method to handle subscription and send email notification.
        Returns a dictionary with the result.
        """
        try:
            # Create subscription record
            subscription = Subscription(
                full_name=full_name,
                email=email,
                subject_code=subject_code,
                subject_name=subject_name
            )
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
            log.info(f"New subscription created: {email}")

            # Find matching exam files
            exam_files = self._find_matching_exam_files(subject_code, subject_name)

            if not exam_files:
                log.warning(f"No exam files found for subscription {subscription.id}")
                return {
                    "success": True,
                    "message": "Đăng ký thành công. Không tìm thấy file thi phù hợp.",
                    "subscription_id": subscription.id,
                    "files_found": 0
                }

            # Process each exam file
            exam_files_data = []
            for exam_file in exam_files:
                # Download the file if not already downloaded
                file_path = self._get_excel_file_path(exam_file.file_name)
                if not file_path.exists():
                    file_path = self._download_excel_file(exam_file)

                if not file_path or not file_path.exists():
                    log.warning(f"Could not download file {exam_file.file_name}")
                    continue

                # Extract user's exam information
                user_exam_info = self._extract_user_exam_info(file_path, full_name)

                exam_files_data.append({
                    'file_id': exam_file.id,
                    'file_name': exam_file.file_name,
                    'file_path': str(file_path),
                    'exam_info': user_exam_info
                })

                # Log user's exam information to email_log
                for info in user_exam_info:
                    try:
                        # Try to find the exam_schedule record
                        exam_schedule = self.db.query(ExamSchedule).filter(
                            ExamSchedule.student_name == info.get('student_name'),
                            ExamSchedule.subject_code == info.get('subject_code'),
                            ExamSchedule.exam_file_id == exam_file.id
                        ).first()

                        if exam_schedule:
                            email_log = EmailLog(
                                subscription_id=subscription.id,
                                exam_schedule_id=exam_schedule.id,
                                email=email,
                                status='pending',
                                sent_at=None
                            )
                            self.db.add(email_log)
                    except Exception as e:
                        log.debug(f"Could not log exam schedule: {e}")

            self.db.commit()

            # Create and send email
            if exam_files_data:
                msg = self._create_email_message(email, full_name, exam_files_data)
                success = self._send_email(msg, email)

                # Update email log status
                for file_data in exam_files_data:
                    for info in file_data.get('exam_info', []):
                        self._log_email(subscription.id, info, 'sent' if success else 'failed')

                return {
                    "success": True,
                    "message": f"Đăng ký thành công! Email đã được gửi đến {email}.",
                    "subscription_id": subscription.id,
                    "files_found": len(exam_files),
                    "files_with_info": len([f for f in exam_files_data if f.get('exam_info')])
                }

            return {
                "success": True,
                "message": "Đăng ký thành công. Không tìm thấy thông tin thi cho bạn.",
                "subscription_id": subscription.id,
                "files_found": len(exam_files)
            }

        except Exception as e:
            log.error(f"Error in subscribe_and_notify: {e}")
            self.db.rollback()
            return {
                "success": False,
                "message": f"Lỗi: {str(e)}",
                "error": str(e)
            }