"""
User Manager GUI Application

This module provides a Streamlit-based graphical user interface for managing users in the HotelApp system.
It connects to the FastAPI backend through HTTP requests.
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("User Manager")

tab1, tab2, tab3, tab4 = st.tabs(["Create User", "List Users", "Delete User", "User History"])

with tab1:
    st.header("Create a new user")
    first_name = st.text_input("First Name", key="create_first_name")
    last_name = st.text_input("Last Name", key="create_last_name")
    email = st.text_input("Email", key="create_email")

    if st.button("Create user"):
        try:
            response = requests.post(f"{API_URL}/users/", json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            })
            if response.status_code == 201:
                user = response.json()
                st.success(f"User created with ID {user['id']}")
            else:
                st.error(response.json().get("detail", "Error creating user"))
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure it is running.")

with tab2:
    st.header("List of users")
    try:
        response = requests.get(f"{API_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            if users:
                for user in users:
                    st.write(f"ID: {user['id']} | Name: {user['first_name']} {user['last_name']} | Email: {user['email']}")
            else:
                st.write("No users found.")
        else:
            st.error("Error fetching users.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure it is running.")

with tab3:
    st.header("Delete a user")
    user_id = st.number_input("User ID to delete", min_value=1, step=1, key="delete_id")

    if st.button("Delete user"):
        try:
            response = requests.delete(f"{API_URL}/users/{int(user_id)}")
            if response.status_code == 204:
                st.success(f"User with ID {user_id} deleted.")
            elif response.status_code == 404:
                st.error(f"User with ID {user_id} not found.")
            else:
                st.error("Error deleting user.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure it is running.")

with tab4:
    st.header("Register user room history")
    history_user_id = st.number_input("User ID", min_value=1, step=1, key="history_user_id")
    room_id = st.text_input("Room ID", key="history_room_id")
    action = st.text_input("Action", value="Reservation", key="history_action")
    description = st.text_area("Description", key="history_description")

    if st.button("Save history entry"):
        try:
            payload = {
                "user_id": int(history_user_id),
                "action": action,
            }
            if room_id.strip():
                payload["room_id"] = room_id.strip()
            if description.strip():
                payload["description"] = description.strip()

            response = requests.post(f"{API_URL}/user-history/", json=payload)
            if response.status_code == 201:
                st.success("History record created successfully.")
            else:
                st.error(response.json().get("detail", "Error recording history"))
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure it is running.")
