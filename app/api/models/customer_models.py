"""This file contains the models for the Customers table."""
from datetime import datetime
from uuid import uuid4

from app.api.models.record_models import Record

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(String, primary_key=True, default=uuid4().hex)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    phone_number = Column(String(255), nullable=False)
    gender = Column(String(255))
    date_of_birth = Column(String(255))
    address = Column(String)
    occupation = Column(String(255))
    image_url = Column(String(255))
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())
    country = Column(String(255))
    state = Column(String(255))

    user = relationship("User", back_populates="customers")
    records = relationship("Record", back_populates="customer",cascade="all, delete", lazy="joined")

