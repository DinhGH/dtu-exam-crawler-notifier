from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.subscription import Subscription
from app.models.user import User
from app.api.deps import get_current_user
from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionResult,
)
from app.utils.logger import log

router = APIRouter()


@router.post("", response_model=SubscriptionResult)
def create_subscription(
    subscription: SubscriptionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new subscription and send email notification with exam information.
    The system will search for exam files matching the provided subject code/name
    and send an email containing the user's exam information extracted from Excel files.
    """
    log.info(f"New subscription request: {subscription.email}, subject_code={subscription.subject_code} by user={current_user.username}")

    try:
        service = SubscriptionService(db)
        # Note: Need to update SubscriptionService.create_subscription to accept user_id
        # For now, I will modify it here or assume I need to update it
        subscription_obj = service.create_subscription(
            full_name=subscription.full_name,
            email=subscription.email,
            subject_code=subscription.subject_code,
            subject_name=subscription.subject_name,
            user_id=current_user.id
        )
        
        # Trigger background processing
        background_tasks.add_task(service.process_subscription_async, subscription_obj.id)
        
        return {
            "success": True,
            "message": "Đăng ký thành công! Hệ thống đang xử lý và sẽ gửi email cho bạn.",
            "subscription_id": subscription_obj.id
        }
    except Exception as e:
        log.error(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[SubscriptionResponse])
def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all subscriptions for current user.
    """
    log.info(f"Fetching subscriptions for user={current_user.username}: skip={skip}, limit={limit}")

    try:
        subscriptions = db.query(Subscription).filter(Subscription.user_id == current_user.id).offset(skip).limit(limit).all()
        return subscriptions
    except Exception as e:
        log.error(f"Error fetching subscriptions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email/{email}", response_model=List[SubscriptionResponse])
def get_subscription_by_email(
    email: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve subscriptions by email address.
    """
    log.info(f"Fetching subscription for email: {email}")

    try:
        subscriptions = db.query(Subscription).filter(Subscription.email == email).all()
        return subscriptions
    except Exception as e:
        log.error(f"Error fetching subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription_by_id(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single subscription by ID.
    """
    log.info(f"Fetching subscription id={subscription_id} for user={current_user.username}")
    try:
        subscription = db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        ).first()
        if not subscription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return subscription
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error fetching subscription by id: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    payload: SubscriptionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing subscription.
    """
    log.info(f"Updating subscription id={subscription_id} for user={current_user.username}")
    try:
        subscription = db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        ).first()
        if not subscription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")

        subscription.full_name = payload.full_name
        subscription.email = payload.email
        subscription.subject_code = payload.subject_code
        subscription.subject_name = payload.subject_name

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        # Trigger notification check after update using background task
        background_tasks.add_task(SubscriptionService(db).process_subscription_async, subscription.id)

        return subscription
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating subscription: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{subscription_id}", response_model=dict)
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a subscription by ID.
    """
    log.info(f"Deleting subscription id={subscription_id} for user={current_user.username}")
    try:
        subscription = db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        ).first()
        if not subscription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")

        db.delete(subscription)
        db.commit()

        return {"success": True, "message": "Subscription deleted"}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting subscription: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))