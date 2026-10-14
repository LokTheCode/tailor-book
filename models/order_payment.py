from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from database.base import TimestampMixin

class OrderPayment(Base, TimestampMixin):
    __tablename__ = "order_payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(String(20), nullable=False)
    payment_method = Column(String(30), default="cash", nullable=False) # cash, upi, card, bank
    reference = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("admins.id"), nullable=True)

    # Relationships
    order = relationship("Order", back_populates="payments")