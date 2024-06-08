-- Create a table for storing shopping cart items
CREATE TABLE shopping_cart (
    item_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(100),
    price DECIMAL(10, 2),
    quantity INT
);

-- Insert sample data into the shopping cart table
INSERT INTO shopping_cart (item_id, title, author, price, quantity)
VALUES (1, 'Book A', 'Author X', 19.99, 2),
       (2, 'Book B', 'Author Y', 24.99, 1);

-- Query to display the shopping cart contents
SELECT title, author, price, quantity, (price * quantity) AS total_price
FROM shopping_cart;
