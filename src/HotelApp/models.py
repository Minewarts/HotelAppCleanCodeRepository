from __future__ import annotations
from typing import List
from .exceptions import InvalidUserDataError


class User:
    """
    Represents a user in the system.

    Attributes:
        _id (int): Unique identifier of the user.
        _name (str): Name of the user.
        _email (str): Email address of the user.
        history (List[Room]): List containing the history of rooms associated with the user.
    """

    def __init__(self, user_id: int, name: str, email: str):
        """
        Initializes a new User instance.

        Args:
            user_id (int): Unique positive identifier for the user.
            name (str): Name of the user.
            email (str): Email address of the user.

        Raises:
            InvalidUserDataError: If the user ID is not positive or the email is invalid.
        """
        self._validate_id(user_id)
        self._validate_email(email)

        self._id = user_id
        self._name = name
        self._email = email
        self.history: List[Room] = []

    def get_id(self):
        """
        Returns the user's ID.

        Returns:
            int: The unique identifier of the user.
        """
        return self._id

    def get_name(self):
        """
        Returns the user's name.

        Returns:
            str: The name of the user.
        """
        return self._name

    def get_email(self):
        """
        Returns the user's email address.

        Returns:
            str: The email address of the user.
        """
        return self._email

    def set_email(self, new_email):
        """
        Updates the user's email address after validation.

        Args:
            new_email (str): The new email address to assign.

        Raises:
            InvalidUserDataError: If the provided email is invalid.
        """
        self._validate_email(new_email)
        self._email = new_email

    def _validate_id(self, user_id):
        """
        Validates that the user ID is a positive integer.

        Args:
            user_id (int): The ID to validate.

        Raises:
            InvalidUserDataError: If the ID is less than or equal to zero.
        """
        if user_id <= 0:
            raise InvalidUserDataError("User id must be positive")

    def _validate_email(self, user_email):
        """
        Validates the basic format of an email address.

        Args:
            user_email (str): The email address to validate.

        Raises:
            InvalidUserDataError: If the email is empty or does not contain '@'.
        """
        if "@" not in user_email or not user_email.strip():
            raise InvalidUserDataError("Invalid Email")

class Room:
    """
    Represents a room in the system.

    Attributes:
        _room_number (int): Unique number identifying the room.
        _room_type (str): Type or category of the room.
        _status (str): Current status of the room (available or occupied).
    """

    def __init__(self, room_number: int, room_type: str):
        """
        Initializes a new Room instance.

        Args:
            room_number (int): Unique positive number identifying the room.
            room_type (str): Type or category of the room.

        Raises:
            ValueError: If the room number is not positive.
        """
        self._validate_room_number(room_number)
        self._room_number = room_number
        self._room_type = room_type
        self._status = "available"

    def get_room_number(self):
        """
        Returns the room number.

        Returns:
            int: The room number.
        """
        return self._room_number

    def get_room_type(self):
        """
        Returns the type of the room.

        Returns:
            str: The room type.
        """
        return self._room_type

    def get_status(self):
        """
        Returns the current status of the room.

        Returns:
            str: The room status ("available" or "occupied").
        """
        return self._status

    def set_status(self, status: str):
        """
        Updates the status of the room.

        Args:
            status (str): New status for the room.

        Raises:
            ValueError: If the status is not "available" or "occupied".
        """
        if status not in ("available", "occupied"):
            raise ValueError("status must be 'available' or 'occupied'")
        self._status = status

    def _validate_room_number(self, room_number):
        """
        Validates that the room number is a positive integer.

        Args:
            room_number (int): The room number to validate.

        Raises:
            ValueError: If the room number is less than or equal to zero.
        """
        if room_number <= 0:
            raise ValueError("Room number must be positive")

class Hotel:
    """
    Represents a hotel that manages rooms and clients.

    Attributes:
        _name (str): Name of the hotel.
        _stars (int | None): Star rating of the hotel.
        _rooms (List[Room]): List of rooms available in the hotel.
        _clients (List[User]): List of registered clients.
    """

    def __init__(self, name: str, stars: int | None = None):
        """
        Initializes a new Hotel instance.

        Args:
            name (str): Name of the hotel.
            stars (int | None): Optional star rating of the hotel.
        """
        self._name = name
        self._stars = stars
        self._rooms: List[Room] = []
        self._clients: List[User] = []

    def get_name(self):
        """
        Returns the name of the hotel.

        Returns:
            str: The hotel name.
        """
        return self._name

    def get_stars(self):
        """
        Returns the star rating of the hotel.

        Returns:
            int | None: The number of stars or None if not defined.
        """
        return self._stars

    def add_room(self, room: Room):
        """
        Adds a new room to the hotel.

        Args:
            room (Room): The room to add.

        Raises:
            ValueError: If a room with the same number already exists.
        """
        if self.get_room_by_number(room.get_room_number()) is not None:
            raise ValueError("Room already exists")
        self._rooms.append(room)

    def add_client(self, client: User):
        """
        Adds a new client to the hotel.

        Args:
            client (User): The client to add.

        Raises:
            ValueError: If a client with the same ID already exists.
        """
        if self.get_client_by_id(client.get_id()) is not None:
            raise ValueError("Client already exists")
        self._clients.append(client)

    def get_client_by_id(self, client_id):
        """
        Searches for a client by their ID.

        Args:
            client_id (int): ID of the client to find.

        Returns:
            User | None: The client if found, otherwise None.
        """
        for client in self._clients:
            if client.get_id() == client_id:
                return client
        return None

    def get_room_by_number(self, room_number):
        """
        Searches for a room by its number.

        Args:
            room_number (int): Number of the room.

        Returns:
            Room | None: The room if found, otherwise None.
        """
        for room in self._rooms:
            if room.get_room_number() == room_number:
                return room
        return None

    def get_room_by_type(self, room_type):
        """
        Searches for a room by its type.

        Args:
            room_type (str): Type of the room.

        Returns:
            Room | None: The room if found, otherwise None.
        """
        for room in self._rooms:
            if room.get_room_type() == room_type:
                return room
        return None