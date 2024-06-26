# import logging
# import os
# import sqlite3 as sqlite
# import threading


# class Store:
#     database: str

#     def __init__(self, db_path):
#         self.database = os.path.join(db_path, "be.db")
#         self.init_tables()

#     def init_tables(self):
#         try:
#             conn = self.get_db_conn()
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user ("
#                 "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
#                 "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
#             )

#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user_store("
#                 "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
#             )

#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS store( "
#                 "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
#                 " PRIMARY KEY(store_id, book_id))"
#             )

#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order( "
#                 "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
#             )

#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order_detail( "
#                 "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
#                 "PRIMARY KEY(order_id, book_id))"
#             )

#             conn.commit()
#         except sqlite.Error as e:
#             logging.error(e)
#             conn.rollback()

#     def get_db_conn(self) -> sqlite.Connection:
#         return sqlite.connect(self.database)


# database_instance: Store = None
# # global variable for database sync
# init_completed_event = threading.Event()


# def init_database(db_path):
#     global database_instance
#     database_instance = Store(db_path)


# def get_db_conn():
#     global database_instance
#     return database_instance.get_db_conn()

import pymongo
import logging
import threading

import pymongo.errors


class Store:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bookstore"]
        self.init_tables()

    def init_tables(self):
        try:
            user_col = self.db["user"]
            user_col.create_index([("user_id", pymongo.ASCENDING)], unique=True)

            user_store_col = self.db["user_store"]
            user_store_col.create_index([("user_id", pymongo.ASCENDING), ("store_id", pymongo.ASCENDING)], unique=True)

            store_col = self.db["store"]
            store_col.create_index([("store_id", pymongo.ASCENDING), ("book_id", pymongo.ASCENDING)], unique=True)

            new_order_col = self.db["new_order"]
            new_order_col.create_index([("order_id", pymongo.ASCENDING)], unique=True)

            new_order_detail_col = self.db["new_order_detail"]
            new_order_detail_col.create_index([("order_id", pymongo.ASCENDING), ("book_id", pymongo.ASCENDING)], unique=True)

        except pymongo.errors.PyMongoError as e:
            logging.error(e)

    def get_db_conn(self):
        return self.client

database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database():
    global database_instance
    database_instance = Store()
    database_instance.init_tables()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
