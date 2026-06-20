from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic
from datetime import datetime, date

T = TypeVar('T')

class ExamFileResponse(BaseModel):
    id: int
    file_name: str
    download_link: str
    crawl_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ExamScheduleResponse(BaseModel):
    id: int
    student_id: str | None
    student_name: str | None
    subject_code: str | None
    subject_name: str | None
    exam_date: date | None
    exam_time: str | None
    exam_room: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class ExamFileDetailResponse(ExamFileResponse):
    total_records: int

class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    page_size: int
    total: int
    items: List[T]
