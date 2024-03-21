"""MongoDB model"""
from mongoengine import Document, StringField, EmailField, BooleanField


class Contact(Document):
    """MongoDB model for the Contact document."""
    name = StringField(required=True)
    email = EmailField()
    phone_number = StringField()
    preferred = StringField(choices=["email", "sms"])
    is_sent = BooleanField(default=False)
    meta = {"collection": "contacts"}
