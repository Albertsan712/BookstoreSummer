# Book class definition
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __repr__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __hash__(self):
        return hash(self.isbn)

# Wishlist class definition
class Wishlist:
    def __init__(self):
        self.books = set()  # Use a set to avoid duplicate books based on ISBN

    def add_book(self, book):
        if book not in self.books:
            self.books.add(book)
            print(f'Book {book} has been added to your wishlist.')
        else:
            print(f'Book {book} is already in your wishlist.')

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f'Book {book} has been removed from your wishlist.')
        else:
            print(f'Book {book} is not in your wishlist.')

    def view_wishlist(self):
        if self.books:
            print("Your wishlist contains the following books:")
            for book in self.books:
                print(f' - {book}')
        else:
            print("Your wishlist is empty.")

# Example usage
if __name__ == "__main__":
    wishlist = Wishlist()

    book1 = Book("1984", "George Orwell", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "1234567891")
    book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567892")

    wishlist.add_book(book1)
    wishlist.add_book(book2)
    wishlist.add_book(book3)
    wishlist.view_wishlist()

    wishlist.remove_book(book2)
    wishlist.view_wishlist()
