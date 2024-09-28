"""This file contains the models for the UserTemplates table."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from app.database.connection import Base

class UserTemplate(Base):
    __tablename__ = 'user_template'

    id = Column(String, primary_key=True, default=uuid4().hex)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    category = Column(String(255), nullable=False)
    content = Column(JSON, nullable=False)
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="user_templates", lazy="joined")