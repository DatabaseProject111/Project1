# import pytest
# from fe.access.buyer import Buyer
# from fe.test.gen_book_data import GenBook
# from fe.access.new_buyer import register_new_buyer
# from fe.access.book import Book
# import uuid
# from freezegun import freeze_time


# class TestCancelTimeoutOrders:
#     seller_id: str
#     store_id: str
#     buyer_id: str
#     password: str
#     buy_book_info_list: [Book]
#     total_price: int
#     order_id: str
#     buyer: Buyer

#     @pytest.fixture(autouse=True)
#     def pre_run_initialization(self):
#         self.seller_id = "test_cancel_timeout_orders_seller_id_{}".format(str(uuid.uuid1()))
#         self.store_id = "test_cancel_timeout_orders_store_id_{}".format(str(uuid.uuid1()))
#         self.buyer_id = "test_cancel_timeout_orders_buyer_id_{}".format(str(uuid.uuid1()))
#         self.password = self.seller_id
#         gen_book = GenBook(self.seller_id, self.store_id)
#         ok, buy_book_id_list = gen_book.gen(
#             non_exist_book_id=False, low_stock_level=False, max_book_count=5
#         )
#         self.buy_book_info_list = gen_book.buy_book_info_list
#         assert ok
#         b = register_new_buyer(self.buyer_id, self.password)
#         self.buyer = b
#         with freeze_time("2024-04-23 00:00:00"):
#             code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
#         print(f"Actual status code: {code}")  # Add this line to print actual status code
#         assert code == 200

#     def test_non_timeout(self):
#         try:
#             code, message = self.buyer.query_order()
#             assert code == 200
#         except TypeError as e:
#             pytest.fail(f"Failed to cancel timeout orders: {e}")
#         except Exception as e:
#             pytest.fail(f"Failed to cancel timeout orders: {e}")
import pytest
from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid

class TestQueryOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
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

    def test_ok(self):
        # Test querying a successfully created order
        code = self.buyer.query_order(self.order_id)
        assert code == 200

    def test_query_nonexistent_order(self):
        # Generate a random UUID for a non-existent order and try querying it
        nonexistent_order_id = str(uuid.uuid1())
        code = self.buyer.query_order(nonexistent_order_id)
        assert code != 200  
# Note: This assumes you have methods like `register_new_buyer`, `new_order`, and `query_order` implemented correctly. If not, you might need to implement these methods or use mocks/stubs for them in your tests.
