import requests
from urllib.parse import urljoin


class Auth:
    def __init__(self, url_prefix):
        self.url_prefix = urljoin(url_prefix, "auth/")

    def login(self, user_id: str, password: str, terminal: str) -> (int, str):
        json = {"user_id": user_id, "password": password, "terminal": terminal}
        url = urljoin(self.url_prefix, "login")
        r = requests.post(url, json=json)
        return r.status_code, r.json().get("token")

    def register(self, user_id: str, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "register")
        r = requests.post(url, json=json)
        return r.status_code

    def password(self, user_id: str, old_password: str, new_password: str) -> int:
        json = {
            "user_id": user_id,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        url = urljoin(self.url_prefix, "password")
        r = requests.post(url, json=json)
        return r.status_code

    def logout(self, user_id: str, token: str) -> int:
        json = {"user_id": user_id}
        headers = {"token": token}
        url = urljoin(self.url_prefix, "logout")
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def unregister(self, user_id: str, password: str) -> int:
        json = {"user_id": user_id, "password": password}
        url = urljoin(self.url_prefix, "unregister")
        r = requests.post(url, json=json)
        return r.status_code


    # 搜索后端
    def search_books_global(self, query: str, start: int, size: int) -> (int, list):
        # params = {"query": query, "start": start, "size": size}
        # url = urljoin(self.url_prefix, "search_books_global")
        # headers = {"token": ""}
        # response = requests.get(url, headers=headers, params=params)
        # if response.status_code == 200:
        #     try:
        #         books = response.json().get("books", [])
        #     except ValueError:  # Includes simplejson.decoder.JSONDecodeError
        #         books = []  # Default to an empty list if there's a JSON decode error
        # else:
        #     books = []  # Default to an empty list if the response isn't successful
        # return response.status_code
        params = {"query": query, "start": start, "size": size}
        url = urljoin(self.url_prefix, "search_books_global")
        headers = {"token": ""}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                books = response.json().get("books", [])
            except ValueError:  # 包括 simplejson.decoder.JSONDecodeError
                books = []  # 如果JSON解析出错，则默认返回空列表
        else:
            books = []  # 如果响应状态码不是200，也返回空列表
        return response.status_code, books  # 确保总是返回一个元组


    def search_books_in_store(self, store_id: str, query: str, start: int, size: int) -> (int, list):
        params = {"store_id": store_id, "query": query, "start": start, "size": size}
        url = urljoin(self.url_prefix, "search_books_in_store")
        headers = {"token": ""}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                books = response.json().get("books", [])
            except ValueError:
               books = []
        else:
            books = []
        return response.status_code, books