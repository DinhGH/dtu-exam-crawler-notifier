from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class SubscriptionCreate(BaseModel):
    """Schema for creating a new subscription"""
    full_name: str
    email: EmailStr
    subject_code: str
    subject_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Nguyễn Văn A",
                "email": "student@dtu.edu.vn",
                "subject_code": "CS101",
                "subject_name": "Lập trình C++"
            }
        }


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription"""
    full_name: Optional[str] = None
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None


class SubscriptionResponse(BaseModel):
    """Schema for subscription response"""
    id: int
    full_name: str
    email: str
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionList(BaseModel):
    """Schema for subscription list response"""
    id: int
    full_name: str
    email: str
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CancelSubscriptionRequest(BaseModel):
    """Schema for canceling subscription"""
    email: EmailStr
    subject_code: str
