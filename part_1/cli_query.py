"""CLI for quote queries."""
from redis import Redis
from mongoengine import connect
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv
from os import getenv

from odms import Quote
from models import QuoteModel

# redis = Redis(host='redis', port=6379)


@dataclass
class Response:
    result: str
    payload: Any


HANDLERS = {}


def register(handler):
    """Register a new handler."""
    def factory(func):
        HANDLERS[handler] = func
        return func
    return factory


@register('name')
def get_quote_by_name(name: str) -> Response:
    """Get a quote by name."""
    return Response(
        result='OK',
        payload=f"QuoteModel.objects(name={name})"
    )


@register('tag')
def get_quote_by_tag(tag: str) -> Response:
    """Get a quote by tag."""
    quotes = Quote.objects(tags=tag).all()
    payload = []
    for quote in quotes:
        quote_model = QuoteModel(**quote.to_mongo())
        payload.append(quote_model)
    return Response(
        result='OK',
        payload=payload
    )


if __name__ == "__main__":
    load_dotenv()
    ATLAS_HOST = getenv('ATLAS_HOST')
    ATLAS_PARAMS = getenv('ATLAS_PARAMS')

    connection_string = ATLAS_HOST + 'pythonweb_hw08' + ATLAS_PARAMS
    connection = connect(host=connection_string)
    while True:
        query = input("Enter a query: ")
        handler, args = query.split(':', maxsplit=1)
        if handler.lower() == "exit":
            break
        if handler not in HANDLERS:
            print(f"Unknown command: {handler}.\n"
                  f"Available commands: {', '.join(HANDLERS.keys())}, exit\n")
            continue
        response = HANDLERS[handler](args)
        print(response.result, response.payload)
