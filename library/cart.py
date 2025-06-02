import json
from dataclasses import dataclass, field
from library.book import Book
from library.file_io import Fstream
from library.random_number_utils import RandomNumberUtils

@dataclass
class Cart:
    database_path:  str
    isEmpty:        bool = True
    isActive:       bool = False
    id:             str = field(init=False, default_factory=RandomNumberUtils.generate_random_id)

    def get_all_books(self, verbose=0) -> dict:
        """
        Reads and returns all items from the database as hash map.

        Args:
            verbose set to 1 to print the items to the console.

        Returns:
            dict: A hash map containing the items.
        """
        data_file = Fstream.load_json_file(self.database_path)

        if "Items" in data_file and len(data_file["Items"]) > 0:
            self.isEmpty = False
            self.isActive = True

        if verbose not in (0, 1):
            raise ValueError("The value of verbose must be 0 or 1")

        if verbose == 1:
            Fstream.print_json_structure(data_file)

        return data_file
    
            
    def search_items(self, query: str) -> list[Book]:       
        """
        Search for items in the database based on a query.

        Args:
            query (str): The query to search for.
        """
        data = Fstream.load_json_file(self.database_path)
        matching_books = []

        for book_id, book_data in data["Items"].items():
            book = Book(name=book_data["name"], genre=book_data["genre"], year=book_data["year"], id=book_id)
            if query.lower() in book.search_string.lower():
                matching_books.append(book)

        if not matching_books:
            print("No items found!")

        else:
            for book in matching_books:
                print(f"Found: {book.name} ({book.genre}) - {book.year}")                

        return matching_books
    

    def get_total_item_count(self) -> int:
        """
        Returns the total number of items in the cart.
        """
        data = Fstream.load_json_file(self.database_path)
        return len(data["Items"])
    

    def add_book_to_cart(self, book: Book):
        """
        Adds a book to the cart and updates the database.json file.
        """
        data = self.get_all_books()

        new_book = {
            "name": book.name,
            "genre": book.genre,
            "year": book.year,
        }

        data["Items"][book.id] = new_book

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {book.name} to the cart.")


    def remove_book_from_cart(self, query: str = None):
        """
        Removes all instances of an item from the cart based on a query.
        Args:
            query (str): The query to search for.
        """
        data = self.get_all_books()
        books_to_remove = []

        for book_id, book_data in data["Items"].items():
            if query.lower() in book_data["name"].lower() or query.lower() in book_data["genre"].lower():
                books_to_remove.append(book_id)

        if not books_to_remove:
            print(f"No books found matching '{query}'!")
            return
        
        for book_id in books_to_remove:
            book_name = data["Items"][book_id]["name"]
            del data["Items"][book_id]
            print(f"Removed {book_name} from the cart.")

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False


    def remove_books_from_cart_by_user_input(self):
        """
        Removes items from the cart based on user input.

        """
        data = self.get_all_books()
        books = []
        i = 1

        for item_id, item_data in data["Items"].items():
            books.append(item_id)
            print(f"{i}: {item_data}")
            i += 1
        try:
            usr_choice = int(input("Select the book to delete by number, example: 2: ")) -1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice > len(books) -1:
            print("Book not found!")
            return

        item_to_delete = books[usr_choice]
        item_name = data["Items"][item_to_delete]["name"]
        del data["Items"][item_to_delete]
        print(f"Removed {item_name} from the cart.")

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False


    def empty_cart(self):
        """
        Empties the cart and updates the database.json file.
        """
        data = self.get_all_books()
        if len(data["Items"].items()) > 0:
            data = {"Items": {}}

            with open(self.database_path, "w") as file:
                json.dump(data, file, indent=4)

            if not data["Items"]:
                self.isEmpty = True
                self.isActive = False

            print("Cart is now empty!")
        else:
            print("Cart is already empty!")