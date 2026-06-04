from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.notification import NotificationHistory
from app.models.subscription import Subscription
from app.services.email_service import EmailService
from app.services.subscription_service import SubscriptionService
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for managing notifications and data reconciliation"""
    
    @staticmethod
    def create_notification(
        db: Session,
        recipient_email: str,
        recipient_name: str,
        course_code: str,
        course_name: str,
        exam_date: str,
        exam_time: str,
        exam_room: str,
        exam_file_name: str,
        email_subject: str,
        email_body: str,
    ) -> NotificationHistory:
        """Create notification history record"""
        try:
            notification = NotificationHistory(
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                course_code=course_code,
                course_name=course_name,
                exam_date=exam_date,
                exam_time=exam_time,
                exam_room=exam_room,
                exam_file_name=exam_file_name,
                email_subject=email_subject,
                email_body=email_body,
                status="pending",
            )
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
            logger.info(f"Notification created: ID={notification.id}, Email={recipient_email}")
            return notification
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating notification: {str(e)}")
            raise

    @staticmethod
    def send_notification(
        db: Session,
        notification_id: int,
    ) -> bool:
        """
        Send notification email and update status
        
        Args:
            db: Database session
            notification_id: Notification ID
            
        Returns:
            True if sent successfully
        """
        try:
            notification = db.query(NotificationHistory).filter(
                NotificationHistory.id == notification_id
            ).first()
            
            if not notification:
                logger.error(f"Notification not found: {notification_id}")
                return False
            
            # Send email
            success = EmailService.send_notification_email(
                to_email=notification.recipient_email,
                recipient_name=notification.recipient_name,
                course_name=notification.course_name,
                course_code=notification.course_code,
                exam_date=notification.exam_date,
                exam_time=notification.exam_time,
                exam_room=notification.exam_room,
                file_name=notification.exam_file_name,
            )
            
            if success:
                notification.status = "sent"
                notification.sent_at = datetime.utcnow()
                
                db.commit()
                logger.info(f"Notification sent: ID={notification_id}, Email={notification.recipient_email}")
                return True
            else:
                notification.status = "failed"
                notification.retry_count += 1
                if notification.retry_count > 3:
                    notification.error_message = "Exceeded maximum retry attempts"
                db.commit()
                logger.error(f"Failed to send notification: {notification_id}")
                return False
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error sending notification: {str(e)}")
            return False

    @staticmethod
    def get_notification_by_id(db: Session, notification_id: int) -> NotificationHistory:
        """Get notification by ID"""
        return db.query(NotificationHistory).filter(
            NotificationHistory.id == notification_id
        ).first()

    @staticmethod
    def get_notifications(
        db: Session,
        email: str = None,
        course_code: str = None,
        status: str = None,
        skip: int = 0,
        limit: int = 20,
    ):
        """Get notifications with filters"""
        query = db.query(NotificationHistory)
        
        if email:
            query = query.filter(NotificationHistory.recipient_email == email)
        if course_code:
            query = query.filter(NotificationHistory.course_code == course_code)
        if status:
            query = query.filter(NotificationHistory.status == status)
        
        return query.order_by(
            NotificationHistory.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_notification_count(
        db: Session,
        email: str = None,
        course_code: str = None,
        status: str = None,
    ) -> int:
        """Get total notification count with filters"""
        query = db.query(func.count(NotificationHistory.id))
        
        if email:
            query = query.filter(NotificationHistory.recipient_email == email)
        if course_code:
            query = query.filter(NotificationHistory.course_code == course_code)
        if status:
            query = query.filter(NotificationHistory.status == status)
        
        return query.scalar()

    @staticmethod
    def get_notification_statistics(db: Session) -> dict:
        """Get notification statistics"""
        total = db.query(func.count(NotificationHistory.id)).scalar()
        sent = db.query(func.count(NotificationHistory.id)).filter(
            NotificationHistory.status == "sent"
        ).scalar()
        failed = db.query(func.count(NotificationHistory.id)).filter(
            NotificationHistory.status == "failed"
        ).scalar()
        pending = db.query(func.count(NotificationHistory.id)).filter(
            NotificationHistory.status == "pending"
        ).scalar()
        
        return {
            "total_notifications": total,
            "sent_count": sent,
            "failed_count": failed,
            "pending_count": pending,
        }

    @staticmethod
    def reconcile_and_notify(
        db: Session,
        exam_list_data: list,
        exam_file_name: str,
    ) -> dict:
        """
        Reconcile exam data with subscriptions and create notifications
        Kiểm tra dữ liệu thi mới và tạo thông báo cho người dùng phù hợp
        
        Args:
            db: Database session
            exam_list_data: List of exam records from file
            exam_file_name: Source file name
            
        Returns:
            Dict with statistics about created notifications
        """
        try:
            created_count = 0
            skipped_count = 0
            error_count = 0
            
            # Get all active subscriptions
            subscriptions = SubscriptionService.get_all_subscriptions(db)
            
            for exam_record in exam_list_data:
                try:
                    course_code = exam_record.get("course_code") or exam_record.get("mã_môn")
                    
                    # Find matching subscriptions
                    matching_subs = [
                        sub for sub in subscriptions
                        if sub.subject_code.lower() == course_code.lower()
                    ]
                    
                    for subscription in matching_subs:
                        # Check if already notified for this exam
                        existing = db.query(NotificationHistory).filter(
                            NotificationHistory.recipient_email == subscription.email,
                            NotificationHistory.course_code == course_code,
                            NotificationHistory.exam_file_name == exam_file_name,
                            NotificationHistory.status == "sent",
                        ).first()
                        
                        if existing:
                            skipped_count += 1
                            continue
                        
                        # Create notification
                        notification = NotificationService.create_notification(
                            db=db,
                            recipient_email=subscription.email,
                            recipient_name=subscription.full_name,
                            course_code=course_code,
                            course_name=subscription.subject_name,
                            exam_date=exam_record.get("exam_date") or exam_record.get("ngày_thi"),
                            exam_time=exam_record.get("exam_time") or exam_record.get("giờ_thi"),
                            exam_room=exam_record.get("exam_room") or exam_record.get("phòng_thi"),
                            exam_file_name=exam_file_name,
                            email_subject=f"[DTU] Danh sách thi: {subscription.subject_name}",
                            email_body="",  # Will be formatted by email service
                        )
                        
                        # Send notification immediately
                        NotificationService.send_notification(db, notification.id)
                        created_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing exam record: {str(e)}")
                    error_count += 1
                    continue
            
            return {
                "success": True,
                "created_notifications": created_count,
                "skipped_notifications": skipped_count,
                "error_count": error_count,
                "message": f"Tạo {created_count} thông báo, bỏ qua {skipped_count}"
            }
            
        except Exception as e:
            logger.error(f"Error in reconciliation: {str(e)}")
            return {
                "success": False,
                "message": f"Lỗi trong quá trình đối chiếu dữ liệu: {str(e)}"
            }

    @staticmethod
    def get_pending_notifications(db: Session, limit: int = 100):
        """Get pending notifications to send"""
        return db.query(NotificationHistory).filter(
            NotificationHistory.status == "pending",
            NotificationHistory.retry_count < 3,
        ).limit(limit).all()

    @staticmethod
    def retry_failed_notifications(db: Session) -> dict:
        """Retry sending failed notifications"""
        try:
            failed_notifications = db.query(NotificationHistory).filter(
                NotificationHistory.status == "failed",
                NotificationHistory.retry_count < 3,
            ).all()
            
            success_count = 0
            for notification in failed_notifications:
                if NotificationService.send_notification(db, notification.id):
                    success_count += 1
            
            return {
                "success": True,
                "retried_count": len(failed_notifications),
                "success_count": success_count,
            }
        except Exception as e:
            logger.error(f"Error retrying notifications: {str(e)}")
            return {"success": False, "message": str(e)}
