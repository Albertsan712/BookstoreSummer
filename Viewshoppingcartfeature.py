class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, title, author, price, quantity):
        self.items.append({"title": title, "author": author, "price": price, "quantity": quantity})

    def calculate_total_price(self):
        total_price = sum(item["price"] * item["quantity"] for item in self.items)
        return total_price

class CartPage:
    def display_items(self, items):
        for item in items:
            print(f"Title: {item['title']}, Author: {item['author']}, Price: {item['price']}, Quantity: {item['quantity']}")

    def display_total_price(self, total_price):
        print(f"Total Price: {total_price}")

# Test Cases
def test_view_cart_with_items():
    cart = ShoppingCart()
    cart.add_item("Book 1", "Author A", 20, 2)
    cart.add_item("Book 2", "Author B", 15, 1)

    cart_page = CartPage()
    cart_page.display_items(cart.items)
    total_price = cart.calculate_total_price()
    cart_page.display_total_price(total_price)

def test_view_empty_cart():
    cart = ShoppingCart()

    cart_page = CartPage()
    cart_page.display_items(cart.items)
    total_price = cart.calculate_total_price()
    cart_page.display_total_price(total_price)

# Run Test Cases
test_view_cart_with_items()
test_view_empty_cart()
