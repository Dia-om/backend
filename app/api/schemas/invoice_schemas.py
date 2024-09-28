"""This module defines Pydantic schemas for invoice"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Json



class InvoiceSchema(BaseModel):
    invoice_number: str
    invoice_title: str
    business_email: EmailStr
    start_date: datetime
    due_date: datetime
    status: str
    receiver_details: Json[Any]
    item_details: Json[Any]
    payment_details: Json[Any]