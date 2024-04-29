

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