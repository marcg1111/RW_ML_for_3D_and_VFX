import pytest
from shopping_cart.item import Item

def test_item_price()->None:
    item = Item("Car", "vehicle", 80500.90)
    assert item.price >= 0 or item.price == 80500.90

def test_item_name()->None:
    item = Item("a", "b", 10.50)
    assert len(item.name) > 0
