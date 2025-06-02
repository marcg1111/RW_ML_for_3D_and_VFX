import os
from library.book import Book
from library.cart import Cart

if __name__ == "__main__":

    # Load the database
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(base_dir, "database.json")
    my_cart = Cart(database)

    # search for an item
    print("Searching for an book")
    my_cart.search_items("book_a")
    print("___________________")

    #get total item count
    print("Total Books in the current cart")
    total_book_count = my_cart.get_total_item_count()
    print(f"Total books: {total_book_count}")
    print("___________________")

    #Create a new book, so it can be added to the cart
    book_X = Book("book_X", "Humor", 2001)
    book_Y = Book("book_Y", "Fantasy", 2012)


    #add the books to the cart
    print("Adding books to the cart")
    my_cart.add_book_to_cart(book_X)
    my_cart.add_book_to_cart(book_Y)
    print("___________________")


    #get all books in the cart
    print("All books in the cart")
    my_cart.get_all_books(verbose=1)
    print("___________________")

    #remove all books by name or genre
    print("Removing all instances of a book:")
    print("______________________")
    my_cart.remove_book_from_cart(book_X.name)
    print("\n")

    #remove selected books by user input
    print("Removing selected books by user input:")
    my_cart.remove_books_from_cart_by_user_input()
    print("______________________")

    #print all books in the cart
    print("Printing all books in the cart:")
    my_cart.get_all_books(verbose=1)
    print("______________________")
