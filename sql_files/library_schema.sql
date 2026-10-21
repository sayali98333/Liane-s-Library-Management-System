CREATE SCHEMA IF NOT EXISTS library;
USE library;

-- 1. Books table
CREATE TABLE books (
    isbn VARCHAR(15) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    genre VARCHAR(50),
    book_language VARCHAR(50),
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);

-- 2. Friends table
CREATE TABLE friends (
    friends_id INT AUTO_INCREMENT PRIMARY KEY,
    friends_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(100) NOT NULL UNIQUE,
    max_loans INT NOT NULL DEFAULT 5
);

-- 3. Loans table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(15) NOT NULL,
    friends_id INT NOT NULL,
    loan_date DATE NOT NULL DEFAULT (CURRENT_DATE()),
    due_date DATE NOT NULL,
    extended_due_date DATE NULL,
    extension_count TINYINT NOT NULL DEFAULT 0,
    return_date DATE NULL,

    FOREIGN KEY (isbn) REFERENCES books(isbn),
    FOREIGN KEY (friends_id) REFERENCES friends(friends_id)
);