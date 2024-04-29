

import os
import sqlite3 as sqlite
import random
import base64
import simplejson as json
import pymongo

class Book:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    currency_unit: str
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: [str]
    pictures: [bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bookstore"]
        self.collection = self.db["book"]

    def get_book_count(self):
        return self.collection.count_documents({})

    def get_book_info(self, start, size) -> [Book]:
        books = []
        cursor = self.collection.find().skip(start).limit(size)
        for doc in cursor:
            book = Book()
            book.id = doc.get("id")
            book.title = doc.get("title")
            book.author = doc.get("author")
            book.publisher = doc.get("publisher")
            book.original_title = doc.get("original_title")
            book.translator = doc.get("translator")
            book.pub_year = doc.get("pub_year")
            book.pages = doc.get("pages")
            book.price = doc.get("price")
            book.currency_unit = doc.get("currency_unit")
            book.binding = doc.get("binding")
            book.isbn = doc.get("isbn")
            book.author_intro = doc.get("author_intro")
            book.book_intro = doc.get("book_intro")
            book.content = doc.get("content")
            tags = doc.get("tags")
            if tags:
                book.tags = tags.split("\n")
            pictures = doc.get("picture")
            if pictures:
                # for picture in pictures:
                #     picture_str = picture.toString()
                #     decoded_bytes = base64.b64decode(picture_str)
                #     encode_str = decoded_bytes.decode("utf-8")
                #     book.pictures.append(encode_str)
                pictures=str(doc.get("picture"))


            books.append(book)
            print(book)
        return books
