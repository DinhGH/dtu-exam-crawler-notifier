import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        is_html: bool = True,
    ) -> bool:
        """
        Send email to recipient
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            is_html: Whether body is HTML format
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.smtp_email
            msg["To"] = to_email
            
            # Attach body
            if is_html:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))
            
            # Send email
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_email, settings.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def send_notification_email(
        to_email: str,
        recipient_name: str,
        course_name: str,
        course_code: str,
        exam_date: str,
        exam_time: str,
        exam_room: str,
        file_name: str,
    ) -> bool:
        """
        Send notification email about exam list
        
        Args:
            to_email: Student email
            recipient_name: Student name
            course_name: Course name
            course_code: Course code
            exam_date: Exam date
            exam_time: Exam time
            exam_room: Exam room
            file_name: Source file name
            
        Returns:
            True if sent successfully
        """
        subject = f"[DTU] Danh sách thi: {course_name} ({course_code})"
        
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #2c3e50;">Thông báo danh sách thi</h2>
                
                <p>Xin chào <strong>{recipient_name}</strong>,</p>
                
                <p>Hệ thống đã phát hiện danh sách thi cho môn học mà bạn đã đăng ký theo dõi:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Thông tin môn học:</strong></p>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li><strong>Mã môn:</strong> {course_code}</li>
                        <li><strong>Tên môn:</strong> {course_name}</li>
                        <li><strong>Ngày thi:</strong> {exam_date}</li>
                        <li><strong>Giờ thi:</strong> {exam_time}</li>
                        <li><strong>Phòng thi:</strong> {exam_room}</li>
                        <li><strong>Tệp nguồn:</strong> {file_name}</li>
                    </ul>
                </div>
                
                <p>Vui lòng kiểm tra lại thông tin và chuẩn bị cho kỳ thi sắp tới.</p>
                
                <p style="color: #666; margin-top: 30px;">
                    Đây là email tự động từ <strong>Hệ thống tự động theo dõi và thông báo danh sách thi (DTU)</strong>.<br>
                    Vui lòng không trả lời email này.
                </p>
                
                <p style="color: #999; font-size: 12px;">
                    Nếu có thắc mắc, vui lòng liên hệ với bộ phận hỗ trợ của trường.
                </p>
            </body>
        </html>
        """
        
        return EmailService.send_email(to_email, subject, body, is_html=True)


class EmailTemplate:
    """Email templates for various notifications"""
    
    @staticmethod
    def welcome_email(name: str) -> tuple[str, str]:
        """Welcome email template"""
        subject = "[DTU] Chào mừng bạn đăng ký theo dõi danh sách thi"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Chào mừng {name}!</h2>
                <p>Cảm ơn bạn đã đăng ký theo dõi danh sách thi của Đại học Duy Tân.</p>
                <p>Bạn sẽ nhận được email thông báo ngay khi có danh sách thi cho các môn học mà bạn đã đăng ký.</p>
                <p>Hệ thống sẽ kiểm tra danh sách thi mỗi 60 phút.</p>
            </body>
        </html>
        """
        return subject, body
