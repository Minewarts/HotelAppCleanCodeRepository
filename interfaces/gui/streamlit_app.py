"""
User Manager GUI Application

This module provides a Streamlit-based graphical user interface for managing users in the HotelApp system.
It allows creating, listing, and deleting users through an interactive web interface.
"""

import streamlit as st
from HotelApp.services import UserServices
from HotelApp.storage import JSONStorage
from HotelApp.models import User
from HotelApp.core.exceptions import InvalidUserDataError, UserAlreadyExistsError, UserNotFoundError

storage = JSONStorage("data/database.json")
service = UserServices(storage)

st.title("User Manager")

tab1, tab2, tab3 = st.tabs(["Create User", "List Users", "Delete User"])

with tab1:
    st.header("Create a new user")
    name = st.text_input("Name", key="create_name")
    email = st.text_input("Email", key="create_email")

    if st.button("Create user"):
        try:
            users = storage.load()
            max_id = max((u.get_id() for u in users), default=0)
            new_id = max_id + 1
            user = User(new_id, name, email)
            service.create_user(user)
            st.success(f"User created with id {user.get_id()}")
        except (InvalidUserDataError, UserAlreadyExistsError) as e:
            st.error(str(e))

with tab2:
    st.header("List of users")
    users = storage.load()
    if users:
        for user in users:
            st.write(f"ID: {user.get_id()}, Name: {user.get_name()}, Email: {user.get_email()}")
    else:
        st.write("No users found.")

with tab3:
    st.header("Delete a user")
    user_id = st.number_input("User ID to delete", min_value=1, step=1, key="delete_id")

    if st.button("Delete user"):
        try:
            service.delete_user(int(user_id))
            st.success(f"User with id {user_id} deleted.")
        except UserNotFoundError as e:
            st.error(str(e))

