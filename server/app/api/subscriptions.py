from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
    CancelSubscriptionRequest,
    SubscriptionList,
)
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


@router.post("/register", response_model=dict)
async def register_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    """
    Register for exam notification
    Đăng ký theo dõi danh sách thi
    
    Example:
    {
        "full_name": "Nguyễn Văn A",
        "email": "student@dtu.edu.vn",
        "subject_code": "CS101",
        "subject_name": "Lập trình C++"
    }
    """
    return SubscriptionService.create_subscription(db, subscription)


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
):
    """Get subscription details by ID"""
    subscription = SubscriptionService.get_subscription_by_id(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.get("/email/{email}", response_model=list[SubscriptionList])
async def get_user_subscriptions(
    email: str,
    db: Session = Depends(get_db),
):
    """
    Get all active subscriptions for an email
    Lấy danh sách các môn học mà người dùng đang theo dõi
    """
    subscriptions = SubscriptionService.get_subscriptions_by_email(db, email)
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found")
    return subscriptions


@router.get(
    "/",
    response_model=dict,
)
async def list_subscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    List all subscriptions with pagination
    """
    subscriptions = SubscriptionService.get_all_subscriptions(db, skip, limit)
    total = SubscriptionService.get_subscription_count(db)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": sub.id,
                "full_name": sub.full_name,
                "email": sub.email,
                "subject_code": sub.subject_code,
                "subject_name": sub.subject_name,
                "created_at": sub.created_at,
            }
            for sub in subscriptions
        ],
    }


@router.put("/{subscription_id}", response_model=dict)
async def update_subscription(
    subscription_id: int,
    update_data: SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update subscription information
    Cập nhật thông tin đăng ký
    """
    return SubscriptionService.update_subscription(db, subscription_id, update_data)


@router.post("/cancel", response_model=dict)
async def cancel_subscription(
    request: CancelSubscriptionRequest,
    db: Session = Depends(get_db),
):
    """
    Cancel subscription
    Hủy theo dõi một môn học
    
    Example:
    {
        "email": "student@dtu.edu.vn",
        "subject_code": "CS101"
    }
    """
    return SubscriptionService.cancel_subscription(db, request.email, request.subject_code)


@router.get("/check/{email}/{subject_code}", response_model=dict)
async def check_subscription(
    email: str,
    subject_code: str,
    db: Session = Depends(get_db),
):
    """
    Check if subscription exists
    Kiểm tra trạng thái đăng ký
    """
    exists = SubscriptionService.check_subscription_exists(db, email, subject_code)
    return {
        "email": email,
        "subject_code": subject_code,
        "is_subscribed": exists,
    }


@router.get("/stats/count", response_model=dict)
async def get_subscription_count(
    db: Session = Depends(get_db),
):
    """Get total subscription count"""
    count = SubscriptionService.get_subscription_count(db)
    return {
        "total_subscriptions": count,
    }
