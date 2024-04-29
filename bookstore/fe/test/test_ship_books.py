import pytest
from fe import conf
from fe.access.new_seller import register_new_seller
from fe.access import book
import uuid

class TestShipBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_ship_books_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_ship_books_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        self.seller = register_new_seller(self.user_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB(conf.Use_Large_DB)
        self.books = book_db.get_book_info(0, 5)
        for bk in self.books:
            code = self.seller.add_book(self.store_id, 0, bk)
            assert code == 200
        for bk in self.books:
            book_id = bk.id
            code = self.seller.add_stock_level(self.user_id, self.store_id, book_id, 10)
            assert code == 200
        yield

    def test_error_user_id(self):
        for b in self.books:
            book_id = b.id
            code = self.seller.ship_books(
                self.user_id + "_x", self.store_id, book_id, 5
            )
            assert code != 200

    def test_error_store_id(self):
        for b in self.books:
            book_id = b.id
            code = self.seller.ship_books(
                self.user_id, self.store_id + "_x", book_id, 5
            )
            assert code != 200

    def test_error_book_id(self):
        for b in self.books:
            book_id = b.id
            code = self.seller.ship_books(
                self.user_id, self.store_id, book_id + "_x", 5
            )
            assert code != 200

    def test_ok(self):
        for b in self.books:
            book_id = b.id
            code = self.seller.ship_books(self.user_id, self.store_id, book_id, 5)
            assert code == 200