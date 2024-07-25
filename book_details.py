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

# POST / Create a book
@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(
        isbn=data['isbn'],
        title=data['title'],
        author_id=data['author_id'],
        author=data['author'],
        genre=data['genre'],
        publisher=data['publisher'],
        price=data['price'],
        year_published=data.get('year_published', None),
        copies_sold=data['copies_sold'],
        rating=data.get('rating', None),
        description=data.get('description', None)
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book created successfully."}), 201


# GET / See book with input ISBN
@app.route('/book/<string:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        return jsonify({
            "book_id": book.book_id,
            "isbn": book.isbn,
            "title": book.title,
            "description": book.description,
            "price": book.price,
            "author": book.author,
            "genre": book.genre,
            "publisher": book.publisher,
            "year_published": book.year_published,
            "copies_sold": book.copies_sold
        }), 200
    else:
        return jsonify({"message": "Book not found."}), 404

# POST / Create an author
@app.route('/author', methods=['POST'])
def create_author():
    data = request.get_json()

    author = Author(author=data['author'], biography=data.get('biography'), publisher=data.get('publisher'))
    db.session.add(author)
    db.session.commit()
    return jsonify({"message": "Author created successfully."}), 201

# GET / See books by input author
@app.route('/author/<int:author_id>/books', methods=['GET'])
def get_books_by_author(author_id):
    books = Book.query.filter_by(author_id=author_id).all()
    book_list = [{
        "book_id": book.book_id,
        "isbn": book.isbn,
        "title": book.title,
        "description": book.description,
        "price": book.price,
        "author": book.author,
        "genre": book.genre,
        "publisher": book.publisher,
        "year_published": book.year_published,
        "copies_sold": book.copies_sold
    } for book in books]
    return jsonify(book_list), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
