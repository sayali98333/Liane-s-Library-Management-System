
import pandas as pd
import db


# Make column names easier to read
def prettify_df(df):
    df = df.copy()

    df.columns = [
        c.upper() if c == "isbn"
        else c.replace("_", " ").capitalize()
        for c in df.columns
    ]

    return df.fillna("")


# ---------------- FRIENDS ---------------- #

def read_friends():
    engine = db.get_engine()
    return pd.read_sql("friends", con=engine)


def display_friends():
    friends = read_friends()
    return friends.pipe(prettify_df)


# ---------------- BOOKS ---------------- #

def read_books():
    engine = db.get_engine()
    return pd.read_sql("books", con=engine)


def display_books():
    books = read_books()
    return books.pipe(prettify_df).sort_values(by="Title")


# ---------------- LOANS ---------------- #

def read_loans():
    engine = db.get_engine()
    return pd.read_sql("loans", con=engine)


def display_loans():
    friends = read_friends()
    books = read_books()
    loans = read_loans()

    # Add friend information to loans
    loans = pd.merge(
        loans,
        friends,
        on="friends_id"
    )

    # Add book information to loans
    loans = pd.merge(
        loans,
        books,
        on="isbn"
    )

    return loans.pipe(prettify_df)
