from sqlalchemy import Column, BigInteger, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from app.models import Base


class Subscription(Base):
    """
    Model for user subscription to exam notifications
    Lưu thông tin đăng ký theo dõi danh sách thi của sinh viên
    """
    __tablename__ = "subscriptions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)  # Họ và tên
    email = Column(String(255), nullable=False, index=True)  # Email
    subject_code = Column(String(50), nullable=False, index=True)  # Mã môn học
    subject_name = Column(String(500))
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint("email", "subject_code", name="unique_email_subject"),
    )

    def __repr__(self):
        return f"<Subscription(id={self.id}, email={self.email}, subject={self.subject_code})>"
