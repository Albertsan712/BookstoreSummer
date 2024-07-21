from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    copies_sold = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    publisher = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author_id': self.author_id,
            'genre': self.genre,
            'price': float(self.price),
            'copies_sold': self.copies_sold,
            'rating': self.rating,
            'publisher': self.publisher,
            'year_published': self.year_published
        }

# Define the Author model
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    biography = db.Column(db.String)
    publisher = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'biography': self.biography,
            'publisher': self.publisher,
            'books': [book.to_dict() for book in self.books]
        }

# Function to create a session within the app context
def get_session():
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        return Session()

# ShoppingCart class
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
            book = session.query(Book).get(book_id)
            if book:
                for item in cart:
                    if item['book_id'] == book_id:
                        item['quantity'] += quantity
                        return {"message": f"Quantity of {book.title} updated in cart."}
                cart.append({
                    'book_id': book.book_id,
                    'title': book.title,
                    'author': book.author.first_name + " " + book.author.last_name,
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

# Flask routes for managing books and authors
@app.route('/books', methods=['GET'])
def get_books():
    sort_by = request.args.get('sort_by', 'title')
    order = request.args.get('order', 'asc')

    if order == 'asc':
        books = Book.query.order_by(getattr(Book, sort_by).asc()).all()
    else:
        books = Book.query.order_by(getattr(Book, sort_by).desc()).all()

    books_list = [book.to_dict() for book in books]
    return jsonify(books_list)

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    authors_list = [author.to_dict() for author in authors]
    return jsonify(authors_list)

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
