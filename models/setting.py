from sqlalchemy import Column, Integer, String, Text
from database.database import Base
from database.base import TimestampMixin

class Setting(Base, TimestampMixin):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    description = Column(String(255), nullable=True)