import streamlit as st
from HotelApp.services import UserService
from HotelApp.storage import JSONStorage

storage = JSONStorage("data/database.json")
service = UserService(storage)

st.title("User Manager")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Create user"):

    user = service.create_user(name, email)

    st.success(f"User created with id {user.id}")

