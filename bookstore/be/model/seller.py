# import sqlite3 as sqlite
# from be.model import error
# from be.model import db_conn


# class Seller(db_conn.DBConn):
#     def __init__(self):
#         db_conn.DBConn.__init__(self)

#     def add_book(
#         self,
#         user_id: str,
#         store_id: str,
#         book_id: str,
#         book_json_str: str,
#         stock_level: int,
#     ):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if self.book_id_exist(store_id, book_id):
#                 return error.error_exist_book_id(book_id)

#             self.conn.execute(
#                 "INSERT into store(store_id, book_id, book_info, stock_level)"
#                 "VALUES (?, ?, ?, ?)",
#                 (store_id, book_id, book_json_str, stock_level),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"

#     def add_stock_level(
#         self, user_id: str, store_id: str, book_id: str, add_stock_level: int
#     ):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if not self.book_id_exist(store_id, book_id):
#                 return error.error_non_exist_book_id(book_id)

#             self.conn.execute(
#                 "UPDATE store SET stock_level = stock_level + ? "
#                 "WHERE store_id = ? AND book_id = ?",
#                 (add_stock_level, store_id, book_id),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"

#     def create_store(self, user_id: str, store_id: str) -> (int, str):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if self.store_id_exist(store_id):
#                 return error.error_exist_store_id(store_id)
#             self.conn.execute(
#                 "INSERT into user_store(store_id, user_id)" "VALUES (?, ?)",
#                 (store_id, user_id),
#             )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
import pymongo
import json
from be.model import error
from be.model import db_conn
import pymongo.errors
class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            store_col = self.db["store"]
            store_col.insert_one({
                "store_id": store_id,
                "book_id": book_id,
                "book_info": json.loads(book_json_str),
                "stock_level": stock_level
            })
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            store_col = self.db["store"]
            store_info = store_col.find_one({"store_id": store_id, "book_id": book_id})
            if store_info is None:
                return error.error_non_exist_book_id(book_id)

            new_stock_level = store_info.get("stock_level", 0) + add_stock_level
            store_col.update_one(
                {"store_id": store_id, "book_id": book_id},
                {"$set": {"stock_level": new_stock_level}}
            )
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            user_store_col = self.db["user_store"]
            user_store_col.insert_one({
                "store_id": store_id,
                "user_id": user_id
            })
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        return 200, "ok"
