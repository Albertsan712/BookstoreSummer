from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from decimal import Decimal

db = SQLAlchemy()

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    copies_sold = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __init__(self, book_id, title, author, genre, price, copies_sold, rating, publisher):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.copies_sold = copies_sold
        self.rating = rating
        self.publisher = publisher

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'price': float(self.price),
            'copies_sold': self.copies_sold,
            'rating': self.rating,
            'publisher': self.publisher
        }

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        db.init_app(self.app)
        self.create_tables_and_seed_data()
        self.add_routes()

    def create_tables_and_seed_data(self):
        with self.app.app_context():
            db.create_all()
            if not Book.query.first():
                self.seed_data()

    def seed_data(self):
        books = [
            Book(book_id=1, title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Classic', price=12.99, copies_sold=500, rating=4.3, publisher='Scribner'),
            Book(book_id=2, title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', price=10.50, copies_sold=800, rating=4.8, publisher='J.B. Lippincott & Co.'),
            Book(book_id=3, title='1984', author='George Orwell', genre='Dystopian', price=15.75, copies_sold=600, rating=4.6, publisher='Secker & Warburg'),
            Book(book_id=4, title='Pride and Prejudice', author='Jane Austen', genre='Romance', price=9.99, copies_sold=700, rating=4.7, publisher='T. Egerton'),
            Book(book_id=5, title='The Catcher in the Rye', author='J.D. Salinger', genre='Coming-of-Age', price=11.25, copies_sold=750, rating=4.5, publisher='Little, Brown and Company'),
            Book(book_id=6, title='Moby Dick', author='Herman Melville', genre='Adventure', price=14.50, copies_sold=400, rating=4.1, publisher='Harper & Brothers'),
            Book(book_id=7, title='War and Peace', author='Leo Tolstoy', genre='Historical', price=19.99, copies_sold=300, rating=4.4, publisher='The Russian Messenger'),
            Book(book_id=8, title='Crime and Punishment', author='Fyodor Dostoevsky', genre='Psychological', price=13.75, copies_sold=450, rating=4.3, publisher='The Russian Messenger'),
            Book(book_id=9, title='The Brothers Karamazov', author='Fyodor Dostoevsky', genre='Philosophical', price=17.50, copies_sold=350, rating=4.5, publisher='The Russian Messenger'),
            Book(book_id=10, title='Brave New World', author='Aldous Huxley', genre='Science Fiction', price=12.00, copies_sold=550, rating=4.2, publisher='Chatto & Windus'),
            Book(book_id=11, title='The Hobbit', author='J.R.R. Tolkien', genre='Fantasy', price=10.99, copies_sold=600, rating=4.7, publisher='George Allen & Unwin'),
            Book(book_id=12, title='Anna Karenina', author='Leo Tolstoy', genre='Romance', price=11.50, copies_sold=400, rating=4.6, publisher='The Russian Messenger'),
            Book(book_id=13, title='The Adventures of Huckleberry Finn', author='Mark Twain', genre='Adventure', price=9.50, copies_sold=500, rating=4.4, publisher='Chatto & Windus'),
            Book(book_id=14, title='Jane Eyre', author='Charlotte Brontë', genre='Gothic', price=12.75, copies_sold=450, rating=4.5, publisher='Smith, Elder & Co.'),
            Book(book_id=15, title='Wuthering Heights', author='Emily Brontë', genre='Tragedy', price=10.25, copies_sold=480, rating=4.3, publisher='Thomas Cautley Newby')
        ]
        db.session.bulk_save_objects(books)
        db.session.commit()

    def add_routes(self):
        self.app.add_url_rule('/', 'get_books', self.get_books, methods=['GET'])
        self.app.add_url_rule('/books_by_genre', 'get_books_by_genre', self.get_books_by_genre, methods=['GET'])
        self.app.add_url_rule('/top_sellers', 'get_top_sellers', self.get_top_sellers, methods=['GET'])
        self.app.add_url_rule('/books_by_rating', 'get_books_by_rating', self.get_books_by_rating, methods=['GET'])
        self.app.add_url_rule('/discount_books_by_publisher', 'discount_books_by_publisher', self.discount_books_by_publisher, methods=['PUT'])

    def get_books(self):
        sort_by = request.args.get('sort_by', 'title')
        order = request.args.get('order', 'asc')

        if order == 'asc':
            books = Book.query.order_by(getattr(Book, sort_by).asc()).all()
        else:
            books = Book.query.order_by(getattr(Book, sort_by).desc()).all()

        books_list = [book.to_dict() for book in books]
        return jsonify(books_list)

    def get_books_by_genre(self):
        genre = request.args.get('genre')
        if genre:
            books = Book.query.filter_by(genre=genre).all()
            books_list = [book.to_dict() for book in books]
            return jsonify(books_list)
        else:
            return jsonify({"error": "Genre parameter is required"}), 400

    def get_top_sellers(self):
        top_books = Book.query.order_by(Book.copies_sold.desc()).limit(10).all()
        books_list = [book.to_dict() for book in top_books]
        return jsonify(books_list)

    def get_books_by_rating(self):
        rating = request.args.get('rating', type=float)
        if rating is not None:
            books = Book.query.filter(Book.rating >= rating).all()
            books_list = [book.to_dict() for book in books]
            return jsonify(books_list)
        else:
            return jsonify({"error": "Rating parameter is required"}), 400

    def discount_books_by_publisher(self):
        data = request.get_json()
        discount_percent = data.get('discount_percent')
        publisher = data.get('publisher')

        if discount_percent is None or publisher is None:
            return jsonify({"error": "Discount percent and publisher parameters are required"}), 400

        discount_decimal = Decimal(discount_percent) / 100
        books = Book.query.filter_by(publisher=publisher).all()
        for book in books:
            book.price = book.price * (1 - discount_decimal)
        db.session.commit()

        return jsonify({"message": f"Updated price of all books by {publisher} by {discount_percent}%."})

if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.app.run(debug=True)
