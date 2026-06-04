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

    def _extract_user_exam_info(self, excel_file_path: Path, user_full_name: str) -> List[Dict[str, Any]]:
        """
        Read the Excel file and extract exam information for the user.
        Looks for the user's name in the 'họ và tên' column.
        """
        try:
            # ĐÃ SỬA: Thêm header=4 để Pandas nhảy xuống dòng số 5 đọc tiêu đề cột chuẩn
            df = pd.read_excel(excel_file_path, header=4)

            # Normalize column names
            df.columns = df.columns.str.lower().str.strip()

            # Map possible name column variations
            name_columns = ['họ và tên', 'hoten', 'hovaten', 'name', 'fullname', 'ho va ten']
            name_col = None

            for col in name_columns:
                if col in df.columns:
                    name_col = col
                    break

            if not name_col:
                log.warning(f"No name column found in {excel_file_path}. Available columns: {list(df.columns)}")
                return []

            # Search for user's name
            user_rows = df[df[name_col].astype(str).str.contains(user_full_name, case=False, na=False)]

            if user_rows.empty:
                return []

            # Extract relevant information
            result = []
            for _, row in user_rows.iterrows():
                result.append({
                    'student_name': str(row.get(name_col, '')),
                    'student_id': str(row.get('mã sv', row.get('masv', ''))),
                    'subject_code': str(row.get('mã học phần', row.get('mã hp', ''))),
                    'subject_name': str(row.get('tên học phần', row.get('tên hp', ''))),
                    'exam_date': str(row.get('ngày thi', '')),
                    'exam_time': str(row.get('giờ thi', '')),
                    'exam_room': str(row.get('phòng thi', row.get('phong thi', ''))),
                })

            return result

        except Exception as e:
            log.error(f"Error extracting user info from {excel_file_path}: {e}")
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
        Generate the HTML content for the email.
        """
        # Filter out entries without exam info (just the file attachment)
        user_exam_info = [d for d in exam_files_data if d.get('exam_info')]

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                .info-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .info-table th, .info-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                .info-table th {{ background-color: #667eea; color: white; }}
                .info-table tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .file-info {{ background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; }}
                .file-info h3 {{ margin-top: 0; color: #333; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
                .no-exam-info {{ color: #666; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Thông báo Danh Sách Thi</h1>
                </div>
                <div class="content">
                    <div class="section">
                        <h2>Xin chào {user_full_name}!</h2>
                        <p>Cảm ơn bạn đã đăng ký nhận thông báo từ hệ thống. Dưới đây là thông tin về kỳ thi của bạn:</p>
                    </div>
        """

        # Add exam information for each matching file
        for file_data in exam_files_data:
            exam_info = file_data.get('exam_info', [])
            file_name = file_data.get('file_name', 'Unknown')

            html += f"""
                    <div class="file-info">
                        <h3>{file_name}</h3>
            """

            if exam_info:
                html += """
                        <table class="info-table">
                            <thead>
                                <tr>
                                    <th>Họ và tên</th>
                                    <th>Mã sinh viên</th>
                                    <th>Mã học phần</th>
                                    <th>Tên học phần</th>
                                    <th>Ngày thi</th>
                                    <th>Giờ thi</th>
                                    <th>Phòng thi</th>
                                </tr>
                            </thead>
                            <tbody>
                """

                for info in exam_info:
                    html += f"""
                                <tr>
                                    <td>{info.get('student_name', '')}</td>
                                    <td>{info.get('student_id', '')}</td>
                                    <td>{info.get('subject_code', '')}</td>
                                    <td>{info.get('subject_name', '')}</td>
                                    <td>{info.get('exam_date', '')}</td>
                                    <td>{info.get('exam_time', '')}</td>
                                    <td>{info.get('exam_room', '')}</td>
                                </tr>
                    """
                html += """
                            </tbody>
                        </table>
                """
            else:
                html += """
                        <p class="no-exam-info">Không tìm thấy thông tin thi trong file này.</p>
                """

            html += """
                    </div>
        """

        html += f"""
                    <div class="section">
                        <h2>Chi tiết kỳ thi của bạn</h2>
                        <p>Hãy kiểm tra kỹ thông tin bên trên để chuẩn bị cho kỳ thi. Nếu bạn thấy có bất kỳ sai sót nào, vui lòng liên hệ với phòng đào tạo.</p>
                    </div>

                    <div class="section">
                        <h2>Lưu ý quan trọng</h2>
                        <ul>
                            <li>Vui lòng mang theo thẻ sinh viên và giấy tờ tùy thân khi đi thi</li>
                            <li>Có mặt tại phòng thi ít nhất 15 phút trước giờ thi</li>
                            <li>Chỉ mang các vật dụng được phép vào phòng thi</li>
                            <li>Giữ điện thoại tắt hoặc để ở chế độ im lặng</li>
                        </ul>
                    </div>

                    <div class="footer">
                        <p>Đây là email tự động từ hệ thống Thông báo Danh Sách Thi.</p>
                        <p>Không trả lời email này. Liên hệ phòng đào tạo nếu có thắc mắc.</p>
                        <p>Ngày gửi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
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