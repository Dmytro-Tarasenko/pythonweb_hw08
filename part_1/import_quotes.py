"""PythonWeb homework 08 part 1 import quotes from json file to MongoDB."""
from mongoengine import connect
from models import QuoteModel
from odms import Quote
import json

if __name__ == "__main__":
    connection = connect('pythonweb_hw08')
    qoutes = []
    with open("quotes.json", "r", encoding="utf-8") as file:
        qoutes = json.load(file)

    for quote in qoutes:
        try:
            valid_quote = QuoteModel(**quote)
        except Exception as e:
            print(f"Error: {e}")
            continue
        print(valid_quote.model_dump(warnings=False))
        quote_doc = Quote(**valid_quote.model_dump(warnings=False))
        quote_doc.save()
