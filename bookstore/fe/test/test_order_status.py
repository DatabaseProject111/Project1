import pytest
from fe.access.buyer import Buyer
#from fe.access.seller import Seller
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
#from fe.access.new_seller import register_new_seller
from fe.access.book import Book
import uuid


class TestPayment:
    seller_id: str
    store_id: str
    buyer_id: str
    password: str
    buy_book_info_list: [Book]
    total_price: int
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
        
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        yield
        
        # code, self.order_status = self.buyer.get_order_info(self.order_id)
        # assert code == 200
        
        
    def test_ok(self):
        # 买家充值
        code = self.buyer.add_funds(self.total_price)
        assert code ==200
        # 买家付钱
        code = self.buyer.payment(self.order_id)
        assert code == 200
        # code = self.buyer.order_status(self.order_id)
        # assert code ==200
        code = self.buyer.receive_order(self.order_id)
        assert code ==200
        
        code = self.buyer.order_status(self.order_id)
        assert code ==200
        #assert self.order_status == 'paid'
        # # 卖家发货
        # code = ship_books(self.store_id,self.order_id)
        # assert code ==200
        # self.status=self.buyer.order_status(self.order_id)
        # assert self.status == 'shipped'
        # 买家收货
        
        # self.order_status=self.buyer.order_status(self.order_id)
        # assert self.order_status =='received'


