# Check if the user is logged in

# If the user is not logged in, show the login page

# If the user is logged in, show the library

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import db
from login import *
from read import *
from create import *
from update import *
from delete import *
#import the own function .py files from the same directory


# ---------- Database setup ---------- #

DB_USER = "root"
DB_PORT = 3306
DB_HOST = "127.0.0.1"

DB_NAME = "library"
SQL_PASS= st.secrets["mysql"]["password"]

connection_string = f"mysql+pymysql://{DB_USER}:{SQL_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if "engine" not in st.session_state:
    st.session_state["engine"] = create_engine(connection_string)

db.set_engine(st.session_state["engine"])


# ---------- Check Login ---------- #

if "login" not in st.session_state:

    # User is NOT logged in
    login()

    st.stop()


# ---------- Library App ---------- #

st.title("Welcome to your Library!", text_alignment="center")

action= st.radio("Selection:", options=["Read friends", "Create friend", "Update friend", "Delete friend"], key="action_selection")

if action == "Read_friends":
    friends_df = display_friends()
    st.dataframe(friends_df, hide_index=True, use_container_width=True)

if action == "create friend":
    friend_name = st.text_input("Friend's Name:")
    max_loans = st.number_input("Insert Max Loans:", value=None,placeholder="Type a number....")
    notes = st.text_area("Notes:")

    if st.button("Add Friend"):
        message = create_friend(friend_name, max_loans)
        st.success(message)
        st.balloons()

if action == "Update friend":
    friends_df = read_friends()

    friend_names = st.selectbox("Select a friend to update:",friends_df["name"])
    friend= friends_df[friends_df["name"] == friend_names].iloc[0]

    fields_choice = st.selectbox("Select fields to update:", options=["Name", "Max Loans"])



  if action == "Delete friend":
    friends_df = read_friends()

    friend_names = st.selectbox("Select a friend to delete:",friends_df["friends_name"])
    friend= friends_df[friends_df["friends_name"] == friend_names].iloc[0]

    if st.button("Delete Friend"):
        message = delete_friend(friend)
        st.success(message)