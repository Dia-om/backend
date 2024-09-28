"""This file contains the models for the Users table."""
from datetime import datetime
from uuid import uuid4

# import models for purpose of populating
from app.api.models.template_models import UserTemplate
from app.api.models.draft_models import Draft
from app.api.models.invoice_models import Invoice
from app.api.models.customer_models import Customer
from app.api.models.note_models import Note

from sqlalchemy import Boolean, text, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.database.connection import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, default=uuid4().hex)
    email = Column(String(255), unique=True)
    user_code = Column(String(255))
    password = Column(String(255))
    phone_number = Column(String(255))
    business_name = Column(String(255))
    image_url = Column(String)
    auth_id = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())
    date_deleted = Column(DateTime)

    user_templates = relationship("UserTemplate", back_populates="user", cascade="all, delete", lazy="joined")
    drafts = relationship("Draft", back_populates="user", cascade="all, delete", lazy="joined")
    notes = relationship("Note", back_populates="user",cascade="all, delete", lazy="joined")
    invoices = relationship("Invoice", back_populates="user",cascade="all, delete", lazy="joined")
    customers = relationship("Customer", back_populates="user",cascade="all, delete", lazy="joined")
