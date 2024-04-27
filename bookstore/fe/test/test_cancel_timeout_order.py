import pytest
from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from freezegun import freeze_time
import uuid

class TestCancelTimeoutOrders:
    seller_id: str
    store_id: str
    buyer_id: str
    password: str
    buy_book_info_list: [Book]
    order_id: str
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_cancel_timeout_orders_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_cancel_timeout_orders_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_cancel_timeout_orders_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        with freeze_time("2024-04-23 00:00:00"):
            code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        yield

    # @freeze_time("2024-04-23 00:00:00")  # 模拟当前时间为订单创建时间
    def test_cancel_timeout_orders_ok(self):
        # 模拟订单超时，假设15分钟后订单自动取消
        with freeze_time("2024-04-23 00:20:00"):  # 模拟15分钟后的时间
            code = self.buyer.cancel_timeout_orders()
        assert code == 200

    def test_non_timeout(self):
        # 模拟订单未超时，假设10分钟后
        with freeze_time("2024-04-23 00:10:00"):  # 模拟10分钟后的时间
            code = self.buyer.cancel_timeout_orders()
        assert code == 200

    def test_cancel_order_invalid_order_id(self):
        # 使用一个不存在的订单ID
        invalid_order_id = "invalid_order_id"
        code = self.buyer.cancel_order(invalid_order_id)
        assert code != 200

    def test_repeat_cancelled(self):
        # 模拟已经取消的订单
        code = self.buyer.cancel_order(self.order_id)
        assert code == 200
        # 再次取消已经取消的订单
        code= self.buyer.cancel_order(self.order_id)
        assert code != 200
