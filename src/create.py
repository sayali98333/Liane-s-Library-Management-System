
import pandas as pd
import db
from sqlalchemy import text


# ==================================================
# FRIENDS
# ==================================================

def create_friend(
    friends_name,
    phone_number=None,
    email=None,
    max_loans=5
):

    engine = db.get_engine()

    # Check if email already exists
    if email:
        query = text("""
            SELECT COUNT(*)
            FROM friends
            WHERE email = :email
        """)

        with engine.connect() as connection:
            exists = connection.execute(
                query,
                {"email": email}
            ).scalar()

        if exists > 0:
            return f"Email '{email}' already exists."

    # Create dataframe
    df = pd.DataFrame(
        [[friends_name, phone_number, email, max_loans]],
        columns=[
            "friends_name",
            "phone_number",
            "email",
            "max_loans"
        ]
    )

    # Insert into database
    df.to_sql(
        "friends",
        con=engine,
        if_exists="append",
        index=False
    )

    return f"Added '{friends_name}' to 'friends'."


# ==================================================
# BOOKS
# ==================================================

def create_book(
    isbn,
    title,
    author=None,
    genre=None,
    book_language=None,
    is_available=True
):

    engine = db.get_engine()

    # Check if ISBN already exists
    query = text("""
        SELECT COUNT(*)
        FROM books
        WHERE isbn = :isbn
    """)

    with engine.connect() as connection:
        exists = connection.execute(
            query,
            {"isbn": isbn}
        ).scalar()

    if exists > 0:
        return f"ISBN '{isbn}' already exists."

    # Create dataframe
    df = pd.DataFrame(
        [[
            isbn,
            title,
            author,
            genre,
            book_language,
            is_available
        ]],
        columns=[
            "isbn",
            "title",
            "author",
            "genre",
            "book_language",
            "is_available"
        ]
    )

    # Insert into database
    df.to_sql(
        "books",
        con=engine,
        if_exists="append",
        index=False
    )

    return f"Added '{title}' to 'books'."

# ==================================================
# LOANS
# ==================================================

def create_loan(
    isbn,
    friends_id,
    due_date
):

    engine = db.get_engine()

    # ----------------------------------------------
    # Check if book exists and is available
    # ----------------------------------------------

    book_query = text("""
        SELECT is_available
        FROM books
        WHERE isbn = :isbn
    """)

    with engine.connect() as connection:
        book = connection.execute(
            book_query,
            {"isbn": isbn}
        ).fetchone()

    if book is None:
        return f"Book with ISBN '{isbn}' does not exist."

    if not book[0]:
        return f"Book with ISBN '{isbn}' is already borrowed."

    # ----------------------------------------------
    # Check if friend exists
    # ----------------------------------------------

    friend_query = text("""
        SELECT COUNT(*)
        FROM friends
        WHERE friends_id = :friends_id
    """)

    with engine.connect() as connection:
        friend_exists = connection.execute(
            friend_query,
            {"friends_id": friends_id}
        ).scalar()

    if friend_exists == 0:
        return f"Friend with ID '{friends_id}' does not exist."

    # ----------------------------------------------
    # Create loan
    # ----------------------------------------------

    df = pd.DataFrame(
        [[isbn, friends_id, due_date]],
        columns=[
            "isbn",
            "friends_id",
            "due_date"
        ]
    )

    df.to_sql(
        "loans",
        con=engine,
        if_exists="append",
        index=False
    )

    # ----------------------------------------------
    # Make book unavailable
    # ----------------------------------------------

    update_query = text("""
        UPDATE books
        SET is_available = FALSE
        WHERE isbn = :isbn
    """)

    with engine.begin() as connection:
        connection.execute(
            update_query,
            {"isbn": isbn}
        )

    return f"Loan created for book '{isbn}'."