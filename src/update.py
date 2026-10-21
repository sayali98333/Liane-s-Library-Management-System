
from sqlalchemy import text
import db


# ---------------- FRIENDS ---------------- #

def update_friend(friend_id, field, new_data):

    engine = db.get_engine()

    query = text(f"""
        UPDATE friends
        SET {field} = :new_data
        WHERE friends_id = :friend_id
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "new_data": new_data,
                "friend_id": friend_id
            }
        )

    return "Friend updated."


# ---------------- BOOKS ---------------- #

def update_book(isbn, field, new_data):

    engine = db.get_engine()

    query = text(f"""
        UPDATE books
        SET {field} = :new_data
        WHERE isbn = :isbn
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "new_data": new_data,
                "isbn": isbn
            }
        )

    return "Book updated."


# ---------------- LOANS ---------------- #

def update_loan(loan_id, field, new_data):

    engine = db.get_engine()

    query = text(f"""
        UPDATE loans
        SET {field} = :new_data
        WHERE loan_id = :loan_id
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "new_data": new_data,
                "loan_id": loan_id
            }
        )

    return "Loan updated."


# ---------------- RETURN BOOK ---------------- #

def return_book(loan_id):

    engine = db.get_engine()

    # Find the ISBN connected to this loan
    find_loan = text("""
        SELECT isbn, return_date
        FROM loans
        WHERE loan_id = :loan_id
    """)

    with engine.connect() as connection:
        loan = connection.execute(
            find_loan,
            {"loan_id": loan_id}
        ).fetchone()

    if loan is None:
        return "Loan does not exist."

    isbn = loan[0]
    return_date = loan[1]

    # Check if already returned
    if return_date is not None:
        return "This book has already been returned."

    # Update loan and book together
    with engine.begin() as connection:

        # Set return date
        connection.execute(
            text("""
                UPDATE loans
                SET return_date = CURRENT_DATE
                WHERE loan_id = :loan_id
            """),
            {"loan_id": loan_id}
        )

        # Make book available again
        connection.execute(
            text("""
                UPDATE books
                SET is_available = TRUE
                WHERE isbn = :isbn
            """),
            {"isbn": isbn}
        )

    return "Book returned successfully."


# ---------------- EXTEND LOAN ---------------- #

def extend_loan(loan_id, new_due_date):

    engine = db.get_engine()

    # Get current loan information
    find_loan = text("""
        SELECT extension_count, return_date
        FROM loans
        WHERE loan_id = :loan_id
    """)

    with engine.connect() as connection:
        loan = connection.execute(
            find_loan,
            {"loan_id": loan_id}
        ).fetchone()

    if loan is None:
        return "Loan does not exist."

    extension_count = loan[0]
    return_date = loan[1]

    # Check if book has already been returned
    if return_date is not None:
        return "This book has already been returned."

    # Allow maximum 2 extensions
    if extension_count >= 2:
        return "This loan cannot be extended more than 2 times."

    # Update loan
    query = text("""
        UPDATE loans
        SET extended_due_date = :new_due_date,
            extension_count = extension_count + 1
        WHERE loan_id = :loan_id
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "new_due_date": new_due_date,
                "loan_id": loan_id
            }
        )

    return "Loan extended successfully."
