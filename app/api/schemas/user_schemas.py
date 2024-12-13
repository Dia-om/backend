"""This module defines Pydantic schemas for user account."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountSchema(BaseModel):
    email: EmailStr
    referral_code: Optional[str]
    business_name: Optional[str]
    image_url: Optional[str]
    auth_id: Optional[str] 
    password: Optional[str] 
    album_id: Optional[str]
    image_hash: Optional[str]

class UpdateUserSchema(BaseModel):
    referral_code: Optional[str]
    business_name: Optional[str]
    image_url: Optional[str]
    auth_id: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]
    album_id: Optional[str]
    image_hash: Optional[str]

