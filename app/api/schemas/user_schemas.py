"""This module defines Pydantic schemas for user account."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountSchema(BaseModel):
    email: EmailStr
    referral_code: Optional[str]
    business_name: Optional[str]
    image_url: Optional[str]
    auth_id: Optional[str] # used for storing imgur deleteHash at the moment
    password: Optional[str] # used for storing  imgur album_id at the moment

class UpdateUserSchema(BaseModel):
    referral_code: Optional[str]
    business_name: Optional[str]
    image_url: Optional[str]
    auth_id: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]

