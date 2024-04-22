# from be.model import store


# class DBConn:
#     def __init__(self):
#         self.conn = store.get_db_conn()

#     def user_id_exist(self, user_id):
#         cursor = self.conn.execute(
#             "SELECT user_id FROM user WHERE user_id = ?;", (user_id,)
#         )
#         row = cursor.fetchone()
#         if row is None:
#             return False
#         else:
#             return True

#     def book_id_exist(self, store_id, book_id):
#         cursor = self.conn.execute(
#             "SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;",
#             (store_id, book_id),
#         )
#         row = cursor.fetchone()
#         if row is None:
#             return False
#         else:
#             return True

#     def store_id_exist(self, store_id):
#         cursor = self.conn.execute(
#             "SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,)
#         )
#         row = cursor.fetchone()
#         if row is None:
#             return False
#         else:
#             return True
from be.model import store

class DBConn:
    def __init__(self):
        # 连接本地 MongoDB，默认端口为 27017
        self.client = store.get_db_conn()
        self.db = self.client["bookstore"] 
        self.user_collection=self.db["user"]

    def user_id_exist(self, user_id):
        # 获取名为 user 的集合（相当于 SQL 中的表）
        user_collection = self.db['user']
        # 在 user 集合中查找是否存在指定 user_id
        return user_collection.find_one({'user_id': user_id}) is not None

    def book_id_exist(self, store_id, book_id):
        # 获取名为 store 的集合
        store_collection = self.db['store']
        # 在 store 集合中查找是否存在指定 store_id 和 book_id 的记录
        return store_collection.find_one({'store_id': store_id, 'book_id': book_id}) is not None

    def store_id_exist(self, store_id):
        # 获取名为 user_store 的集合
        user_store_collection = self.db['user_store']
        # 在 user_store 集合中查找是否存在指定 store_id
        return user_store_collection.find_one({'store_id': store_id}) is not None
