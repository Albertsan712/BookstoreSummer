from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    copies_sold = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, genre, price, copies_sold):
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.copies_sold = copies_sold

# Function to create a session within the app context
def get_session():
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        return Session()

class ShoppingCart:
    def __init__(self):
        self.carts = {}
        self.discount_code = None
        self.gift_card_discount = 0
        self.gift_card_codes = {
            "GIFT2022": 20,
            "GIFT2023": 30,
            "GIFT2024": 40
        }

    def get_cart(self, user_id):
        if user_id not in self.carts:
            self.carts[user_id] = []
        return self.carts[user_id]

    def add_to_cart(self, user_id, book_id, quantity=1):
        cart = self.get_cart(user_id)
        Session = get_session()
        with Session() as session:
            book = session.get(Book, book_id)
            if book:
                for item in cart:
                    if item['book_id'] == book_id:
                        item['quantity'] += quantity
                        return {"message": f"Quantity of {book.title} updated in cart."}
                cart.append({
                    'book_id': book.book_id,
                    'title': book.title,
                    'author': book.author,
                    'price': float(book.price),
                    'quantity': quantity
                })
                return {"message": f"{book.title} added to cart."}
            else:
                return {"message": "Sorry, book not available."}

    def remove_from_cart(self, user_id, book_id):
        cart = self.get_cart(user_id)
        for item in cart:
            if item['book_id'] == book_id:
                cart.remove(item)
                return {"message": f"{item['title']} removed from cart."}
        return {"message": "Book not found in cart."}

    def display_cart(self, user_id):
        cart = self.get_cart(user_id)
        return cart

    def calculate_total(self, user_id):
        cart = self.get_cart(user_id)
        total = sum(item['price'] * item['quantity'] for item in cart)

        if self.discount_code:
            total -= total * self.discount_code.discount_percentage

        total -= self.gift_card_discount

        return total

    def apply_gift_card(self, gift_card_code):
        if gift_card_code in self.gift_card_codes:
            discount_amount = self.gift_card_codes[gift_card_code]
            self.gift_card_discount += discount_amount
            return {"message": f"Gift card code {gift_card_code} applied. Discount amount: ${discount_amount}"}
        else:
            return {"message": "Invalid gift card code."}

class DiscountCode:
    def __init__(self, code, discount_percentage):
        self.code = code
        self.discount_percentage = discount_percentage

discount_codes = [
    DiscountCode("SUMMER2021", 0.1),
    DiscountCode("WINTER2021", 0.15),
    DiscountCode("SPRING2022", 0.2)
]

cart = ShoppingCart()

@app.route('/cart/total/<user_id>', methods=['GET'])
def cart_total(user_id):
    total = cart.calculate_total(user_id)
    return jsonify({"total": total})

@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)
    response = cart.add_to_cart(user_id, book_id, quantity)
    return jsonify(response)

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    items = cart.display_cart(user_id)
    return jsonify(items)

@app.route('/cart/<user_id>/<book_id>', methods=['DELETE'])
def remove_from_cart(user_id, book_id):
    response = cart.remove_from_cart(user_id, book_id)
    return jsonify(response)

@app.route('/cart/discount', methods=['POST'])
def apply_discount():
    data = request.get_json()
    discount_code = data.get('discount_code')
    for code in discount_codes:
        if code.code == discount_code:
            cart.discount_code = code
            return jsonify({"message": "Discount code applied."})
    return jsonify({"message": "Invalid discount code."})

@app.route('/cart/giftcard', methods=['POST'])
def apply_gift_card():
    data = request.get_json()
    gift_card_code = data.get('gift_card_code')
    response = cart.apply_gift_card(gift_card_code)
    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
