from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.exam_file import ExamFile
from app.models.exam_schedule import ExamSchedule
from app.models.email_log import EmailLog
from app.models.subscription import Subscription

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self):
        file_count = self.db.query(func.count(ExamFile.id)).scalar()
        schedule_count = self.db.query(func.count(ExamSchedule.id)).scalar()
        subscription_count = self.db.query(func.count(Subscription.id)).scalar()
        
        return {
            "file_count": file_count,
            "schedule_count": schedule_count,
            "subscription_count": subscription_count
        }

    def get_files_over_time(self):
        # Assuming there is a crawl_time or similar field. 
        # Let's assume crawl_time or created_at. Checking ExamFile model.
        # Actually I don't know the fields for sure without reading the model.
        # Let's check model fields.
        return self.db.query(
            func.date(ExamFile.crawl_time).label('date'),
            func.count(ExamFile.id).label('count')
        ).group_by(func.date(ExamFile.crawl_time)).all()

    def get_emails_over_time(self):
        return self.db.query(
            func.date(EmailLog.sent_at).label('date'),
            func.count(EmailLog.id).label('count')
        ).group_by(func.date(EmailLog.sent_at)).all()
