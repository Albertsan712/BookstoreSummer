from flask import Flask, jsonify, request

app = Flask(__name__)

class Book:
    def __init__(self, title, author, price, available, quantity=1):
        self.title = title
        self.author = author
        self.price = price
        self.available = available
        self.quantity = quantity

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, book):
        if book.available:
            for item in self.items:
                if item.title == book.title:
                    item.quantity += book.quantity
                    print(f"Quantity of {book.title} updated in cart.")
                    break
            else:
                self.items.append(book)
                print(f"{book.title} added to cart.")
        else:
            print("Sorry, book not available.")

    def remove_from_cart(self, title, remove_quantity):
        for item in self.items:
            if item.title == title:
                if item.quantity > remove_quantity:
                    item.quantity -= remove_quantity
                    print(f"Quantity of {title} reduced by {remove_quantity} in cart.")
                elif item.quantity == remove_quantity:
                    self.items.remove(item)
                    print(f"{title} removed from cart.")
                else:
                    print(f"Cannot remove {remove_quantity} copies of {title} from cart. Only {item.quantity} available.")
                break
        else:
            print(f"{title} not found in cart.")

    def display_cart(self):
        print("Shopping Cart:")
        for item in self.items:
            print(f"- {item.title} by {item.author} (${item.price} for {item.quantity} items)")

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        return total

    def apply_discount(self, discount_code):
        if discount_code == "SUMMER2021":
            total = self.calculate_total()
            discount = total * 0.1  # 10% discount
            total -= discount
            return total
        else:
            return self.calculate_total()

cart = ShoppingCart()

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'GET':
        return jsonify([{"title": item.title, "author": item.author, "price": item.price, "quantity": item.quantity} for item in cart.items])
    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(data['title'], data['author'], data['price'], data['available'], data.get('quantity', 1))
        cart.add_to_cart(new_book)
        return jsonify({"message": "Book added to cart."})

@app.route('/cart/<title>', methods=['PUT', 'DELETE'])
def update_cart(title):
    if request.method == 'PUT':
        data = request.get_json()
        for item in cart.items:
            if item.title == title:
                item.available = data.get('available', item.available)
                item.price = data.get('price', item.price)
                item.quantity = data.get('quantity', item.quantity)
                return jsonify({"message": f"Quantity of {title} updated in cart."})
        return jsonify({"message": f"{title} not found in cart."})
    elif request.method == 'DELETE':
        remove_quantity = int(request.args.get('remove_quantity', 1))
        cart.remove_from_cart(title, remove_quantity)
        return jsonify({"message": f"{title} quantity updated in cart."})

@app.route('/cart/total', methods=['GET'])
def cart_total():
    total = cart.calculate_total()
    return jsonify({"total": total})

@app.route('/cart/discount', methods=['POST'])
def apply_discount():
    data = request.get_json()
    discount_code = data.get('discount_code')
    total = cart.apply_discount(discount_code)
    return jsonify({"total": total})

if __name__ == '__main__':
    app.run(debug=True)
