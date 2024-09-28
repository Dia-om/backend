"""This module defines Pydantic schemas for record"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Json

class RecordSchema(BaseModel):
    title: str
    status: str
    content: Json[Any]
