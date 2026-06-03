from sqlalchemy import (Column, BigInteger, String, Date, DateTime, 
                        ForeignKey, UniqueConstraint, func)
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExamSchedule(Base):
    __tablename__ = 'exam_schedules'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    exam_file_id = Column(BigInteger, ForeignKey('exam_files.id'), nullable=False)
    student_id = Column(String(50), index=True)
    student_name = Column(String(255), index=True)
    subject_code = Column(String(50), index=True)
    subject_name = Column(String(500))
    exam_date = Column(Date)
    exam_time = Column(String(100))
    exam_room = Column(String(100))
    created_at = Column(DateTime, default=func.now())

    exam_file = relationship("ExamFile")

    __table_args__ = (
        UniqueConstraint('exam_file_id', 'student_id', 'subject_code', name='_exam_file_student_subject_uc'),
    )