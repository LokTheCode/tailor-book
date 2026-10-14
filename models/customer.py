from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from database.database import Base
from database.base import TimestampMixin

class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False, index=True)
    alternate_mobile = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    gender = Column(String(10), default="Male")  # Male, Female, Other
    customer_type = Column(String(20), default="regular")  # regular, vip, business
    reference = Column(String(50), nullable=True)  # Walk-in, Google, Friend, etc.
    address = Column(Text, nullable=True)
    photo = Column(String(255), nullable=True)  # File path or filename
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    measurements = relationship("CustomerMeasurement", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer")