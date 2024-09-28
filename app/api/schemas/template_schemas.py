"""This module defines Pydantic schemas for template"""

from typing import Any

from pydantic import BaseModel, Json



class TemplateSchema(BaseModel):
    category: str
    content: Json[Any]