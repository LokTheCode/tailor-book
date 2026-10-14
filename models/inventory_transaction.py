from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from database.database import Base
from database.base import TimestampMixin


class InventoryTransaction(Base, TimestampMixin):

    __tablename__ = "inventory_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    inventory_item_id = Column(
        Integer,
        ForeignKey("inventory_items.id"),
        nullable=False
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    reference_type = Column(
        String(50),
        nullable=True
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("admins.id"),
        nullable=True
    )

    item = relationship(
        "InventoryItem",
        back_populates="transactions"
    )