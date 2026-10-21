
# ==========================================================
# LIANA'S LIBRARY
# ==========================================================
# Check if the user is logged in.
# If the user is not logged in, show the login page.
# If the user is logged in, show the library.
# ==========================================================

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

import db
from login import *
from read import *
from create import *
from update import *
from delete import *


# ==========================================================
# DATABASE SETUP
# ==========================================================

DB_USER = "root"
DB_PORT = 3306
DB_HOST = "127.0.0.1"
DB_NAME = "library"

SQL_PASS = st.secrets["mysql"]["password"]

connection_string = (
    f"mysql+pymysql://{DB_USER}:{SQL_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

if "engine" not in st.session_state:
    st.session_state["engine"] = create_engine(
        connection_string
    )

db.set_engine(st.session_state["engine"])


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# ==========================================================
# SHOW LOGIN PAGE
# ==========================================================

if not st.session_state["logged_in"]:

    login()


# ==========================================================
# SHOW LIBRARY AFTER LOGIN
# ==========================================================

else:

    # ======================================================
    # MAIN HEADING
    # ======================================================

    st.markdown(
        """
        <h1 style="text-align: center;">
            📚 Liana's Library
        </h1>

        <p style="text-align: center;">
            Manage books, friends and loans
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    # ======================================================
    # SIDEBAR
    # ======================================================

    st.sidebar.title("📚 Library Menu")

    page = st.sidebar.radio(
        "Select a page",
        [
            "Dashboard",
            "Books",
            "Friends",
            "Loans"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.rerun()


    # ======================================================
    # DASHBOARD
    # ======================================================

    if page == "Dashboard":

        st.header("📊 Dashboard")

        st.caption(
            "Quick overview of your library."
        )

        # --------------------------------------------------
        # GET DATA
        # --------------------------------------------------

        books = display_books()
        friends = display_friends()
        loans = display_loans()


        # --------------------------------------------------
        # BOOK STATISTICS
        # --------------------------------------------------

        total_books = len(books)

        total_friends = len(friends)

        if not books.empty:

            available_books = len(
                books[
                    books["Is available"] == 1
                ]
            )

        else:

            available_books = 0


        borrowed_books = (
            total_books - available_books
        )


        # --------------------------------------------------
        # LOAN STATISTICS
        # --------------------------------------------------

        if not loans.empty:

            # Make a copy so we do not change the
            # original dataframe.

            loan_data = loans.copy()

            # Convert Return date to datetime.
            # Empty values and NULL values become NaT.

            loan_data["Return date"] = pd.to_datetime(
                loan_data["Return date"],
                errors="coerce"
            )

            # Active loans = books that have not
            # been returned.

            active_loans = loan_data[
                loan_data["Return date"].isna()
            ].copy()

            # Returned loans

            returned_loans = loan_data[
                loan_data["Return date"].notna()
            ].copy()

            active_loan_count = len(
                active_loans
            )

            returned_count = len(
                returned_loans
            )

        else:

            active_loans = pd.DataFrame()

            active_loan_count = 0

            returned_count = 0


        # --------------------------------------------------
        # OVERDUE LOANS
        # --------------------------------------------------

        overdue_count = 0

        if not active_loans.empty:

            active_loans["Due date"] = pd.to_datetime(
                active_loans["Due date"],
                errors="coerce"
            )

            today = pd.Timestamp.today().normalize()

            overdue_loans = active_loans[
                active_loans["Due date"] < today
            ]

            overdue_count = len(
                overdue_loans
            )


        # ==================================================
        # LIBRARY + LOANS TABLES
        # ==================================================

        col1, col2 = st.columns(2)


        # --------------------------------------------------
        # LIBRARY TABLE
        # --------------------------------------------------

        with col1:

            st.subheader("📚 Library")

            library_data = pd.DataFrame(
                {
                    "Information": [
                        "Total Books",
                        "Available",
                        "Borrowed",
                        "Friends"
                    ],

                    "Count": [
                        total_books,
                        available_books,
                        borrowed_books,
                        total_friends
                    ]
                }
            )

            st.table(
                library_data
            )


        # --------------------------------------------------
        # LOANS TABLE
        # --------------------------------------------------

        with col2:

            st.subheader("📖 Loans")

            loans_data = pd.DataFrame(
                {
                    "Information": [
                        "Active Loans",
                        "Returned",
                        "Overdue"
                    ],

                    "Count": [
                        active_loan_count,
                        returned_count,
                        overdue_count
                    ]
                }
            )

            st.table(
                loans_data
            )


        # ==================================================
        # OVERDUE MESSAGE
        # ==================================================

        if overdue_count > 0:

            st.warning(
                f"⚠️ {overdue_count} overdue loan"
                f"{'s' if overdue_count != 1 else ''} "
                "needs your attention."
            )

        else:

            st.success(
                "✅ No overdue loans."
            )


        # ==================================================
        # CURRENT LOANS
        # ==================================================

        st.subheader("📋 Current Loans")

        if active_loan_count == 0:

            st.info(
                "🎉 There are currently no active loans."
            )

        else:

            display_columns = [
                "Loan id",
                "Title",
                "Friends name",
                "Due date"
            ]

            # Only select columns that actually exist.

            available_columns = [
                column
                for column in display_columns
                if column in active_loans.columns
            ]

            dashboard_loans = active_loans[
                available_columns
            ].copy()


            # ----------------------------------------------
            # FORMAT DUE DATE
            # ----------------------------------------------

            if "Due date" in dashboard_loans.columns:

                dashboard_loans["Due date"] = (
                    pd.to_datetime(
                        dashboard_loans["Due date"],
                        errors="coerce"
                    )
                    .dt.strftime("%d/%m/%y")
                )


            # ----------------------------------------------
            # RENAME COLUMNS FOR DASHBOARD
            # ----------------------------------------------

            dashboard_loans = dashboard_loans.rename(
                columns={
                    "Loan id": "Loan ID",
                    "Friends name": "Friend",
                    "Due date": "Due Date"
                }
            )


            # ----------------------------------------------
            # DISPLAY CURRENT LOANS
            # ----------------------------------------------

            st.dataframe(
                dashboard_loans,
                use_container_width=True,
                hide_index=True,
                height=180
            )


        # ==================================================
        # SIMPLE LIBRARY MESSAGE
        # ==================================================

        st.divider()

        st.caption(
            f"You have {total_books} books, "
            f"{available_books} available books, "
            f"{total_friends} friends and "
            f"{active_loan_count} active loans."
        )


    # ======================================================
    # BOOKS
    # ======================================================

    elif page == "Books":

        st.header("📚 Books")

        st.caption(
            "Add, update, delete and search books in your library."
        )


        # ==================================================
        # ADD NEW BOOK
        # ==================================================

        with st.expander("➕ Add a Book"):

            isbn = st.text_input(
                "ISBN",
                key="add_isbn"
            )

            title = st.text_input(
                "Title",
                key="add_title"
            )

            author = st.text_input(
                "Author",
                key="add_author"
            )

            genre = st.text_input(
                "Genre",
                key="add_genre"
            )

            book_language = st.text_input(
                "Language",
                key="add_language"
            )

            is_available = st.checkbox(
                "Book is available",
                value=True,
                key="add_available"
            )

            if st.button(
                "➕ Add Book",
                key="add_book_button",
                use_container_width=True
            ):

                if isbn == "":

                    st.warning(
                        "Please enter the ISBN."
                    )

                elif title == "":

                    st.warning(
                        "Please enter the book title."
                    )

                elif author == "":

                    st.warning(
                        "Please enter the author."
                    )

                else:

                    message = create_book(
                        isbn,
                        title,
                        author,
                        genre,
                        book_language,
                        is_available
                    )

                    if "already exists" in message:

                        st.warning(message)

                    else:

                        st.success(message)
                        st.rerun()


        # ==================================================
        # UPDATE BOOK
        # ==================================================

        st.divider()

        with st.expander("✏️ Update a Book"):

            books = display_books()

            if books.empty:

                st.info(
                    "📚 There are no books to update."
                )

            else:

                book_options = dict(
                    zip(
                        books["Title"],
                        books["ISBN"]
                    )
                )

                selected_book = st.selectbox(
                    "Select Book",
                    list(book_options.keys()),
                    key="update_book_select"
                )

                selected_isbn = book_options[
                    selected_book
                ]

                field = st.selectbox(
                    "What do you want to update?",
                    [
                        "title",
                        "author",
                        "genre",
                        "book_language"
                    ],
                    key="update_book_field"
                )

                new_data = st.text_input(
                    "Enter new value",
                    key="update_book_value"
                )

                if st.button(
                    "✏️ Update Book",
                    key="update_book_button",
                    use_container_width=True
                ):

                    if new_data == "":

                        st.warning(
                            "Please enter a new value."
                        )

                    else:

                        message = update_book(
                            selected_isbn,
                            field,
                            new_data
                        )

                        st.success(message)
                        st.rerun()


        # ==================================================
        # DELETE BOOK
        # ==================================================

        st.divider()

        with st.expander("🗑️ Delete a Book"):

            books = display_books()

            if books.empty:

                st.info(
                    "📚 There are no books to delete."
                )

            else:

                book_options = dict(
                    zip(
                        books["Title"],
                        books["ISBN"]
                    )
                )

                selected_book = st.selectbox(
                    "Select Book",
                    list(book_options.keys()),
                    key="delete_book_select"
                )

                selected_isbn = book_options[
                    selected_book
                ]

                st.warning(
                    "⚠️ Deleting a book cannot be undone."
                )

                confirm_delete = st.checkbox(
                    "I understand that this book will be deleted.",
                    key="confirm_delete_book"
                )

                if st.button(
                    "🗑️ Delete Book",
                    key="delete_book_button",
                    use_container_width=True
                ):

                    if not confirm_delete:

                        st.warning(
                            "Please confirm that you want to delete the book."
                        )

                    else:

                        message = delete_book(
                            selected_isbn
                        )

                        if "cannot be deleted" in message:

                            st.warning(message)

                        else:

                            st.success(message)
                            st.rerun()


        # ==================================================
        # SEARCH BOOKS
        # ==================================================

        st.divider()

        st.subheader("📖 All Books")

        search = st.text_input(
            "🔎 Search books",
            placeholder="Search by title, author or ISBN...",
            key="book_search"
        )

        books = display_books()

        if search:

            books = books[
                books["Title"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                books["Author"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                books["ISBN"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if books.empty:

            st.info(
                "📚 No books found."
            )

        else:

            st.dataframe(
                books,
                use_container_width=True,
                hide_index=True
            )


    # ======================================================
    # FRIENDS
    # ======================================================

    elif page == "Friends":

        st.header("👥 Friends")

        st.caption(
            "Add, update, delete and search library friends."
        )


        # ==================================================
        # ADD NEW FRIEND
        # ==================================================

        with st.expander("➕ Add a Friend"):

            friends_name = st.text_input(
                "Name",
                key="add_friend_name"
            )

            phone_number = st.text_input(
                "Phone Number",
                key="add_friend_phone"
            )

            email = st.text_input(
                "Email",
                key="add_friend_email"
            )

            max_loans = st.number_input(
                "Maximum Loans",
                min_value=1,
                value=5,
                key="add_friend_max_loans"
            )

            if st.button(
                "➕ Add Friend",
                key="add_friend_button",
                use_container_width=True
            ):

                if friends_name == "":

                    st.warning(
                        "Please enter the friend's name."
                    )

                elif email == "":

                    st.warning(
                        "Please enter the email."
                    )

                else:

                    message = create_friend(
                        friends_name,
                        phone_number,
                        email,
                        max_loans
                    )

                    if "already exists" in message:

                        st.warning(message)

                    else:

                        st.success(message)
                        st.rerun()


        # ==================================================
        # UPDATE FRIEND
        # ==================================================

        st.divider()

        with st.expander("✏️ Update a Friend"):

            friends = display_friends()

            if friends.empty:

                st.info(
                    "👥 There are no friends to update."
                )

            else:

                friend_options = dict(
                    zip(
                        friends["Friends name"],
                        friends["Friends id"]
                    )
                )

                selected_friend = st.selectbox(
                    "Select Friend",
                    list(friend_options.keys()),
                    key="update_friend_select"
                )

                selected_friend_id = friend_options[
                    selected_friend
                ]

                field = st.selectbox(
                    "What do you want to update?",
                    [
                        "friends_name",
                        "phone_number",
                        "email",
                        "max_loans"
                    ],
                    key="update_friend_field"
                )

                new_data = st.text_input(
                    "Enter new value",
                    key="update_friend_value"
                )

                if st.button(
                    "✏️ Update Friend",
                    key="update_friend_button",
                    use_container_width=True
                ):

                    if new_data == "":

                        st.warning(
                            "Please enter a new value."
                        )

                    else:

                        message = update_friend(
                            selected_friend_id,
                            field,
                            new_data
                        )

                        st.success(message)
                        st.rerun()


        # ==================================================
        # DELETE FRIEND
        # ==================================================

        st.divider()

        with st.expander("🗑️ Delete a Friend"):

            friends = display_friends()

            if friends.empty:

                st.info(
                    "👥 There are no friends to delete."
                )

            else:

                friend_options = dict(
                    zip(
                        friends["Friends name"],
                        friends["Friends id"]
                    )
                )

                selected_friend = st.selectbox(
                    "Select Friend",
                    list(friend_options.keys()),
                    key="delete_friend_select"
                )

                selected_friend_id = friend_options[
                    selected_friend
                ]

                st.warning(
                    "⚠️ Deleting a friend cannot be undone."
                )

                confirm_delete = st.checkbox(
                    "I understand that this friend will be deleted.",
                    key="confirm_delete_friend"
                )

                if st.button(
                    "🗑️ Delete Friend",
                    key="delete_friend_button",
                    use_container_width=True
                ):

                    if not confirm_delete:

                        st.warning(
                            "Please confirm that you want to delete the friend."
                        )

                    else:

                        message = delete_friend(
                            selected_friend_id
                        )

                        if "cannot be deleted" in message:

                            st.warning(message)

                        else:

                            st.success(message)
                            st.rerun()


        # ==================================================
        # SEARCH FRIENDS
        # ==================================================

        st.divider()

        st.subheader("👤 All Friends")

        search_friend = st.text_input(
            "🔎 Search friends",
            placeholder="Search by name or email...",
            key="friend_search"
        )

        friends = display_friends()

        if search_friend:

            friends = friends[
                friends["Friends name"].str.contains(
                    search_friend,
                    case=False,
                    na=False
                )
                |
                friends["Email"].str.contains(
                    search_friend,
                    case=False,
                    na=False
                )
            ]

        if friends.empty:

            st.info(
                "👥 No friends found."
            )

        else:

            st.dataframe(
                friends,
                use_container_width=True,
                hide_index=True
            )


    # ======================================================
    # LOANS
    # ======================================================

    elif page == "Loans":

        st.header("📖 Loans")

        st.caption(
            "Borrow, return and extend library books."
        )


        # ==================================================
        # DISPLAY ALL LOANS
        # ==================================================

        st.subheader("📋 All Loans")

        loans = display_loans()

        if loans.empty:

            st.info(
                "📖 No loans found."
            )

        else:

            st.dataframe(
                loans,
                use_container_width=True,
                hide_index=True
            )


        # ==================================================
        # BORROW A BOOK
        # ==================================================

        st.divider()

        with st.expander("➕ Borrow a Book"):

            books = display_books()
            friends = display_friends()

            available_books = books[
                books["Is available"] == 1
            ]

            if available_books.empty:

                st.info(
                    "📚 There are no books available to borrow."
                )

            elif friends.empty:

                st.info(
                    "👥 Please add a friend before creating a loan."
                )

            else:

                book_options = dict(
                    zip(
                        available_books["Title"],
                        available_books["ISBN"]
                    )
                )

                selected_book = st.selectbox(
                    "Select Book",
                    list(book_options.keys()),
                    key="loan_book_select"
                )

                friend_options = dict(
                    zip(
                        friends["Friends name"],
                        friends["Friends id"]
                    )
                )

                selected_friend = st.selectbox(
                    "Select Friend",
                    list(friend_options.keys()),
                    key="loan_friend_select"
                )

                due_date = st.date_input(
                    "Due Date",
                    key="loan_due_date"
                )

                if st.button(
                    "📖 Borrow Book",
                    key="borrow_book_button",
                    use_container_width=True
                ):

                    selected_isbn = book_options[
                        selected_book
                    ]

                    selected_friend_id = friend_options[
                        selected_friend
                    ]

                    message = create_loan(
                        selected_isbn,
                        selected_friend_id,
                        due_date
                    )

                    if "Loan created" in message:

                        st.success(message)
                        st.rerun()

                    else:

                        st.warning(message)


        # ==================================================
        # RETURN A BOOK
        # ==================================================

        st.divider()

        with st.expander("🔄 Return a Book"):

            loans = display_loans()

            if loans.empty:

                st.info(
                    "📖 There are no loans."
                )

            else:

                # Convert Return date to datetime
                # so NULL/empty values are handled correctly.

                loan_data = loans.copy()

                loan_data["Return date"] = pd.to_datetime(
                    loan_data["Return date"],
                    errors="coerce"
                )

                active_loans = loan_data[
                    loan_data["Return date"].isna()
                ]

                if active_loans.empty:

                    st.info(
                        "✅ There are no active loans."
                    )

                else:

                    loan_options = {}

                    for _, row in active_loans.iterrows():

                        label = (
                            f"Loan {row['Loan id']} - "
                            f"{row['Title']} - "
                            f"{row['Friends name']}"
                        )

                        loan_options[label] = row[
                            "Loan id"
                        ]

                    selected_loan = st.selectbox(
                        "Select Loan",
                        list(loan_options.keys()),
                        key="return_loan_select"
                    )

                    if st.button(
                        "🔄 Return Book",
                        key="return_book_button",
                        use_container_width=True
                    ):

                        loan_id = loan_options[
                            selected_loan
                        ]

                        message = return_book(
                            loan_id
                        )

                        if "successfully" in message:

                            st.success(message)
                            st.rerun()

                        else:

                            st.warning(message)


        # ==================================================
        # EXTEND A LOAN
        # ==================================================

        st.divider()

        with st.expander("📅 Extend a Loan"):

            loans = display_loans()

            if loans.empty:

                st.info(
                    "📖 There are no loans."
                )

            else:

                loan_data = loans.copy()

                loan_data["Return date"] = pd.to_datetime(
                    loan_data["Return date"],
                    errors="coerce"
                )

                active_loans = loan_data[
                    loan_data["Return date"].isna()
                ]

                if active_loans.empty:

                    st.info(
                        "✅ There are no active loans to extend."
                    )

                else:

                    loan_options = {}

                    for _, row in active_loans.iterrows():

                        label = (
                            f"Loan {row['Loan id']} - "
                            f"{row['Title']} - "
                            f"{row['Friends name']}"
                        )

                        loan_options[label] = row[
                            "Loan id"
                        ]

                    selected_loan = st.selectbox(
                        "Select Loan",
                        list(loan_options.keys()),
                        key="extend_loan_select"
                    )

                    new_due_date = st.date_input(
                        "New Due Date",
                        key="new_due_date"
                    )

                    if st.button(
                        "📅 Extend Loan",
                        key="extend_loan_button",
                        use_container_width=True
                    ):

                        loan_id = loan_options[
                            selected_loan
                        ]

                        message = extend_loan(
                            loan_id,
                            new_due_date
                        )

                        if "successfully" in message:

                            st.success(message)
                            st.rerun()

                        else:

                            st.warning(message)