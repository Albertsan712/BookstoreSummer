class Book:
    def __init__(self, title, author, available):
        self.title = title
        self.author = author
        self.available = available

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, book):
        if book.available:
            self.items.append(book)
            print(f"{book.title} added to cart.")
        else:
            print("Sorry, book not available.")

    def display_cart(self):
        print("Shopping Cart:")
        for item in self.items:
            print(f"- {item.title} by {item.author}")

# Sample Book Instances
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", True)
book2 = Book("To Kill a Mockingbird", "Harper Lee", False)

# Initialize Shopping Cart
cart = ShoppingCart()

# Add Books to Cart
cart.add_to_cart(book1)
cart.add_to_cart(book2)

# Display Cart
cart.display_cart()
print("Hello world")