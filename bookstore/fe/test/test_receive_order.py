import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid

class TestReceiveOrder:
    seller_id: str
    store_id: str
    buyer_id: str
    password: str
    buy_book_info_list: [Book]
    order_id: str
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_receive_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_receive_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_receive_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield

    def test_receive_order_ok(self):
        code = self.buyer.receive_order(self.order_id)
        assert code == 200

    def test_receive_order_invalid_order_id(self):
        # 使用一个不存在的订单ID
        self.order_id = self.order_id + "_x"
        code = self.buyer.receive_order(self.order_id)
        assert code != 200

    def test_receive_order_authorization_error(self):
        # 使用不匹配的用户ID尝试接收订单
        self.buyer.user_id = self.buyer.user_id + "_x"
        code = self.buyer.receive_order(self.order_id)
        assert code != 200