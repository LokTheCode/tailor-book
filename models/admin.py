from sqlalchemy import Column, Integer, String, Boolean, Text
from database.database import Base
from database.base import TimestampMixin


class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)

    # 'super_admin', 'admin' or 'sub_admin' (see services/user_service.py)
    role = Column(String(20), default="sub_admin", nullable=False)

    # Comma separated page keys this user may open, e.g. "dashboard,customers"
    # Ignored for super_admin, who can always open everything.
    permissions = Column(Text, default="", nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
