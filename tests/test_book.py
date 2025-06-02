import pytest
from library.book import Book

def test_book_name()->None:
    book = Book("a", "b", 2025)
    assert len(book.name) > 0