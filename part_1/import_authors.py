"""PythonWeb homework 08 part 1 import authors from json file to MongoDB."""
from mongoengine import connect
from models import AuthorModel
from odms import Author
import json
from dotenv import load_dotenv
from os import getenv


load_dotenv()
ATLAS_HOST = getenv('ATLAS_HOST')
ATLAS_PARAMS = getenv('ATLAS_PARAMS')

if __name__ == "__main__":
    connection_string = ATLAS_HOST+'pythonweb_hw08'+ATLAS_PARAMS
    connection = connect(host=connection_string)
    authors = []
    with open('authors.json', 'r') as file:
        authors = json.load(file)

    for author in authors:
        try:
            valid_author = AuthorModel(**author)
        except Exception as e:
            print(f"Error: {e}")
            continue
        author_doc = Author(**valid_author.model_dump(warnings=False))
        author_doc.save()
