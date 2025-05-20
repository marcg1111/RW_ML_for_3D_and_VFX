import os
from shopping_cart.item import Item
from shopping_cart.cart import Cart


if __name__ == "__main__":

    # Load the database
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(base_dir, "database.json")
    my_cart = Cart(database);

    # search for an item
    print("Searching for an item")
    my_cart.search_items("apple")
    print("___________________")

    #get total item count
    print("Total items in the current cart")
    total_item_count = my_cart.get_total_item_count()
    print(f"Total items: {total_item_count}")
    print("___________________")

    #Create a new item, so it can be added to the cart
    milk = Item("milk", "liquid", 1.25)
    onion = Item("onion", "vegetable", 0.44)
    
    #add the item to the cart
    print("Adding an item to the cart")
    my_cart.add_item_to_cart(milk)
    my_cart.add_item_to_cart(onion)
    print("___________________")

    #get all items in the cart
    print("All items in the cart")
    my_cart.get_all_items(verbose=1)
    print("___________________")

    #remove all items by name or type
    print("Removing all instances of an item:")
    print("______________________")
    my_cart.remove_item_from_cart(milk.name)
    print("\n")

    #remove selected items by user input
    print("Removing selected items by user input:")
    my_cart.remove_items_from_cart_by_user_input()
    print("______________________")

    #print all items in the cart
    print("Printing all items in the cart:")
    my_cart.get_all_items(verbose=1)
    print("______________________")

    #get total price of items in the cart
    print("Total price of items in the cart:")
    total_price = my_cart.get_total_price_of_items()
    print(f"Total price: {total_price} EUR")
