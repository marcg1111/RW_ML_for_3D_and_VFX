import pytest
from library.cart import Cart
from library.book import Book

# Fixture to create a cart object. this object is available to all test functions thanks to pytest @pytest.fixture
@pytest.fixture
def cart():
   database = "./tests/test_database.json"
   cart = Cart(database)
   cart.empty_cart()
   return cart

def test_empty_cart(cart):
    item1 = Book("book_a", "Sci-Fi", 1990)
    item2 = Book("book_b", "Fantasy", 2021)
    item3 = Book("book_c", "Selfe care", 2025)
    cart.add_book_to_cart(item1)
    cart.add_book_to_cart(item2)
    cart.add_book_to_cart(item3)
    cart.empty_cart()
    assert len(cart.get_all_books()["Items"].items()) == 0


def test_search_books(cart):
    item1 = Book("book_a", "Fantasy", 2010)
    cart.add_book_to_cart(item1)
    items_list = cart.search_items("book_a")
    assert items_list[0].name == "book_a"


def test_get_all_books(cart):
    item1 = Book("book_a", "Sci-Fi", 1990)
    item2 = Book("book_b", "Fantasy", 2021)
    item3 = Book("book_c", "Selfe care", 2025)
    cart.add_book_to_cart(item1)
    cart.add_book_to_cart(item2)
    cart.add_book_to_cart(item3)
    retrieved_items = cart.get_all_books()
    names_to_compare = [item1.name, item2.name, item3.name]
    result = [item_data["name"] for item_id, item_data in retrieved_items["Items"].items()]
    assert result == names_to_compare


def test_get_total_item_count(cart):
    item1 = Book("book_a", "Sci-Fi", 1990)
    item2 = Book("book_b", "Fantasy", 2021)
    item3 = Book("book_c", "Selfe care", 2025)
    cart.add_book_to_cart(item1)
    cart.add_book_to_cart(item2)
    cart.add_book_to_cart(item3)
    assert cart.get_total_item_count() == 3