from flask import Flask, jsonify, request

app = Flask(__name__)

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
            for item in self.items:
                if item.title == book.title:
                    item.available = book.available
                    print(f"Quantity of {book.title} updated in cart.")
                    break
            else:
                self.items.append(book)
                print(f"{book.title} added to cart.")
        else:
            print("Sorry, book not available.")

    def remove_from_cart(self, title):
        for item in self.items:
            if item.title == title:
                self.items.remove(item)
                print(f"{title} removed from cart.")
                break
        else:
            print(f"{title} not found in cart.")

    def display_cart(self):
        print("Shopping Cart:")
        for item in self.items:
            print(f"- {item.title} by {item.author}")

cart = ShoppingCart()

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'GET':
        return jsonify([{"title": item.title, "author": item.author} for item in cart.items])
    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(data['title'], data['author'], data['available'])
        cart.add_to_cart(new_book)
        return jsonify({"message": "Book added to cart."})

@app.route('/cart/<title>', methods=['PUT', 'DELETE'])
def update_cart(title):
    if request.method == 'PUT':
        data = request.get_json()
        for item in cart.items:
            if item.title == title:
                item.available = data['available']
                return jsonify({"message": f"Quantity of {title} updated in cart."})
        return jsonify({"message": f"{title} not found in cart."})
    elif request.method == 'DELETE':
        cart.remove_from_cart(title)
        return jsonify({"message": f"{title} removed from cart."})

if __name__ == '__main__':
    app.run(debug=True)
