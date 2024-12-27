"""This file contains the models for the Notes table."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Note(Base):
    __tablename__ = 'note'

    id = Column(String, primary_key=True, default=uuid4().hex)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    title = Column(String(255), nullable=False)
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())
    content = Column(String, nullable=False)

    user = relationship("User", back_populates="notes")