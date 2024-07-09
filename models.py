from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    #author = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    copies_sold = db.Column(db.Integer, nullable=False, default=0)  # Added this field
    rating = db.Column(db.Float, nullable=False, default=0.0)  # Added this field
    publisher = db.Column(db.String(100), nullable=False)  # Added this field
    name = db.Column(db.String, nullable=False) # Added this field
    year_published = db.Column(db.Integer, nullable=False)
    


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    biography = db.Column(db.String)
    publisher = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

