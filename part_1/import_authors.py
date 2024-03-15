"""PythonWeb homework 08 part 1 import authors from json file to MongoDB."""
from mongoengine import connect
from models import AuthorModel
from odms import Author
import json

if __name__ == "__main__":
    connection = connect('pythonweb_hw08')
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
