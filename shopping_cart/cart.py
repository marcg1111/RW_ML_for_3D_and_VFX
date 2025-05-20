import json
from dataclasses import dataclass, field
from shopping_cart.item import Item
from shopping_cart.file_io import Fstream
from shopping_cart.random_number_utils import RandomNumberUtils


@dataclass
class Cart:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomNumberUtils.generate_random_id)

    def get_all_items(self, verbose=0) -> dict:
        """
        Reads and returns all items from the database as hash map.

        Args:
            verbose set to 1 to print the items to the console.

        Returns:
            dict: A hash map containing the items.
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

            try:
                if verbose == 1:
                    Fstream.print_json_structure(data_file)
                    return data_file
                else:
                    return data_file
            except Exception as e:
               raise ValueError("The value of verbose has to be 0 or 1")
                

    def search_items(self, query: str) -> list[Item]:       
        """
        Search for items in the database based on a query.

        Args:
            query (str): The query to search for.
        """
        data = Fstream.load_json_files(self.database_path)
        matching_items = []
        for item_id, item_data in data["Items"].items():
            item = Item(name=item_data["name"], type=item_data["type"], _price=item_data["price"], id=item_id)
            if query.lower() in item.search_string.lower():
                matching_items.append(item)

        if len(matching_items) == 0:
            print("No items found!")

        else:
            for item in matching_items:
                print(f"Found: {item.name} ({item.type}) ${item.price} EUR")                

        return matching_items


    def get_total_item_count(self) -> int:
        """
        Returns the total number of items in the cart.
        """
        data = Fstream.load_json_files(self.database_path)
        return len(data["Items"])

    def add_item_to_cart(self, item: Item):
        """
        Adds an item to the cart and updates the database.json file.
        """
        data = self.get_all_items()

        new_item = {
            "name": item.name,
            "type": item.type,
            "price": item.price,
        }

        data["Items"][item.id] = new_item

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {item.name} to the cart.")


    def remove_item_from_cart(self, query: str = None):
        """
        Removes all instances of an item from the cart based on a query.
        Args:
            query (str): The query to search for.
        """
        data = self.get_all_items()
        items_to_remove = []

        for item_id, item_data in data["Items"].items():
            if query.lower() in item_data["name"].lower() or query.lower() in item_data["type"].lower():
                items_to_remove.append(item_id)

        if not items_to_remove:
            print(f"No items found matching '{query}'!")
            return
        
        for item_id in items_to_remove:
            item_name = data["Items"][item_id]["name"]
            del data["Items"][item_id]
            print(f"Removed {item_name} from the cart.")

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def remove_items_from_cart_by_user_input(self):
        """
        Removes items from the cart based on user input.
        """
        data = self.get_all_items()
        items = []
        i = 1

        for item_id, item_data in data["Items"].items():
            items.append(item_id)
            print(f"{i}: {item_data}")
            i += 1
        try:
            usr_choice = int(input("Select the item to delete by number, example: 0: ")) -1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice > len(items) -1:
            print("Item not found!")
            return

        item_to_delete = items[usr_choice]
        item_name = data["Items"][item_to_delete]["name"]
        del data["Items"][item_to_delete]
        print(f"Removed {item_name} from the cart.")

        with open(self.database_path, "w") as file:
            json.dump(data, file, indent=4)

        if not data["Items"]:
            self.isEmpty = True
            self.isActive = False

    def get_total_price_of_items(self) -> float:
        """
        Returns the total price of all items in the cart.
        """
        data = self.get_all_items()
        total_price = 0

        for item_id, item_data in data["Items"].items():
            total_price += data["Items"][item_id]["price"]

        return total_price

    def empty_cart(self):
        """
        Empties the cart and updates the database.json file.
        """
        data = self.get_all_items()
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

    

