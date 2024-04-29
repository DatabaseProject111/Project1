import pymongo
import uuid
import json
import logging
from be.model import db_conn
from be.model import error
import pymongo.errors
from datetime import datetime, timedelta
import pytz
class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            for book_id, count in id_and_count:
                store_col = self.db["store"]
                book = store_col.find_one({"store_id": store_id, "book_id": book_id})
                if book is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                stock_level = book.get("stock_level")
                book_info = book.get("book_info")
                price = book_info.get("price")

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                result = store_col.update_one(
                    {"store_id": store_id, "book_id": book_id, "stock_level": {"$gte": count}},
                    {"$inc": {"stock_level": -count}}
                )
                if result.modified_count == 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                order_detail_col = self.db["new_order_detail"]
                order_detail_col.insert_one({
                    "order_id": uid,
                    "book_id": book_id,
                    "count": count,
                    "price": price
                })

            order_col = self.db["new_order"]
            # 下午：添加订单状态-代付款
            # order_col.insert_one({
            #     "order_id": uid,
            #     "store_id": store_id,
            #     "user_id": user_id
            # })

            # 默认订单状态为待付款
            order_status = "unpaid"
            order_col.insert_one({
                "order_id": uid,
                "store_id": store_id,
                "user_id": user_id,
                "status": order_status,  # 添加订单状态
                "order_date": datetime.now(),  # 添加订单创建时间
                # "expire_time": datetime.now(pytz.timezone.utc) + timedelta(minutes=30)  # 添加订单超时时间
            })
            order_id = uid
        except pymongo.errors.PyMongoError as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        # except BaseException as e:
        #     logging.info("530, {}".format(str(e)))
        #     return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            order_col = self.db["new_order"]
            order_info = order_col.find_one({"order_id": order_id})
            if order_info is None:
                return error.error_invalid_order_id(order_id)
            #返回518

            order_id = order_info.get("order_id")
            buyer_id = order_info.get("user_id")
            store_id = order_info.get("store_id")

            if buyer_id != user_id:
                return error.error_authorization_fail()
            #返回401

            user_col = self.db["user"]
            user_info = user_col.find_one({"user_id": buyer_id})
            if user_info is None:
                return error.error_non_exist_user_id(buyer_id)
            #返回511
            balance = user_info.get("balance")
            if password != user_info.get("password"):
                return error.error_authorization_fail()
            #返回401
            
            user_store_col = self.db["user_store"]
            seller_info = user_store_col.find_one({"store_id": store_id})
            if seller_info is None:
                return error.error_non_exist_store_id(store_id)
            #返回513
            seller_id = seller_info.get("user_id")
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)
            #返回511  
            order_detail_col = self.db["new_order_detail"]
            order_details = order_detail_col.find({"order_id": order_id})
            total_price = 0
            for detail in order_details:
                count = detail.get("count")
                price = detail.get("price")
                total_price = total_price + price * count

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)
            #若余额不足，应该返回519

            result = user_col.update_one(
                {"user_id": buyer_id, "balance": {"$gte": total_price}},
                {"$inc": {"balance": -total_price}}
            )
            if result.modified_count == 0:
                return error.error_not_sufficient_funds(order_id)
            #若余额不足，应该返回519
            result = user_col.update_one(
                {"user_id": seller_info.get("user_id")},
                {"$inc": {"balance": total_price}}
            )
            if result.modified_count == 0:
                return error.error_non_exist_user_id(seller_id)
            #返回511
            #下午：添加订单状态-已付款
            result = order_col.update_one(
                {"order_id": order_id},
                {"$set": {"status": "paid"}}
            )
            if result.modified_count == 0:
                return error.error_invalid_order_id(order_id)
            #下午：感觉还不能删除订单，需要后续发货
            # result = order_col.delete_one({"order_id": order_id})
            # if result.deleted_count == 0:
            #     return error.error_invalid_order_id(order_id)
            # result = order_detail_col.delete_many({"order_id": order_id})
            # if result.deleted_count == 0:
            #     return error.error_invalid_order_id(order_id)

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            user_col = self.db["user"]
            user_info = user_col.find_one({"user_id": user_id})
            if user_info is None:
                return error.error_authorization_fail()

            if user_info.get("password") != password:
                return error.error_authorization_fail()

            result = user_col.update_one(
                {"user_id": user_id},
                {"$inc": {"balance": add_value}}
            )
            if result.modified_count == 0:
                return error.error_non_exist_user_id(user_id)
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))

        return 200, "ok"
    
    # 添加收货功能
    def receive_order(self, user_id: str, order_id: str) -> (int, str):
        try:
            # 检查订单是否存在
            order_col = self.db["new_order"]
            order_info = order_col.find_one({"order_id": order_id})
            if order_info is None:
                return error.error_invalid_order_id(order_id)

            # 检查用户是否为订单所有者
            buyer_id = order_info.get("user_id")
            if buyer_id != user_id:
                return error.error_authorization_fail()

            # 更新订单状态为已收货
            order_col.update_one(
                {"order_id": order_id},
                {"$set": {"status": "received"}}
            )
            # if result.modified_count == 0:
            #     return error.error_invalid_order_id(order_id)

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"
    
    # 添加定时任务来取消超时订单
    def cancel_timeout_orders(self):
        try:
            # 获取当前时间
            current_time = datetime.now()

            # 获取超时时间阈值为15分钟
            timeout_threshold = timedelta(minutes=15)

            # 获取所有未付款的订单
            order_col = self.db["new_order"]
            unpaid_orders = order_col.find({"status": "unpaid"})

            for order in unpaid_orders:
                # 获取订单创建时间
                order_date = order.get("order_date")

                # 计算订单创建时间到当前时间的时间差
                time_diff = current_time - order_date

                # 如果时间差超过超时时间阈值，则取消订单
                if time_diff >= timeout_threshold:
                    order_id = order.get("order_id")
                    # 执行取消订单操作
                    self.cancel_order(order_id)
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"
    
    def cancel_order(self, order_id: str) -> (int, str):
        try:
            # 检查订单是否存在
            order_col = self.db["new_order"]
            order_info = order_col.find_one({"order_id": order_id})
            if order_info is None:
                return error.error_invalid_order_id(order_id)

            # 将订单状态设置为已取消
            result = order_col.update_one(
                {"order_id": order_id},
                {"$set": {"status": "cancelled"}}
            )

            # 返还订单中的书籍数量到商店库存
            order_detail_col = self.db["new_order_detail"]
            order_details = order_detail_col.find({"order_id": order_id})
            store_col = self.db["store"]
            for detail in order_details:
                book_id = detail.get("book_id")
                count = detail.get("count")
                store_col.update_one(
                    {"store_id": order_info.get("store_id"), "book_id": book_id},
                    {"$inc": {"stock_level": count}}
                )

            # 删除订单详情记录
            result = order_detail_col.delete_many({"order_id": order_id})

            # 删除订单记录
            result = order_col.delete_one({"order_id": order_id})

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"
    
    # 添加订单状态：
    def order_status(self, order_id: str) -> dict:
        try:
            # 检查订单是否存在
            order_col = self.db["new_order"]
            order_info = order_col.find_one({"order_id": order_id})
            if order_info is None:
                return error.error_invalid_order_id(order_id)

        # 获取订单状态
            order_status = order_info.get("status")

        except pymongo.errors.PyMongoError as e:
            return {"status_code": 528, "message": str(e)}

        return 200, "ok"
    
    
    #添加订单查询功能
    def query_order(self, order_id: str) -> dict:
        try:
            # 检查订单是否存在
            order_col = self.db["new_order"]
            order_info = order_col.find_one({"order_id": order_id})
            if order_info is None:
                return error.error_invalid_order_id(order_id)

            # 获取订单详情
            order_detail_col = self.db["new_order_detail"]
            order_details = order_detail_col.find({"order_id": order_id})

            # 构建订单详情字典列表
            details_list = []
            for detail in order_details:
                book_id = detail.get("book_id")
                count = detail.get("count")
                details_list.append({"book_id": book_id, "count": count})

         # 构建订单信息字典
            order_info_dict = {
                "order_id": order_info.get("order_id"),
                "user_id": order_info.get("user_id"),
                "store_id": order_info.get("store_id"),
                "status": order_info.get("status"),
                "order_date": order_info.get("order_date"),
                "order_details": details_list
            }
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        return 200, "ok"
        # except pymongo.errors.PyMongoError as e:
        #     return {"status_code": 528, "message": str(e)}

        # return {"status_code": 200, "order_info": order_info_dict}
        #添加订单状态查询功能
    # def get_order_info(self, order_id: str) -> dict:
    #     try:
    #         # 检查订单是否存在
    #         order_col = self.db["new_order"]
    #         order_info = order_col.find_one({"order_id": order_id})
    #         if order_info is None:
    #             return error.error_invalid_order_id(order_id)
    #     except pymongo.errors.PyMongoError as e:
    #         logging.info("528, {}".format(str(e)))
    #         return 528, "{}".format(str(e)), ""
    #     # except BaseException as e:
    #     #     logging.info("530, {}".format(str(e)))
    #     #     return 530, "{}".format(str(e)), ""

    #     return 200, "ok", order_status

    
    