from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    copies_sold = db.Column(db.Integer, nullable=False, default=0)  # Added this field
    rating = db.Column(db.Float, nullable=False, default=0.0)  # Added this field
    publisher = db.Column(db.String(100), nullable=False)  # Added this field
