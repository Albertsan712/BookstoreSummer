from flask import Flask, jsonify, request

app = Flask(__name__)

class Book:
    def __init__(self, book_id, title, author, price, available, quantity=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.available = available
        self.quantity = quantity

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount_code = None

    def add_to_cart(self, book):
        if book.available:
            for item in self.items:
                if item.book_id == book.book_id:
                    item.quantity += book.quantity
                    print(f"Quantity of {book.title} updated in cart.")
                    break
            else:
                self.items.append(book)
                print(f"{book.title} added to cart.")
        else:
            print("Sorry, book not available.")

    def remove_from_cart(self, book_id, remove_quantity):
        for item in self.items:
            if item.book_id == book_id:
                if item.quantity > remove_quantity:
                    item.quantity -= remove_quantity
                    print(f"Quantity of {item.title} reduced by {remove_quantity} in cart.")
                elif item.quantity == remove_quantity:
                    self.items.remove(item)
                    print(f"{item.title} removed from cart.")
                else:
                    print(f"Cannot remove {remove_quantity} copies of {item.title} from cart. Only {item.quantity} available.")
                break
        else:
            print(f"Book ID {book_id} not found in cart.")

    def display_cart(self):
        print("Shopping Cart:")
        for item in self.items:
            print(f"- {item.title} by {item.author} (${item.price} for {item.quantity} items)")

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        if self.discount_code:
            total -= total * self.discount_code.discount_percentage
        return total

class DiscountCode:
    def __init__(self, code, discount_percentage):
        self.code = code
        self.discount_percentage = discount_percentage

discount_codes = [
    DiscountCode("SUMMER2021", 0.1),
    DiscountCode("WINTER2021", 0.15),
    DiscountCode("SPRING2022", 0.2)
]

carts = {}

@app.route('/cart/<username>', methods=['GET', 'POST'])
def shopping_cart(username):
    if username not in carts:
        carts[username] = ShoppingCart()

    if request.method == 'GET':
        return jsonify([{"book_id": item.book_id, "title": item.title, "author": item.author, "price": item.price, "quantity": item.quantity} for item in carts[username].items])
    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(data['book_id'], data['title'], data['author'], data['price'], data['available'], data.get('quantity', 1))
        carts[username].add_to_cart(new_book)
        return jsonify({"message": "Book added to cart."})

@app.route('/cart/<username>/<book_id>', methods=['PUT', 'DELETE'])
def update_cart(username, book_id):
    if username not in carts:
        return jsonify({"message": "User does not have a cart."})

    book_id = int(book_id)

    if request.method == 'PUT':
        data = request.get_json()
        for item in carts[username].items:
            if item.book_id == book_id:
                item.available = data.get('available', item.available)
                item.price = data.get('price', item.price)
                item.quantity = data.get('quantity', item.quantity)
                return jsonify({"message": f"Quantity of {item.title} updated in cart."})
        return jsonify({"message": f"Book ID {book_id} not found in cart."})
    elif request.method == 'DELETE':
        remove_quantity = int(request.args.get('remove_quantity', 1))
        carts[username].remove_from_cart(book_id, remove_quantity)
        return jsonify({"message": f"Book ID {book_id} quantity updated in cart."})

@app.route('/cart/<username>/total', methods=['GET'])
def cart_total(username):
    if username not in carts:
        return jsonify({"message": "User does not have a cart."})

    total = carts[username].calculate_total()
    return jsonify({"total": total})

@app.route('/cart/<username>/discount', methods=['POST'])
def apply_discount(username):
    if username not in carts:
        return jsonify({"message": "User does not have a cart."})

    data = request.get_json()
    discount_code = data.get('discount_code')
    for code in discount_codes:
        if code.code == discount_code:
            carts[username].discount_code = code
            return jsonify({"message": "Discount code valid!"})
    return jsonify({"message": "Invalid discount code."})

if __name__ == '__main__':
    app.run(debug=True)
