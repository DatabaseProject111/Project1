import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Buyer:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = urljoin(url_prefix, "buyer/")
        self.user_id = user_id
        self.password = password
        self.token = ""
        self.terminal = "my terminal"
        self.auth = Auth(url_prefix)
        code, self.token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

    def new_order(self, store_id: str, book_id_and_count: [(str, int)]) -> (int, str):
        books = []
        for id_count_pair in book_id_and_count:
            books.append({"id": id_count_pair[0], "count": id_count_pair[1]})
        json = {"user_id": self.user_id, "store_id": store_id, "books": books}
        # print(simplejson.dumps(json))
        url = urljoin(self.url_prefix, "new_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        return r.status_code, response_json.get("order_id")

    def payment(self, order_id: str):
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "order_id": order_id,
        }
        url = urljoin(self.url_prefix, "payment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def add_funds(self, add_value: str) -> int:
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "add_value": add_value,
        }
        url = urljoin(self.url_prefix, "add_funds")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
    
    #添加收货功能
    def receive_order(self, order_id: str) -> (int, str):
        json = {"user_id": self.user_id, "order_id": order_id}
        url = urljoin(self.url_prefix, "receive_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
    
    # 添加自动取消订单功能
    def cancel_timeout_orders(self):
        url = urljoin(self.url_prefix, "cancel_timeout_orders")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers)
        return r.status_code

    # 添加取消订单功能
    def cancel_order(self, order_id: str) -> (int, str):
        json = {"order_id": order_id}
        url = urljoin(self.url_prefix, "cancel_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
    
    # # P改的：通常情况下，订单状态查询和订单状态功能不需要用户的密码。这些功能仅涉及与订单相关的操作，而不涉及用户的身份验证或安全敏感信息。因此，可以在这两个方法中省略密码参数。
    # 添加订单状态功能
    
    def order_status(self, order_id: str) -> (int, str):
        # params = {"user_id": self.user_id, "order_id": order_id}
        # url = urljoin(self.url_prefix, "order_status")
        # headers = {"token": self.token}
        # # 确保使用POST方法
        # r = requests.post(url, json=params, headers=headers)
        # return r.status_code
        json = {"order_id": order_id}
        url = urljoin(self.url_prefix, "order_status")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        return r.status_code

    # # 添加订单查询功能
    # def get_order_info(self, order_id: str) -> dict:
    #     params = {"user_id": self.user_id, "order_id": order_id}
    #     url = urljoin(self.url_prefix, "query_order")
    #     headers = {"token": self.token}
    #     r = requests.get(url, headers=headers, params=params)
    #     return r.json()
    #用于订单查询的超时
    def query_order(self, order_id: str) -> (int, str):
        # url = urljoin(self.url_prefix, "query_order")
        # headers = {"token": self.token}
        # r = requests.post(url, headers=headers)
        # return r.status_code
        json = {"order_id": order_id}
        url = urljoin(self.url_prefix, "query_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
