from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from app.models import Base


class NotificationHistory(Base):
    """
    Model for storing notification sending history
    Lưu lịch sử gửi email thông báo
    """
    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(255), nullable=False)  # Địa chỉ email nhận
    recipient_name = Column(String(255), nullable=False)  # Tên người nhận
    course_code = Column(String(50), nullable=False)  # Mã môn học
    course_name = Column(String(255), nullable=False)  # Tên môn học
    exam_date = Column(String(50), nullable=True)  # Ngày thi
    exam_time = Column(String(50), nullable=True)  # Giờ thi
    exam_room = Column(String(100), nullable=True)  # Phòng thi
    exam_file_name = Column(String(255), nullable=True)  # Tên tệp danh sách thi
    email_subject = Column(String(500), nullable=False)  # Tiêu đề email
    email_body = Column(Text, nullable=False)  # Nội dung email
    status = Column(String(50), default="pending")  # Trạng thái: pending, sent, failed
    error_message = Column(Text, nullable=True)  # Thông báo lỗi nếu có
    sent_at = Column(DateTime, nullable=True)  # Thời gian gửi thực tế
    created_at = Column(DateTime, server_default=func.now())  # Thời gian tạo
    retry_count = Column(Integer, default=0)  # Số lần thử lại

    def __repr__(self):
        return f"<NotificationHistory(id={self.id}, email={self.recipient_email}, status={self.status})>"
