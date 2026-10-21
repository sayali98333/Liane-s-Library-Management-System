import streamlit as st
from sqlalchemy import create_engine
import db


def login():

    st.title("🔐 Liana's Library Login")

    user = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", key="login_button"):

        # Get password from Streamlit secrets
        db_password = st.secrets["mysql"]["password"]

        # Create database connection
        connection_string = (
            f"mysql+pymysql://{user}:{db_password}"
            f"@127.0.0.1:3306/library"
        )

        try:
            engine = create_engine(connection_string)

            # Test the connection
            with engine.connect():
                pass

            # Save engine
            db.set_engine(engine)
            st.session_state["engine"] = engine

            # Login successful
            st.session_state["logged_in"] = True

            st.success("Login successful!")

            # Refresh the app
            st.rerun()

        except Exception as e:
            st.error(f"Login failed: {e}")

