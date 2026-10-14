from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.database import Base
from database.base import TimestampMixin

class CustomerMeasurement(Base, TimestampMixin):
    __tablename__ = "customer_measurements"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    measurement_name = Column(String(100), nullable=False)  # e.g., "Regular Fit", "Suit 2026"
    
    # Store structured JSON objects directly
    upper_measurements = Column(JSON, nullable=True)  # {"shoulder": 18, "chest": 40, ...}
    lower_measurements = Column(JSON, nullable=True)  # {"waist": 34, "hip": 40, ...}
    extra_measurements = Column(JSON, nullable=True)  # {"neck": 15, "armhole": 18, ...}
    
    notes = Column(Text, nullable=True)

    # Relationship
    customer = relationship("Customer", back_populates="measurements")