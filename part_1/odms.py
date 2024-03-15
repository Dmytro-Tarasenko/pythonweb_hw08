"""ODM for the application."""
from mongoengine import (Document,
                         StringField,
                         ListField,
                         ReferenceField)


class Author(Document):
    """MongoDB Author Document"""
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    """MongoDB Quote Document"""
    author = ReferenceField(Author, required=True)
    tags = ListField(StringField())
    quote = StringField()
    meta = {'collection': 'quotes'}
