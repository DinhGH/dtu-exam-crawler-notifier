from sqlalchemy import Column, BigInteger, String, DateTime, func
from app.core.database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    subject_code = Column(String(50), index=True)
    subject_name = Column(String(500))
    created_at = Column(DateTime, default=func.now())