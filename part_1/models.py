"""Model definitions for Author and Quote documents"""
from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional, List


class AuthorModel(BaseModel):
    """Data model for Author Document"""
    @field_validator('born_date')
    def validate_born_date(cls, value):
        try:
            date_ = datetime.strptime(value, '%B %d, %Y')
        except ValueError:
            raise ValueError('Invalid date format. Example: May 1, 1999')
        if date_ > datetime.now():
            raise ValueError('Born date cannot be in the future.')
        return value

    fullname: str
    born_date: Optional[str] = None
    born_location: Optional[str] = None
    description: Optional[str] = None


class Tag(BaseModel):
    """Data model for Tag Embedded Document"""
    tag: str


class QuoteModel(BaseModel):
    """Data model for Quote Document"""
    author: str
    tags: Optional[List[str]] = []
    quote: Optional[str] = None
