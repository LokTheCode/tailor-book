from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from database.base import TimestampMixin

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(String(20), nullable=False)
    delivery_date = Column(String(20), nullable=True)
    status = Column(String(30), default="pending", nullable=False) # pending, cutting, stitching, ready, delivered, cancelled
    
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    advance_amount = Column(Float, default=0.0)
    remaining_amount = Column(Float, default=0.0)
    
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("admins.id"), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("OrderPayment", back_populates="order", cascade="all, delete-orphan")