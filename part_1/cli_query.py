"""CLI for quote queries."""
from redis import Redis
from mongoengine import connect
from dataclasses import dataclass
from typing import Any, List
from dotenv import load_dotenv
from os import getenv
from rich.console import Console
from rich.table import Table

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
    try:
        quotes = Quote.objects(author=name).all()
    except Exception as e:
        return Response(
            result='Error',
            payload=str(e)
        )
    payload = []
    for quote in quotes:
        quote_model = QuoteModel(**quote.to_mongo())
        payload.append(quote_model)
    return Response(
        result='OK',
        payload=payload
    )


@register('tag')
def get_quote_by_tag(tag: str) -> Response:
    """Get a quote by tag."""
    try:
        quotes = Quote.objects(tags=tag).all()
    except Exception as e:
        return Response(
            result='Error',
            payload=str(e)
        )
    payload = []
    for quote in quotes:
        quote_model = QuoteModel(**quote.to_mongo())
        payload.append(quote_model)
    return Response(
        result='OK',
        payload=payload
    )


def print_models(models: List[Any]) -> None:
    """Print models."""
    if not models:
        print("No results.")
        return

    table = Table(title="Results")
    table.add_column("#")
    for key in models[0].model_fields:
        table.add_column(key)
    for i, model in enumerate(models):
        fields = [str(i+1)]
        for field in model.model_fields:
            if isinstance(model.__getattribute__(field), list):
                fields.append(", ".join(model.__getattribute__(field)))
            else:
                fields.append(str(model.__getattribute__(field)))
        table.add_row(*fields)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    load_dotenv()
    ATLAS_HOST = getenv('ATLAS_HOST')
    ATLAS_PARAMS = getenv('ATLAS_PARAMS')

    connection_string = ATLAS_HOST + 'pythonweb_hw08' + ATLAS_PARAMS
    connection = connect(host=connection_string, ssl=False)
    while True:
        query = input("Enter a query: ")
        handler, *args = query.split(':', maxsplit=1)

        if handler.lower() == "exit":
            break
        if handler not in HANDLERS:
            print(f"Unknown command: {handler}.\n"
                  f"Available commands: {', '.join(HANDLERS.keys())}, exit\n")
            continue

        response = HANDLERS[handler](*args)

        if response.result == "OK":
            print_models(response.payload)
        else:
            print(f"Error: {response.payload}")
