from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from app.core.database import Base

class ExamFile(Base):
    __tablename__ = 'exam_files'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    detail_url = Column(Text, unique=True, nullable=False)
    file_url = Column(Text, unique=True, nullable=False, index=True)
    file_name = Column(String(500))
    exam_subject_code = Column(String(50))  # Subject code like "CS 201", "HRM 303"
    crawl_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
