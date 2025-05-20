import pytest
from shopping_cart.cart import Cart
from shopping_cart.item import Item

# Fixture to create a cart object. this object is available to all test functions thanks to pytest @pytest.fixture
@pytest.fixture
def cart():
   database = "./tests/test_database.json"
   cart = Cart(database)
   cart.empty_cart()
   return cart

def test_total_price_of_items(cart):
    item1 = Item("banana", "fruit", 1.00)
    item2 = Item("apple", "fruit", 2.00)
    item3 = Item("pineapple", "fruit", 1.00)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    cart.add_item_to_cart(item3)
    assert cart.get_total_price_of_items() == 4.00

def test_empty_cart(cart):
    item1 = Item("banana", "fruit", 1.00)
    item2 = Item("apple", "fruit", 2.00)
    item3 = Item("pineapple", "fruit", 1.00)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    cart.add_item_to_cart(item3)
    cart.empty_cart()
    assert len(cart.get_all_items()["Items"].items()) == 0

def test_search_items(cart):
    item1 = Item("banana", "fruit", 1.00)
    cart.add_item_to_cart(item1)
    items_list = cart.search_items("banana")
    assert items_list[0].name == "banana"

def test_get_all_items(cart):
    item1 = Item("banana", "fruit", 1.00)
    item2 = Item("apple", "fruit", 2.00)
    item3 = Item("pineapple", "fruit", 1.00)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    cart.add_item_to_cart(item3)
    retrieved_items = cart.get_all_items()
    names_to_compare = [item1.name, item2.name, item3.name]
    result = [item_data["name"] for item_id, item_data in retrieved_items["Items"].items()]
    assert result == names_to_compare

def test_get_total_item_count(cart):
    item1 = Item("banana", "fruit", 1.00)
    item2 = Item("apple", "fruit", 2.00)
    item3 = Item("pineapple", "fruit", 1.00)
    cart.add_item_to_cart(item1)
    cart.add_item_to_cart(item2)
    cart.add_item_to_cart(item3)
    assert cart.get_total_item_count() == 3

