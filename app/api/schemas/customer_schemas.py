"""This module defines Pydantic schemas for customer"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr



class CustomerSchema(BaseModel):
    name: str
    email: Optional[str]
    phone_number: str
    gender: Optional[str]
    date_of_birth: Optional[str]
    address: Optional[str]
    occupation: Optional[str]
    image_url: Optional[str]
    country: Optional[str]
    state: Optional[str]