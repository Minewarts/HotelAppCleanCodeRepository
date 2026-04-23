from __future__ import annotations
from typing import List
from .exceptions import InvalidUserDataError


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