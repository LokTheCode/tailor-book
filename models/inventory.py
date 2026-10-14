from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship

from database.database import Base
from database.base import TimestampMixin


class InventoryItem(Base, TimestampMixin):

    __tablename__ = "inventory_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=True,
        index=True
    )

    unit = Column(
        String(20),
        default="meter",
        nullable=False
    )

    quantity = Column(
        Float,
        default=0.0,
        nullable=False
    )

    minimum_quantity = Column(
        Float,
        default=5.0,
        nullable=False
    )

    cost_price = Column(
        Float,
        default=0.0
    )

    selling_price = Column(
        Float,
        default=0.0
    )

    description = Column(
        Text,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    transactions = relationship(
        "InventoryTransaction",
        back_populates="item",
        cascade="all, delete-orphan"
    )