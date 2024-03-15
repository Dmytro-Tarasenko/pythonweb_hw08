"""CLI for quote queries."""
from redis import Redis
from mongoengine import connect

from odms import Quote
from models import QuoteModel, AuthorModel