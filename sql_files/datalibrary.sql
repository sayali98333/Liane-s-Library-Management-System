USE library;

INSERT INTO books
(isbn, title, author, genre, book_language, is_available)
VALUES
('9780140449136', 'The Alchemist', 'Paulo Coelho', 'Fiction', 'English', TRUE),
('9780743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'English', TRUE),
('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 'English', FALSE),
('9780451524935', '1984', 'George Orwell', 'Dystopian', 'English', FALSE),
('9780141185064', 'Animal Farm', 'George Orwell', 'Political Fiction', 'English', TRUE),
('9780261102217', 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'English', TRUE),
('9780132350884', 'Clean Code', 'Robert C. Martin', 'Programming', 'English', TRUE),
('9781491957660', 'Python Crash Course', 'Eric Matthes', 'Programming', 'English', TRUE),
('9788184001754', 'The Palace of Illusions', 'Chitra Banerjee Divakaruni', 'Historical Fiction', 'English', TRUE),
('9780143454212', 'The Midnight Library', 'Matt Haig', 'Fiction', 'English', FALSE);

INSERT INTO friends
(friends_name, phone_number, email, max_loans)
VALUES
('Aarav Sharma', '4915112345678', 'aarav.sharma@example.com', 5),
('Priya Patel', '4915223456789', 'priya.patel@example.com', 3),
('Daniel Weber', '4916334567890', 'daniel.weber@example.com', 5),
('Emma Fischer', '4917445678901', 'emma.fischer@example.com', 4),
('Rahul Mehta', '4917556789012', 'rahul.mehta@example.com', 3);

INSERT INTO loans
(isbn, friends_id, loan_date, due_date, extended_due_date, extension_count, return_date)
VALUES
('9780061120084', 1, '2026-09-10', '2026-09-24', NULL, 0, NULL),
('9780451524935', 2, '2026-09-11', '2026-09-25', NULL, 0, NULL),
('9780143454212', 3, '2026-09-12', '2026-09-26', NULL, 0, NULL);