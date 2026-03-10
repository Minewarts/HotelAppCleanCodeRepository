from __future__ import annotations
from typing import List
from .exceptions import InvalidUserDataError


class User:
    """
    
    """
    def __init__(self, user_id: int, name: str, email: str):
        self._validate_id(user_id)
        self._validate_email(email)

        self._id = user_id
        self._name = name
        self._email = email
        self.history: List[Room] = []

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def set_email(self, new_email):
        self._validate_email(new_email)
        self._email = new_email

    def _validate_id(self, user_id):
        if user_id <= 0:
            raise InvalidUserDataError("User id must be positive")

    def _validate_email(self, user_email):
        if "@" not in user_email or not user_email.strip():
            raise InvalidUserDataError("Invalid Email")


class Room:
    def __init__(self, room_number: int, room_type: str):
        self._validate_room_number(room_number)
        self._room_number = room_number
        self._room_type = room_type
        self._status = "available"

    def get_room_number(self):
        return self._room_number

    def get_room_type(self):
        return self._room_type

    def get_status(self):
        return self._status

    def set_status(self, status: str):
        if status not in ("available", "occupied"):
            raise ValueError("status must be 'available' or 'occupied'")
        self._status = status

    def _validate_room_number(self, room_number):
        if room_number <= 0:
            raise ValueError("Room number must be positive")


class Hotel:
    def __init__(self, name: str, stars: int | None = None):
        self._name = name
        self._stars = stars
        self._rooms: List[Room] = []
        self._clients: List[User] = []

    def get_name(self):
        return self._name

    def get_stars(self):
        return self._stars

    def add_room(self, room: Room):
        if self.get_room_by_number(room.get_room_number()) is not None:
            raise ValueError("Room already exists")
        self._rooms.append(room)

    def add_client(self, client: User):
        if self.get_client_by_id(client.get_id()) is not None:
            raise ValueError("Client already exists")
        self._clients.append(client)

    def get_client_by_id(self, client_id):
        for client in self._clients:
            if client.get_id() == client_id:
                return client
        return None

    def get_room_by_number(self, room_number):
        for room in self._rooms:
            if room.get_room_number() == room_number:
                return room
        return None

    def get_room_by_type(self, room_type):
        for room in self._rooms:
            if room.get_room_type() == room_type:
                return room
        return None