from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SubscriptionCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name of the subscriber")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description="Email address")
    subject_code: Optional[str] = Field(None, max_length=50, description="Subject code (optional)")
    subject_name: Optional[str] = Field(None, max_length=500, description="Subject name (optional)")


class SubscriptionResponse(BaseModel):
    id: int
    full_name: str
    email: str
    subject_code: Optional[str]
    subject_name: Optional[str]
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