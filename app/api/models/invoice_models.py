"""This file contains the models for the Invoices table."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(String, primary_key=True, default=uuid4().hex)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    invoice_number = Column(String(255), nullable=False)
    invoice_title = Column(String(255), nullable=False)
    business_email = Column(String(255), nullable=False)
    start_date = Column(DateTime(timezone=False), nullable=False)
    due_date = Column(DateTime(timezone=False), nullable=False)
    status = Column(String(255), nullable=False)
    receiver_details = Column(JSON, nullable=False)
    item_details = Column(JSON, nullable=False)
    payment_details = Column(JSON)
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="invoices")