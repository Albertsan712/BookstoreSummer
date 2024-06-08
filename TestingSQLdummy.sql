CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(100),
    genre VARCHAR(50),
    price DECIMAL(10, 2)
);

INSERT INTO books (book_id, title, author, genre, price) VALUES
(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 12.99),
(2, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 10.50),
(3, '1984', 'George Orwell', 'Dystopian', 15.75),
(4, 'Pride and Prejudice', 'Jane Austen', 'Romance', 9.99),
(5, 'The Catcher in the Rye', 'J.D. Salinger', 'Coming-of-Age', 11.25);
