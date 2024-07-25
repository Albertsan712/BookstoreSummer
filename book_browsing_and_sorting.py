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

    def serialize(self):
        return {
            "book_id": self.book_id,
            "isbn": self.isbn,
            "title": self.title,
            "author_id": self.author_id,
            "author": self.author,
            "genre": self.genre,
            "publisher": self.publisher,
            "price": self.price,
            "year_published": self.year_published,
            "copies_sold": self.copies_sold,
            "rating": self.rating,
            "description": self.description
        }

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    publisher = db.Column(db.String(80), nullable=True)

class BookAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=True)
    book = db.relationship('Book', backref=db.backref('book_authors', lazy=True))
    author = db.relationship('Author', backref=db.backref('book_authors', lazy=True))

# GET / See all book that are part of the input genre
@app.route('/books/genre/<genre>', methods=['GET'])
def get_books_by_genre(genre): 
    books = Book.query.filter_by(genre=genre).all()
    return jsonify([book.serialize() for book in books]), 200

# GET / See top 10 best selling books
@app.route('/books/top-sellers', methods=['GET'])
def get_top_sellers():
    books = Book.query.order_by(Book.copies_sold.desc()).limit(10).all()
    return jsonify([book.serialize() for book in books]), 200

# GET / See books with a rating >= input
@app.route('/books/rating/<float:min_rating>', methods=['GET'])
def get_books_by_rating(min_rating):
    books = Book.query.filter(Book.rating >= min_rating).all()
    return jsonify([book.serialize() for book in books]), 200

# PUT / Discount book by input percent for input publisher
@app.route('/books/discount', methods=['PUT'])
def discount_books():
    data = request.get_json()
    discount_percent = data['discount_percent']
    publisher = data['publisher']
    books = Book.query.filter_by(publisher=publisher).all()
    for book in books:
        book.price -= book.price * (discount_percent / 100)
        db.session.commit()
        return jsonify({"message": f"Successfully discounted books by {publisher}."}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)