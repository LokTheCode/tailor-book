from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base
from database.base import TimestampMixin

class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="sub_admin", nullable=False) # 'admin' or 'sub_admin'
    is_active = Column(Boolean, default=True, nullable=False)