"""This file contains the models for the Records table."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Record(Base):
    __tablename__ = 'record'

    id = Column(String, primary_key=True, default=uuid4().hex)
    customer_id = Column(String, ForeignKey('customer.id'), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(255))
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())
    content = Column(JSON, nullable=False)

    customer = relationship("Customer", back_populates="records")