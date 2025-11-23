CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    region VARCHAR(50),
    signup_date DATE,
    lifetime_value DECIMAL(10, 2)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10, 2),
    stock INT
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    order_date DATE,
    quantity INT,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20)
);

INSERT INTO customers (customer_id, customer_name, email, region, signup_date, lifetime_value) VALUES
(1, 'Rajesh Kumar', 'rajesh@email.com', 'North', '2024-01-15', 45000),
(2, 'Priya Singh', 'priya@email.com', 'South', '2024-02-20', 32000),
(3, 'Amit Patel', 'amit@email.com', 'West', '2024-01-10', 58000),
(4, 'Sneha Dey', 'sneha@email.com', 'East', '2024-03-05', 28000),
(5, 'Vikram Joshi', 'vikram@email.com', 'North', '2024-02-14', 52000),
(6, 'Anjali Verma', 'anjali@email.com', 'South', '2024-01-25', 35000),
(7, 'Rohit Sharma', 'rohit@email.com', 'West', '2024-03-10', 41000),
(8, 'Divya Iyer', 'divya@email.com', 'East', '2024-02-28', 38000),
(9, 'Arun Nair', 'arun@email.com', 'North', '2024-01-20', 48000),
(10, 'Pooja Gupta', 'pooja@email.com', 'South', '2024-03-15', 55000);

INSERT INTO products (product_id, product_name, category, price, stock) VALUES
(1, 'Laptop Pro', 'Electronics', 85000, 15),
(2, 'Wireless Mouse', 'Electronics', 1500, 100),
(3, 'USB-C Cable', 'Electronics', 500, 200),
(4, 'Office Chair', 'Furniture', 12000, 20),
(5, 'Standing Desk', 'Furniture', 25000, 10),
(6, 'Monitor 4K', 'Electronics', 35000, 12),
(7, 'Keyboard Mechanical', 'Electronics', 8000, 25),
(8, 'Desk Lamp', 'Furniture', 3000, 50),
(9, 'Web Camera', 'Electronics', 5000, 30),
(10, 'Mouse Pad', 'Electronics', 800, 150);

INSERT INTO orders (order_id, customer_id, product_id, order_date, quantity, total_amount, status) VALUES
(1, 1, 1, '2024-01-20', 1, 85000, 'completed'),
(2, 2, 2, '2024-02-01', 2, 3000, 'completed'),
(3, 3, 1, '2024-01-25', 1, 85000, 'completed'),
(4, 1, 6, '2024-02-10', 1, 35000, 'completed'),
(5, 4, 4, '2024-02-15', 1, 12000, 'completed'),
(6, 5, 7, '2024-02-20', 2, 16000, 'completed'),
(7, 6, 2, '2024-03-01', 3, 4500, 'pending'),
(8, 7, 5, '2024-03-05', 1, 25000, 'completed'),
(9, 8, 3, '2024-03-10', 5, 2500, 'completed'),
(10, 9, 1, '2024-03-15', 1, 85000, 'completed'),
(11, 10, 6, '2024-03-18', 1, 35000, 'completed'),
(12, 2, 7, '2024-03-20', 1, 8000, 'completed'),
(13, 3, 4, '2024-03-22', 2, 24000, 'completed'),
(14, 4, 9, '2024-03-25', 1, 5000, 'pending'),
(15, 5, 2, '2024-03-28', 4, 6000, 'completed');
