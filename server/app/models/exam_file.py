from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from app.core.database import Base

class ExamFile(Base):
    __tablename__ = 'exam_files'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(500), nullable=False)  # Exact filename from website, e.g., "Tổng quan Hành vi Tổ chức trong Du lịch OB 253 (B-D-F) (17:18 29/05/2026)"
    download_link = Column(Text, nullable=False)  # Direct link to Excel file
    crawl_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
