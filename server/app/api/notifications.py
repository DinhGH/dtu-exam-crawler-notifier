from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notification import (
    NotificationHistoryResponse,
    NotificationStatistics,
)
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/", response_model=dict)
async def list_notifications(
    email: str = Query(None),
    course_code: str = Query(None),
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    List notifications with filters
    Lấy danh sách lịch sử thông báo
    
    Parameters:
    - email: Filter by recipient email
    - course_code: Filter by course code
    - status: Filter by status (pending, sent, failed)
    - skip: Number of records to skip
    - limit: Number of records to return
    """
    notifications = NotificationService.get_notifications(
        db,
        email=email,
        course_code=course_code,
        status=status,
        skip=skip,
        limit=limit,
    )
    total = NotificationService.get_notification_count(
        db,
        email=email,
        course_code=course_code,
        status=status,
    )
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": notif.id,
                "recipient_email": notif.recipient_email,
                "recipient_name": notif.recipient_name,
                "course_code": notif.course_code,
                "course_name": notif.course_name,
                "exam_date": notif.exam_date,
                "exam_time": notif.exam_time,
                "exam_room": notif.exam_room,
                "exam_file_name": notif.exam_file_name,
                "status": notif.status,
                "sent_at": notif.sent_at,
                "created_at": notif.created_at,
                "retry_count": notif.retry_count,
            }
            for notif in notifications
        ],
    }


@router.get("/{notification_id}", response_model=dict)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    """Get notification details by ID"""
    notification = NotificationService.get_notification_by_id(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {
        "id": notification.id,
        "recipient_email": notification.recipient_email,
        "recipient_name": notification.recipient_name,
        "course_code": notification.course_code,
        "course_name": notification.course_name,
        "exam_date": notification.exam_date,
        "exam_time": notification.exam_time,
        "exam_room": notification.exam_room,
        "exam_file_name": notification.exam_file_name,
        "email_subject": notification.email_subject,
        "status": notification.status,
        "sent_at": notification.sent_at,
        "created_at": notification.created_at,
        "retry_count": notification.retry_count,
        "error_message": notification.error_message,
    }


@router.get("/email/{email}", response_model=dict)
async def get_user_notifications(
    email: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Get notification history for a specific email
    Xem lịch sử gửi email cho một người dùng
    """
    notifications = NotificationService.get_notifications(
        db,
        email=email,
        skip=skip,
        limit=limit,
    )
    total = NotificationService.get_notification_count(db, email=email)
    
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this email")
    
    return {
        "total": total,
        "email": email,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": notif.id,
                "course_code": notif.course_code,
                "course_name": notif.course_name,
                "exam_date": notif.exam_date,
                "status": notif.status,
                "sent_at": notif.sent_at,
                "created_at": notif.created_at,
            }
            for notif in notifications
        ],
    }


@router.get("/stats/summary", response_model=dict)
async def get_notification_statistics(
    db: Session = Depends(get_db),
):
    """
    Get notification statistics
    Thống kê số lượng email đã gửi
    """
    stats = NotificationService.get_notification_statistics(db)
    return {
        "total_notifications": stats["total_notifications"],
        "sent_count": stats["sent_count"],
        "failed_count": stats["failed_count"],
        "pending_count": stats["pending_count"],
    }


@router.post("/retry", response_model=dict)
async def retry_failed_notifications(
    db: Session = Depends(get_db),
):
    """
    Retry sending failed notifications
    Thử gửi lại các email thất bại
    """
    return NotificationService.retry_failed_notifications(db)


@router.post("/send/{notification_id}", response_model=dict)
async def send_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    """
    Manually send a notification
    Gửi thủ công một thông báo
    """
    notification = NotificationService.get_notification_by_id(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    success = NotificationService.send_notification(db, notification_id)
    if success:
        return {
            "success": True,
            "message": "Notification sent successfully",
            "notification_id": notification_id,
        }
    else:
        return {
            "success": False,
            "message": "Failed to send notification",
            "notification_id": notification_id,
        }
