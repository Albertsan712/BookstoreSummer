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

class WishList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class WishListItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wish_list.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    wishlist = db.relationship('WishList', backref=db.backref('items', lazy=True))
    book = db.relationship('Book')

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

# POST / Create a wishlist
@app.route('/wishlist', methods=['POST'])
def create_wishlist():
    data = request.get_json()
    wishlist_name = data['name']
    user_id = data['user_id']
    wishlist = WishList(name=wishlist_name, user_id=user_id)
    db.session.add(wishlist)
    db.session.commit()
    return jsonify({"message": "Wishlist created successfully."}), 201

# POST / Add a book to a wishlist
@app.route('/wishlist/<int:wishlist_id>/book/<int:book_id>', methods=['POST'])
def add_book_to_wishlist(wishlist_id, book_id):
    wishlist_item = WishListItems(wishlist_id=wishlist_id, book_id=book_id)
    db.session.add(wishlist_item)
    db.session.commit()
    return jsonify({"message": "Book added to wishlist successfully."}), 201

# DELETE / Remove a book from a wishlist & add it to the shopping cart
@app.route('/wishlist/<int:wishlist_id>/book/<int:book_id>', methods=['DELETE'])
def remove_book_from_wishlist(wishlist_id, book_id):
    wishlist_item = WishListItems.query.filter_by(wishlist_id=wishlist_id, book_id=book_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        user_id = WishList.query.get(wishlist_id).user_id
        new_cart_item = ShoppingCart(user_id=user_id, book_id=book_id)
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({"message": "Book moved to shopping cart successfully."}), 200
    else:
        return jsonify({"message": "Book not found in wishlist."}), 404

# GET / See all books in a wishlist
@app.route('/wishlist/<int:wishlist_id>', methods=['GET'])
def list_books_in_wishlist(wishlist_id):
    wishlist_items = WishListItems.query.filter_by(wishlist_id=wishlist_id).all()
    books = [{
        "title": item.book.title,
    } for item in wishlist_items]
    return jsonify(books), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
