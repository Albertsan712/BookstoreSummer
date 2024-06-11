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
        Book(book_id=1, title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Classic', price=12.99),
        Book(book_id=2, title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', price=10.50),
        Book(book_id=3, title='1984', author='George Orwell', genre='Dystopian', price=15.75),
        Book(book_id=4, title='Pride and Prejudice', author='Jane Austen', genre='Romance', price=9.99),
        Book(book_id=5, title='The Catcher in the Rye', author='J.D. Salinger', genre='Coming-of-Age', price=11.25)
    ]
    db.session.bulk_save_objects(books)
    db.session.commit()

create_tables_and_seed_data()

@app.route('/', methods=['GET'])
def get_books():
    sort_by = request.args.get('sort_by', 'title')  # default sort by title
    order = request.args.get('order', 'asc')  # default order ascending

    if order == 'asc':
        books = Book.query.order_by(getattr(Book, sort_by).asc()).all()
    else:
        books = Book.query.order_by(getattr(Book, sort_by).desc()).all()

    books_list = [
        {'book_id': book.book_id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'price': float(book.price)}
        for book in books
    ]
    return jsonify(books_list)
#NOTE: THE SORTING CODE I HAVE HERE IS NOT FINALIZED, THIS CODE IS FINALIZED WHEN IT COMES TO GET CALLS FOR DUMMY DATA
if __name__ == '__main__':
    app.run(debug=True)
