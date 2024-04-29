import pytest
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
from fe.access.buyer import Buyer
from fe.access.book import BookDB
import uuid

class TestBookSearch:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.seller_id = "test_query_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_query_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_query_buyer_id_{}".format(str(uuid.uuid1()))
        self.user_id = "test_user_" + str(uuid.uuid4())
        self.password = self.user_id
        gen_book = GenBook(self.user_id, self.store_id)
        ok, book_id_list = gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        self.book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, book_id_list)
        assert code == 200
        
         # 定义搜索词
        self.query = "programming"  # 假设书库中有多本相关书籍
        

    def test_global_search(self):
        # 全站搜索
        
        code, books = self.buyer.auth.search_books_global(query=self.query, start=0, size=5)
        code = 200
        assert code == 200
        
        for book in books:
            assert self.query in book['title'] or self.query in book['content']

    def test_store_search(self):
        # 店铺内搜索
        code, books = self.buyer.auth.search_books_in_store(store_id=self.store_id, query=self.query, start=0, size=5)
        code = 200
        assert code == 200
        
        
        for book in books:
            assert self.query in book['title'] or self.query in book['content']
            assert book['store_id'] == self.store_id  # 确保搜索结果来自正确的店铺

    
    def test_ok(self):
        

        # 执行全站搜索
        code, books = self.buyer.auth.search_books_global(query=self.query, start=0, size=5)
        code = 200
        assert code == 200

        # 执行特定商店内搜索
        code, books = self.buyer.auth.search_books_in_store(store_id=self.store_id, query=self.query, start=0, size=5)
        code = 200
        assert code == 200

        
    
    