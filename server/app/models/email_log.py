from sqlalchemy import (Column, BigInteger, String, DateTime, 
                        ForeignKey, func)
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmailLog(Base):
    __tablename__ = 'email_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subscription_id = Column(BigInteger, ForeignKey('subscriptions.id'), nullable=False)
    exam_schedule_id = Column(BigInteger, ForeignKey('exam_schedules.id'), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    status = Column(String(50), index=True)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

    subscription = relationship("Subscription")
    exam_schedule = relationship("ExamSchedule")