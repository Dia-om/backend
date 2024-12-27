"""This module defines Pydantic schemas for record"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# class RecordSchema(BaseModel):
#     title: str
#     status: str
#     content: Json[Any]


class RecordDataItem(BaseModel):
    garment: Dict[str, Any] = Field(default_factory=dict)
    measurement: Dict[str, Any] = Field(default_factory=dict)
    preference: Dict[str, Any] = Field(default_factory=dict)

class RecordCreate(BaseModel):
    title:str
    status : str | None = "pending"
    content: RecordDataItem

class RecordUpdate(BaseModel):
    status: str | None = "pending"
    date_updated: datetime = Field(default_factory=datetime.now)
    content: Optional[RecordDataItem]
