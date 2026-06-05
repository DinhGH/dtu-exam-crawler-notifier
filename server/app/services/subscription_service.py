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
        """
        # Invalid characters for Windows filenames: < > : " / \ | ? *
        invalid_chars = r'[<>:"|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        # Also replace backslashes with forward slashes
        sanitized = sanitized.replace('\\', '/')
        # Replace date format slashes
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
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 850px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #e53e3e 0%, #b7791f 100%); color: white; padding: 25px; border-radius: 10px 10px 0 0; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 26px; font-weight: bold; }}
                .content {{ background: #f9f9f9; padding: 25px; border: 1px solid #e3e3e3; border-top: none; border-radius: 0 0 10px 10px; }}
                .section {{ margin-bottom: 25px; }}
                .section h2 {{ color: #b7791f; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; font-size: 20px; }}
                .info-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; background: white; }}
                .info-table th, .info-table td {{ border: 1px solid #cbd5e0; padding: 12px; text-align: left; font-size: 14px; }}
                .info-table th {{ background-color: #718096; color: white; font-weight: bold; }}
                .info-table tr:nth-child(even) {{ background-color: #f7fafc; }}
                .file-info {{ background: white; padding: 20px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #e53e3e; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }}
                .file-info h3 {{ margin-top: 0; color: #2d3748; font-size: 16px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 5px; }}
                .footer {{ text-align: center; padding: 20px; color: #718096; font-size: 13px; border-top: 1px solid #e2e8f0; margin-top: 30px; }}
                .no-exam-info {{ color: #e53e3e; font-style: italic; font-weight: 500; }}
                .highlight {{ font-weight: bold; color: #e53e3e; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>HỆ THỐNG THÔNG BÁO LỊCH THI ĐẠI HỌC DUY TÂN</h1>
                </div>
                <div class="content">
                    <div class="section">
                        <h2>Xin chào {user_full_name}!</h2>
                        <p>Hệ thống đã quét thành công file dữ liệu công bố mới nhất. Dưới đây là chi tiết phòng thi và lịch thi được tìm thấy theo thông tin đăng ký của bạn:</p>
                    </div>
        """

        # Thêm thông tin lịch thi dựa trên từng file trùng khớp
        for file_data in exam_files_data:
            exam_info = file_data.get('exam_info', [])
            file_name = file_data.get('file_name', 'Danh sách thi')

            html += f"""
                    <div class="file-info">
                        <h3>📄 <b>Tên File gốc:</b> {file_name}</h3>
            """

            if exam_info:
                html += """
                        <table class="info-table">
                            <thead>
                                <tr>
                                    <th style="width: 8%;">STT Phòng</th>
                                    <th style="width: 25%;">Họ và Tên</th>
                                    <th style="width: 16%;">Mã SV</th>
                                    <th style="width: 25%;">Thời Gian Thi</th>
                                    <th style="width: 17%;">Phòng</th>
                                    <th style="width: 19%;">Địa Điểm</th>
                                </tr>
                            </thead>
                            <tbody>
                """

                for info in exam_info:
                    # ĐÃ SỬA: Map chính xác các Key từ hàm Scanner mới sang bảng HTML
                    html += f"""
                                <tr>
                                    <td style="text-align: center; font-weight: bold;">{info.get('student_no', '')}</td>
                                    <td class="highlight">{info.get('student_name', '')}</td>
                                    <td>{info.get('student_id', '')}</td>
                                    <td>{info.get('exam_date_time', 'Xem chi tiết ở file đính kèm')}</td>
                                    <td><b>{info.get('exam_room', 'Xem chi tiết ở file đính kèm')}</b></td>
                                    <td>{info.get('exam_location', 'Xem chi tiết ở file đính kèm')}</td>
                                </tr>
                    """
                html += """
                            </tbody>
                        </table>
                """
            else:
                html += """
                        <p class="no-exam-info">⚠️ Không tìm thấy thông tin số báo danh hoặc phòng thi của bạn trong file này (Có thể bạn nằm ở danh sách phòng thi thuộc file khác).</p>
                """

            html += """
                    </div>
            """

        html += f"""
                    <div class="section">
                        <h2>💡 Lưu ý quan trọng cho thí sinh</h2>
                        <ul style="padding-left: 20px; color: #4a5568;">
                            <li>Vui lòng kiểm tra kỹ <b>Mã Sinh Viên</b> và đối chiếu với file Excel đính kèm để đảm bảo tính chính xác tuyệt đối.</li>
                            <li>Khi đi thi, bắt buộc phải mang theo <b>Thẻ sinh viên</b> hoặc giấy tờ tùy thân có dán ảnh hợp lệ.</li>
                            <li>Hãy có mặt tại địa điểm thi trước giờ thi tối thiểu <b>15 phút</b> để hoàn tất thủ tục vào phòng.</li>
                        </ul>
                    </div>

                    <div class="footer">
                        <p>Đây là email tự động được xử lý bởi SubscriptionService.</p>
                        <p>Vui lòng không phản hồi lại email này. Chúc bạn hoàn thành kỳ thi thật tốt!</p>
                        <p><b>Thời gian cập nhật:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
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