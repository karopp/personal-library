#!/usr/bin/env python3

import json
import os

from requests_html import HTMLSession

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

#
# Main
#


def main():
    ratings_path = os.path.join(script_path, "content/rating.json")
    books_path = os.path.join(script_path, "../personalLibrary/src/assets/books.json")
    with open(ratings_path, "r") as ratings_file, open(books_path, "w") as books_file:
        ratings = json.load(ratings_file)
        books = []
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
            book["link"] = response.html.xpath(
                '//*[@id="pagebody"]/div[2]/div[2]/div/div/div[1]/a'
            )[0].absolute_links.pop()
            books.append(book)
        books_file.seek(0)
        json.dump(books, books_file, indent=4, ensure_ascii=False)
        books_file.truncate()


if __name__ == "__main__":
    main()
