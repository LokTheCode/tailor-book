from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from database.base import TimestampMixin

class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    garment_type = Column(String(100), nullable=False) # e.g. Shirt, Pant, Suit
    description = Column(String(255), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    measurement_id = Column(Integer, ForeignKey("customer_measurements.id"), nullable=True)

    # Relationships
    order = relationship("Order", back_populates="items")