from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    title = db.Column(db.String(80), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    genre = db.Column(db.String(80), nullable=True)
    publisher = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Float, nullable=True)
    year_published = db.Column(db.Integer, nullable=True)
    copies_sold = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    publisher = db.Column(db.String(80), nullable=True)

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

# GET / see subtotal of user's cart
@app.route('/cart/<int:user_id>/subtotal', methods=['GET'])
def get_cart_subtotal(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
    subtotal = sum(Book.query.get(item.book_id).price for item in cart_items)
    return jsonify({"subtotal": subtotal}), 200

# POST / add books to user's cart
@app.route('/cart/<int:book_id>/<int:user_id>', methods=['POST'])
def add_to_cart(book_id, user_id):
    new_item = ShoppingCart(user_id=user_id, book_id=book_id)
    db.session.add(new_item)
    db.session.commit()
    book_title = Book.query.get(book_id).title
    return jsonify({"message": f"{book_title} was added to the cart."}), 201

# GET / see user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()
    books = [Book.query.get(item.book_id).title for item in cart_items]
    return jsonify(books), 200

# DELETE / remove book from user's cart
@app.route('/cart/remove/<int:book_id>/<int:user_id>', methods=['DELETE'])
def remove_from_cart(book_id, user_id):
    item = ShoppingCart.query.filter_by(user_id=user_id, book_id=book_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        book_title = Book.query.get(book_id).title
        return jsonify({"message": f"{book_title} was removed from the cart."}), 200
    else:
        return jsonify({"message": "Book not found in cart."}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)