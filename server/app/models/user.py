from sqlalchemy import Column, BigInteger, String, DateTime, func
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default='user') # 'user' or 'admin'
    created_at = Column(DateTime, default=func.now())
