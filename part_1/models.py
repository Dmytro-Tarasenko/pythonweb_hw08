"""Model definitions for Author and Quote documents"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, field_validator


class AuthorModel(BaseModel):
    """Data model for Author Document"""
    @field_validator('born_date')
    @staticmethod
    def validate_born_date(value):
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


class QuoteModel(BaseModel):
    """Data model for Quote Document"""
    author: Any
    author_name: Optional[str] = None
    tags: Optional[List[str]] = []
    quote: Optional[str] = None
