# import os
# import sqlite3 as sqlite
# import random
# import base64
# import simplejson as json


# class Book:
#     id: str
#     title: str
#     author: str
#     publisher: str
#     original_title: str
#     translator: str
#     pub_year: str
#     pages: int
#     price: int
#     currency_unit: str
#     binding: str
#     isbn: str
#     author_intro: str
#     book_intro: str
#     content: str
#     tags: [str]
#     pictures: [bytes]

#     def __init__(self):
#         self.tags = []
#         self.pictures = []


# class BookDB:
#     def __init__(self, large: bool = False):
#         parent_path = os.path.dirname(os.path.dirname(__file__))
#         self.db_s = os.path.join(parent_path, "data/book.db")
#         self.db_l = os.path.join(parent_path, "data/book_lx.db")
#         if large:
#             self.book_db = self.db_l
#         else:
#             self.book_db = self.db_s

#     def get_book_count(self):
#         conn = sqlite.connect(self.book_db)
#         cursor = conn.execute("SELECT count(id) FROM book")
#         row = cursor.fetchone()
#         return row[0]

#     def get_book_info(self, start, size) -> [Book]:
#         books = []
#         conn = sqlite.connect(self.book_db)
#         cursor = conn.execute(
#             "SELECT id, title, author, "
#             "publisher, original_title, "
#             "translator, pub_year, pages, "
#             "price, currency_unit, binding, "
#             "isbn, author_intro, book_intro, "
#             "content, tags, picture FROM book ORDER BY id "
#             "LIMIT ? OFFSET ?",
#             (size, start),
#         )
#         for row in cursor:
#             book = Book()
#             book.id = row[0]
#             book.title = row[1]
#             book.author = row[2]
#             book.publisher = row[3]
#             book.original_title = row[4]
#             book.translator = row[5]
#             book.pub_year = row[6]
#             book.pages = row[7]
#             book.price = row[8]

#             book.currency_unit = row[9]
#             book.binding = row[10]
#             book.isbn = row[11]
#             book.author_intro = row[12]
#             book.book_intro = row[13]
#             book.content = row[14]
#             tags = row[15]

#             picture = row[16]

#             for tag in tags.split("\n"):
#                 if tag.strip() != "":
#                     book.tags.append(tag)
#             for i in range(0, random.randint(0, 9)):
#                 if picture is not None:
#                     encode_str = base64.b64encode(picture).decode("utf-8")
#                     book.pictures.append(encode_str)
#             books.append(book)
#             # print(tags.decode('utf-8'))

#             # print(book.tags, len(book.picture))
#             # print(book)
#             # print(tags)

#         return books

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
                for picture in pictures:
                    encode_str = base64.b64encode(picture.encode()).decode("utf-8")
                    book.pictures.append(encode_str)
            books.append(book)
            print(book)
        return books


# import os
# import pymongo
# from bson.binary import Binary
# import random
# import base64
# from bson import ObjectId


# class Book:
#     def __init__(self):
#         self.tags = []
#         self.pictures = []


# class BookDB:
#     def __init__(self, large: bool = False):
#         #parent_path = os.path.dirname(os.path.dirname(__file__))
#         self.client = pymongo.MongoClient("mongodb://localhost:27017/")
#         self.db = self.client["bookstore"]
#         self.collection = self.db["book"]
#         self.large = large

#     def get_book_count(self):
#         return self.collection.count_documents({})

#     def get_book_info(self, start, size) -> [Book]:
#         books = []
#         cursor = self.collection.find().skip(start).limit(size)
#         for doc in cursor:
#             book = Book()
#             book.id = str(doc["_id"])
#             book.title = doc["title"]
#             book.author = doc["author"]
#             book.publisher = doc["publisher"]
#             book.original_title = doc["original_title"]
#             book.translator = doc["translator"]
#             book.pub_year = doc["pub_year"]
#             book.pages = doc["pages"]
#             book.price = doc["price"]
#             book.currency_unit = doc["currency_unit"]
#             book.binding = doc["binding"]
#             book.isbn = doc["isbn"]
#             book.author_intro = doc["author_intro"]
#             book.book_intro = doc["book_intro"]
#             book.content = doc["content"]
#             book.tags = doc["tags"]
#             book.pictures = doc["pictures"]
#             books.append(book)
#         return books

#     def insert_book(self, book: Book):
#         pictures = []
#         for _ in range(random.randint(0, 9)):
#             encoded_picture = base64.b64encode(pictures).decode("utf-8")
#             pictures.append(encoded_picture)

#         book_dict = {
#             "title": book.title,
#             "author": book.author,
#             "publisher": book.publisher,
#             "original_title": book.original_title,
#             "translator": book.translator,
#             "pub_year": book.pub_year,
#             "pages": book.pages,
#             "price": book.price,
#             "currency_unit": book.currency_unit,
#             "binding": book.binding,
#             "isbn": book.isbn,
#             "author_intro": book.author_intro,
#             "book_intro": book.book_intro,
#             "content": book.content,
#             "tags": book.tags,
#             "pictures": pictures,
#         }

#         result = self.collection.insert_one(book_dict)
#         return str(result.inserted_id)

#     def get_book_by_id(self, book_id):
#         return self.collection.find_one({"_id": ObjectId(book_id)})

#     def update_book(self, book_id, new_book_data):
#         result = self.collection.update_one(
#             {"_id": ObjectId(book_id)},
#             {"$set": new_book_data}
#         )
#         return result.modified_count
