from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationHistoryResponse(BaseModel):
    """Schema for notification history response"""
    id: int
    recipient_email: str
    recipient_name: str
    course_code: str
    course_name: str
    exam_date: Optional[str]
    exam_time: Optional[str]
    exam_room: Optional[str]
    exam_file_name: Optional[str]
    email_subject: str
    status: str  # pending, sent, failed
    sent_at: Optional[datetime]
    created_at: datetime
    retry_count: int

    class Config:
        from_attributes = True


class NotificationStatistics(BaseModel):
    """Schema for notification statistics"""
    total_notifications: int
    sent_count: int
    failed_count: int
    pending_count: int
    total_emails_sent: int


class NotificationFilter(BaseModel):
    """Schema for filtering notifications"""
    email: Optional[str] = None
    course_code: Optional[str] = None
    status: Optional[str] = None  # pending, sent, failed
    page: int = 1
    limit: int = 10
