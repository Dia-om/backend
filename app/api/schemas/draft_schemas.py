"""This module defines Pydantic schemas for draft"""

from typing import Any

from pydantic import BaseModel, Json



class DraftSchema(BaseModel):
    category: str
    draft_content: Json[Any]