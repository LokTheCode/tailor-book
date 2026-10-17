from sqlalchemy import Column, ForeignKey, Integer, String, Text

from database.base import TimestampMixin
from database.database import Base


class MessageLog(Base, TimestampMixin):
    """Every WhatsApp / email the app tried to send, and what happened."""

    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, index=True)

    channel = Column(String(20), nullable=False)   # whatsapp / email
    event = Column(String(40), nullable=False)     # order_created / order_ready / order_delivered / marketing / test
    recipient = Column(String(150), nullable=False)
    status = Column(String(20), nullable=False)    # sent / failed
    detail = Column(Text, nullable=True)           # error message or API response
