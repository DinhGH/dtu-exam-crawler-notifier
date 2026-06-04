from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Generic message response"""
    success: bool
    message: str
    data: dict = {}


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    error_code: str = "ERROR"
