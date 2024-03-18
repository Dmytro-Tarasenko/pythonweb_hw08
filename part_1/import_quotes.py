"""PythonWeb homework 08 part 1 import quotes from json file to MongoDB."""
import json
from os import getenv

from mongoengine import connect
from models import QuoteModel
from odms import Quote, Author
from dotenv import load_dotenv


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
            valid_quote = QuoteModel(author_name=quote["author"], **quote)
        except Exception as e:
            print(f"Error: {e}")
            continue
        author_id = Author.objects(fullname=quote["author"]).first().id
        valid_quote = valid_quote.copy(update={"author": author_id},
                                       deep=True)
        print(valid_quote.model_dump(warnings=False, exclude=["author_name"]))
        quote_doc = Quote(**valid_quote.model_dump(warnings=False, exclude=["author_name"]))
        quote_doc.save()
