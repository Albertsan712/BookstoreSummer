from Shoppingcartfeature import db, Book, Author

def add_books():
    # Authors table
    authors = [
        {"author_id": 1, "author": "F. Scott Fitzgerald", "biography": "American novelist", "publisher": "Scribner"},
        {"author_id": 2, "author": "Harper Lee", "biography": "American novelist", "publisher": "J.B. Lippincott & Co."},
        {"author_id": 3, "author": "George Orwell", "biography": "British writer and journalist", "publisher": "Secker & Warburg"},
        {"author_id": 4, "author": "Jane Austen", "biography": "English novelist", "publisher": "T. Egerton"},
        {"author_id": 5, "author": "J.D. Salinger", "biography": "American writer", "publisher": "Little, Brown and Company"},
        {"author_id": 6, "author": "Herman Melville", "biography": "American novelist", "publisher": "Harper & Brothers"},
        {"author_id": 7, "author": "Leo Tolstoy", "biography": "Russian writer", "publisher": "The Russian Messenger"},
        {"author_id": 8, "author": "Fyodor Dostoevsky", "biography": "Russian novelist", "publisher": "The Russian Messenger"},
        {"author_id": 9, "author": "Aldous Huxley", "biography": "English writer and philosopher", "publisher": "Chatto & Windus"},
        {"author_id": 10, "author": "J.R.R. Tolkien", "biography": "English writer", "publisher": "George Allen & Unwin"},
        {"author_id": 11, "author": "Mark Twain", "biography": "American writer and humorist", "publisher": "Chatto & Windus"},
        {"author_id": 12, "author": "Charlotte Brontë", "biography": "English novelist", "publisher": "Smith, Elder & Co."},
        {"author_id": 13, "author": "Emily Brontë", "biography": "English novelist and poet", "publisher": "Thomas Cautley Newby"}
    ]

    # Book table
    books = [
        {"book_id": 1, "isbn": "9780743273565", "title": "The Great Gatsby", "author_id": 1, "author": "F. Scott Fitzgerald", "genre": "Classic", "publisher": "Scribner", "price": 0.1299, "year_published": 1925, "copies_sold": 500, "rating": 4.3, "description": "A novel about the American dream and the Jazz Age."},
        {"book_id": 2, "isbn": "9780061120084", "title": "To Kill a Mockingbird", "author_id": 2, "author": "Harper Lee", "genre": "Fiction", "publisher": "J.B. Lippincott & Co.", "price": 0.105, "year_published": 1960, "copies_sold": 800, "rating": 4.8, "description": "A story about racial injustice in the American South."},
        {"book_id": 3, "isbn": "9780451524935", "title": "1984", "author_id": 3, "author": "George Orwell", "genre": "Dystopian", "publisher": "Secker & Warburg", "price": 15.75, "year_published": 1949, "copies_sold": 600, "rating": 4.6, "description": "A novel depicting a dystopian future under totalitarian rule."},
        {"book_id": 4, "isbn": "9780141439518", "title": "Pride and Prejudice", "author_id": 4, "author": "Jane Austen", "genre": "Romance", "publisher": "T. Egerton", "price": 9.99, "year_published": 1813, "copies_sold": 700, "rating": 4.7, "description": "A classic novel exploring the themes of love and social standing."},
        {"book_id": 5, "isbn": "9780316769488", "title": "The Catcher in the Rye", "author_id": 5, "author": "J.D. Salinger", "genre": "Coming-of-Age", "publisher": "Little, Brown and Company", "price": 11.25, "year_published": 1951, "copies_sold": 750, "rating": 4.5, "description": "A novel about teenage angst and rebellion."},
        {"book_id": 6, "isbn": "9780142437247", "title": "Moby Dick", "author_id": 6, "author": "Herman Melville", "genre": "Adventure", "publisher": "Harper & Brothers", "price": 14.5, "year_published": 1851, "copies_sold": 400, "rating": 4.1, "description": "A tale of obsession and revenge on the high seas."},
        {"book_id": 7, "isbn": "9781400079988", "title": "War and Peace", "author_id": 7, "author": "Leo Tolstoy", "genre": "Historical", "publisher": "The Russian Messenger", "price": 19.99, "year_published": 1869, "copies_sold": 300, "rating": 4.4, "description": "An epic novel set during the Napoleonic Wars."},
        {"book_id": 8, "isbn": "9780140449136", "title": "Crime and Punishment", "author_id": 8, "author": "Fyodor Dostoevsky", "genre": "Psychological", "publisher": "The Russian Messenger", "price": 13.75, "year_published": 1867, "copies_sold": 450, "rating": 4.3, "description": "A psychological drama exploring crime, guilt, and redemption."},
        {"book_id": 9, "isbn": "9780374528379", "title": "The Brothers Karamazov", "author_id": 8, "author": "Fyodor Dostoevsky", "genre": "Philosophical", "publisher": "The Russian Messenger", "price": 17.5, "year_published": 1880, "copies_sold": 350, "rating": 4.5, "description": "A novel delving into deep philosophical and theological questions."},
        {"book_id": 10, "isbn": "9780060850524", "title": "Brave New World", "author_id": 9, "author": "Aldous Huxley", "genre": "Science Fiction", "publisher": "Chatto & Windus", "price": 12, "year_published": 1932, "copies_sold": 550, "rating": 4.2, "description": "A dystopian novel about a technologically advanced society."},
        {"book_id": 11, "isbn": "9780261103283", "title": "The Hobbit", "author_id": 10, "author": "J.R.R. Tolkien", "genre": "Fantasy", "publisher": "George Allen & Unwin", "price": 10.99, "year_published": 1937, "copies_sold": 600, "rating": 4.7, "description": "A fantasy novel about a hobbit's journey to reclaim a treasure."},
        {"book_id": 12, "isbn": "9780143035008", "title": "Anna Karenina", "author_id": 7, "author": "Leo Tolstoy", "genre": "Romance", "publisher": "The Russian Messenger", "price": 11.5, "year_published": 1877, "copies_sold": 400, "rating": 4.6, "description": "A tragic love story set in 19th-century Russia."},
        {"book_id": 13, "isbn": "9780486280613", "title": "The Adventures of Huckleberry Finn", "author_id": 11, "author": "Mark Twain", "genre": "Adventure", "publisher": "Chatto & Windus", "price": 9.5, "year_published": 1884, "copies_sold": 500, "rating": 4.4, "description": "A classic adventure story following a young boy's journey."},
        {"book_id": 14, "isbn": "9780141441145", "title": "Jane Eyre", "author_id": 12, "author": "Charlotte Brontë", "genre": "Gothic", "publisher": "Smith, Elder & Co.", "price": 12.75, "year_published": 1847, "copies_sold": 450, "rating": 4.5, "description": "A novel about a woman's struggle for independence."},
        {"book_id": 15, "isbn": "9780141439558", "title": "Wuthering Heights", "author_id": 13, "author": "Emily Brontë", "genre": "Tragedy", "publisher": "Thomas Cautley Newby", "price": 10.25, "year_published": 1847, "copies_sold": 480, "rating": 4.3, "description": "A tragic love story set on the Yorkshire moors."}
    ]
    
    with db.session() as session:
        for author_data in authors:
            author = session.get(Author, author_data["author_id"])
            if author is None:
                author = Author(**author_data)
                session.add(author)

        for book_data in books:
            book = session.get(Book, book_data["book_id"])
            if book is None:
                book = Book(**book_data)
                session.add(book)
        session.commit()

if __name__ == '__main__':
    from Shoppingcartfeature import app
    with app.app_context():
        db.create_all()
        add_books()
