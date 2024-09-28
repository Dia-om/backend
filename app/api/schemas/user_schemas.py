"""This module defines Pydantic schemas for user account."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountSchema(BaseModel):
    email: EmailStr
    referral_code: Optional[str]
    business_name: Optional[str]
    image_url: Optional[str]
    auth_id: Optional[str]

class UserSchema(BaseModel):
    phone_number: str
    business_name: str
    image_url: Optional[str]
    auth_id: Optional[str]