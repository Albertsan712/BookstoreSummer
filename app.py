from flask import Flask, request, jsonify
from models import db, Book
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_tables_and_seed_data():
    with app.app_context():
        db.create_all()
        if not Book.query.first():
            seed_data()

def seed_data():
    books = [
        Book(book_id=1, title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Classic', price=12.99, copies_sold=500, rating=4.3, publisher='Scribner'),
        Book(book_id=2, title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', price=10.50, copies_sold=800, rating=4.8, publisher='J.B. Lippincott & Co.'),
        Book(book_id=3, title='1984', author='George Orwell', genre='Dystopian', price=15.75, copies_sold=600, rating=4.6, publisher='Secker & Warburg'),
        Book(book_id=4, title='Pride and Prejudice', author='Jane Austen', genre='Romance', price=9.99, copies_sold=700, rating=4.7, publisher='T. Egerton'),
        Book(book_id=5, title='The Catcher in the Rye', author='J.D. Salinger', genre='Coming-of-Age', price=11.25, copies_sold=750, rating=4.5, publisher='Little, Brown and Company')
    ]
    db.session.bulk_save_objects(books)
    db.session.commit()

create_tables_and_seed_data()

@app.route('/', methods=['GET'])
def get_books():
    sort_by = request.args.get('sort_by', 'title')
    order = request.args.get('order', 'asc')

    if order == 'asc':
        books = Book.query.order_by(getattr(Book, sort_by).asc()).all()
    else:
        books = Book.query.order_by(getattr(Book, sort_by).desc()).all()

    books_list = [
        {'book_id': book.book_id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'price': float(book.price)}
        for book in books
    ]
    return jsonify(books_list)

@app.route('/books_by_genre', methods=['GET'])
def get_books_by_genre():
    genre = request.args.get('genre')
    if genre:
        books = Book.query.filter_by(genre=genre).all()
        books_list = [
            {'book_id': book.book_id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'price': float(book.price)}
            for book in books
        ]
        return jsonify(books_list)
    else:
        return jsonify({"error": "Genre parameter is required"}), 400

@app.route('/top_sellers', methods=['GET'])
def get_top_sellers():
    top_books = Book.query.order_by(Book.copies_sold.desc()).limit(10).all()
    books_list = [
        {'book_id': book.book_id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'price': float(book.price), 'copies_sold': book.copies_sold}
        for book in top_books
    ]
    return jsonify(books_list)

@app.route('/books_by_rating', methods=['GET'])
def get_books_by_rating():
    rating = request.args.get('rating', type=float)
    if rating is not None:
        books = Book.query.filter(Book.rating >= rating).all()
        books_list = [
            {'book_id': book.book_id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'price': float(book.price), 'rating': book.rating}
            for book in books
        ]
        return jsonify(books_list)
    else:
        return jsonify({"error": "Rating parameter is required"}), 400

@app.route('/discount_books_by_publisher', methods=['PUT']) # this is a work in progress not ready for showcase!!!
def discount_books_by_publisher():
    data = request.get_json()
    discount_percent = data.get('discount_percent')
    publisher = data.get('publisher')

    if discount_percent is None or publisher is None:
        return jsonify({"error": "Discount percent and publisher parameters are required"}), 400

    books = Book.query.filter_by(publisher=publisher).all()
    for book in books:
        book.price = book.price * (1 - discount_percent / 100)
    db.session.commit()

    return jsonify({"message": f"Updated price of all books by {publisher} by {discount_percent}%."})

if __name__ == '__main__':
    app.run(debug=True)