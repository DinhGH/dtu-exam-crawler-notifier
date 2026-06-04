from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.subscription import Subscription
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
    db: Session = Depends(get_db),
):
    """
    Create a new subscription and send email notification with exam information.
    The system will search for exam files matching the provided subject code/name
    and send an email containing the user's exam information extracted from Excel files.
    """
    log.info(f"New subscription request: {subscription.email}, subject_code={subscription.subject_code}")

    try:
        service = SubscriptionService(db)
        result = service.subscribe_and_notify(
            full_name=subscription.full_name,
            email=subscription.email,
            subject_code=subscription.subject_code,
            subject_name=subscription.subject_name,
        )
        return result
    except Exception as e:
        log.error(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[SubscriptionResponse])
def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve all subscriptions (for admin purposes).
    """
    log.info(f"Fetching subscriptions: skip={skip}, limit={limit}")

    try:
        subscriptions = db.query(Subscription).offset(skip).limit(limit).all()
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
