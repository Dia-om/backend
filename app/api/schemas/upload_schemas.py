"""This module defines Pydantic schemas for file uploads."""

from typing import Optional

from pydantic import BaseModel


class ImgurSchema(BaseModel):
    email: str
    album_title: Optional[str]
    album_hash: Optional[str]
    image_hash : Optional[str]
   