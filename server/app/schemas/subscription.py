from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SubscriptionCreate(BaseModel):
    student_id: str = Field(..., pattern=r'^\d{11}$', description="11-digit student ID")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description="Email address")
    subject_code: Optional[str] = Field(None, max_length=50, description="Subject code (optional)")


class SubscriptionResponse(BaseModel):
    id: int
    student_id: str
    email: str
    subject_code: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionResult(BaseModel):
    success: bool
    message: str
    subscription_id: Optional[int] = None
    files_found: int = 0
    files_with_info: int = 0
    error: Optional[str] = None