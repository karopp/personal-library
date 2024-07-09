#!/usr/bin/env python3
import datetime
import json
import os

import firebase_admin
from firebase_admin import credentials, firestore
import yaml

from requests_html import HTMLSession
from typing import List

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)


class Book:
    def __init__(self, isbn: str, timestamp: datetime, title: str, author: str, image_url: str, link: str, review: str,
                 details: str):
        self.isbn = isbn
        self.timestamp = timestamp
        self.title = title
        self.author = author
        self.image_url = image_url
        self.link = link
        self.review = review
        self.details = details


#
# Main
#
def upload_books(script_path: str, books: List[Book]):
    cert_path = os.path.join(script_path, "karos-personal-library-firebase-adminsdk-fi04s-0384d63ca6.json")
    cred = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    for book in books:
        db.collection("books").document(book.isbn).set(vars(book))


def main():
    ratings_path = os.path.join(script_path, "content/rating.yaml")
    books_path = os.path.join(script_path, "../personalLibrary/src/assets/books.json")
    with open(ratings_path, "r") as ratings_file, open(books_path, "w") as books_file:
        ratings = yaml.safe_load(ratings_file)
        books = []
        books_object = []
        for rating in ratings:
            book = {}
            print(rating["isbn"])
            isbn = rating["isbn"]
            url = f"https://www.genialokal.de/Suche/?q={isbn}"
            session = HTMLSession()
            response = session.get(url)
            xpath = '// *[ @ id = "pagebody"] / div[2] / div[2] / div / div / div[1] / a / img'
            img = response.html.xpath(xpath)[0].attrs["src"]
            title_entry = response.html.xpath(xpath)[0].attrs["title"].split("-")
            title = title_entry[0].strip()
            author = title_entry[1].strip()
            book["image_url"] = img
            book["title"] = title
            book["author"] = author
            link = response.html.xpath(
                '//*[@id="pagebody"]/div[2]/div[2]/div/div/div[1]/a'
            )[0].absolute_links.pop()
            book["link"] = link
            book["review"] = rating["review"]
            book["details"] = rating["details"]
            books_object.append(
                Book(
                    isbn=str(isbn),
                    timestamp=datetime.datetime.now(),
                    title=title,
                    author=author,
                    image_url=img,
                    link=link,
                    review=rating["review"],
                    details=rating["details"])
            )
            books.append(book)
        books_file.seek(0)
        json.dump(books, books_file, indent=4, ensure_ascii=False)
        books_file.truncate()
        upload_books(script_path, books_object)


if __name__ == "__main__":
    main()
