"""PythonWeb homework 08 part 1 import quotes from json file to MongoDB."""
from mongoengine import connect
from models import QuoteModel
from odms import Quote
import json
from dotenv import load_dotenv
from os import getenv


load_dotenv()
ATLAS_HOST = getenv('ATLAS_HOST')
ATLAS_PARAMS = getenv('ATLAS_PARAMS')

if __name__ == "__main__":
    connection_string = ATLAS_HOST+'pythonweb_hw08'+ATLAS_PARAMS
    connection = connect(host=connection_string)
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
