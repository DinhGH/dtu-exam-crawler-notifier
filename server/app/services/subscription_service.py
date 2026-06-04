from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.services.email_service import EmailService, EmailTemplate
import logging

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Service for managing subscriptions"""
    
    @staticmethod
    def create_subscription(db: Session, subscription: SubscriptionCreate) -> dict:
        """
        Create new subscription
        
        Args:
            db: Database session
            subscription: Subscription data
            
        Returns:
            Dict with success status and subscription data
        """
        try:
            db_subscription = Subscription(
                full_name=subscription.full_name,
                email=subscription.email,
                subject_code=subscription.subject_code,
                subject_name=subscription.subject_name,
            )
            db.add(db_subscription)
            db.commit()
            db.refresh(db_subscription)
            
            logger.info(f"Subscription created: {subscription.email} - {subscription.subject_code}")
            return {
                "success": True,
                "message": "Đăng ký theo dõi thành công!",
                "subscription_id": db_subscription.id
            }
        except IntegrityError:
            db.rollback()
            logger.warning(f"Duplicate subscription: {subscription.email} - {subscription.subject_code}")
            return {
                "success": False,
                "message": "Bạn đã đăng ký theo dõi môn học này rồi!"
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating subscription: {str(e)}")
            return {
                "success": False,
                "message": f"Lỗi khi đăng ký: {str(e)}"
            }

    @staticmethod
    def get_subscription_by_id(db: Session, subscription_id: int) -> Subscription:
        """Get subscription by ID"""
        return db.query(Subscription).filter(
            Subscription.id == subscription_id
        ).first()

    @staticmethod
    def get_subscription_by_email_and_subject(
        db: Session,
        email: str,
        subject_code: str
    ) -> Subscription:
        """Get subscription by email and subject code"""
        return db.query(Subscription).filter(
            Subscription.email == email,
            Subscription.subject_code == subject_code
        ).first()

    @staticmethod
    def get_all_subscriptions(db: Session, skip: int = 0, limit: int = 100):
        """Get all subscriptions"""
        return db.query(Subscription).offset(skip).limit(limit).all()

    @staticmethod
    def get_subscriptions_by_email(db: Session, email: str):
        """Get all subscriptions for an email"""
        return db.query(Subscription).filter(
            Subscription.email == email
        ).all()

    @staticmethod
    def get_subscriptions_by_subject(db: Session, subject_code: str):
        """Get all subscriptions for a subject"""
        return db.query(Subscription).filter(
            Subscription.subject_code == subject_code
        ).all()

    @staticmethod
    def update_subscription(
        db: Session,
        subscription_id: int,
        update_data: SubscriptionUpdate
    ) -> dict:
        """Update subscription"""
        try:
            db_subscription = SubscriptionService.get_subscription_by_id(db, subscription_id)
            if not db_subscription:
                return {"success": False, "message": "Đăng ký không tồn tại"}
            
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(db_subscription, key, value)
            
            db.commit()
            db.refresh(db_subscription)
            
            logger.info(f"Subscription updated: {subscription_id}")
            return {"success": True, "message": "Cập nhật đăng ký thành công!"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating subscription: {str(e)}")
            return {"success": False, "message": f"Lỗi khi cập nhật: {str(e)}"}

    @staticmethod
    def cancel_subscription(db: Session, email: str, subject_code: str) -> dict:
        """Cancel subscription"""
        try:
            subscription = SubscriptionService.get_subscription_by_email_and_subject(
                db, email, subject_code
            )
            if not subscription:
                return {"success": False, "message": "Đăng ký không tồn tại"}
            
            db.delete(subscription)
            db.commit()
            
            logger.info(f"Subscription cancelled: {email} - {subject_code}")
            return {"success": True, "message": "Hủy đăng ký thành công!"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error canceling subscription: {str(e)}")
            return {"success": False, "message": f"Lỗi khi hủy đăng ký: {str(e)}"}

    @staticmethod
    def get_subscription_count(db: Session) -> int:
        """Get total subscriptions count"""
        return db.query(func.count(Subscription.id)).scalar()

    @staticmethod
    def check_subscription_exists(db: Session, email: str, subject_code: str) -> bool:
        """Check if subscription exists"""
        subscription = SubscriptionService.get_subscription_by_email_and_subject(
            db, email, subject_code
        )
        return subscription is not None
