
from sqlalchemy import text
import db


# ---------------- FRIENDS ---------------- #

def delete_friend(friends_id):

    engine = db.get_engine()

    # Check if this friend has loan history
    check_query = text("""
        SELECT COUNT(*)
        FROM loans
        WHERE friends_id = :friends_id
    """)

    with engine.connect() as connection:
        loan_count = connection.execute(
            check_query,
            {"friends_id": friends_id}
        ).scalar()

    if loan_count > 0:
        return "This friend cannot be deleted because they have loan history."

    # Delete friend
    delete_query = text("""
        DELETE FROM friends
        WHERE friends_id = :friends_id
    """)

    with engine.begin() as connection:
        connection.execute(
            delete_query,
            {"friends_id": friends_id}
        )

    return "Friend deleted successfully."


# ---------------- BOOKS ---------------- #

def delete_book(isbn):

    engine = db.get_engine()

    # Check if this book has loan history
    check_query = text("""
        SELECT COUNT(*)
        FROM loans
        WHERE isbn = :isbn
    """)

    with engine.connect() as connection:
        loan_count = connection.execute(
            check_query,
            {"isbn": isbn}
        ).scalar()

    if loan_count > 0:
        return "This book cannot be deleted because it has loan history."

    # Delete book
    delete_query = text("""
        DELETE FROM books
        WHERE isbn = :isbn
    """)

    with engine.begin() as connection:
        connection.execute(
            delete_query,
            {"isbn": isbn}
        )

    return "Book deleted successfully."


# ---------------- LOANS ---------------- #

def delete_loan(loan_id):

    engine = db.get_engine()

    query = text("""
        DELETE FROM loans
        WHERE loan_id = :loan_id
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {"loan_id": loan_id}
        )

    return "Loan deleted successfully."