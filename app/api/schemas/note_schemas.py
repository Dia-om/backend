"""This module defines Pydantic schemas for note"""

from typing import Any

from pydantic import BaseModel, Json



class NoteSchema(BaseModel):
    title: str
    content: Json[Any]