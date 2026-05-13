from __future__ import annotations
from typing import List

from .room import Room
from .user import User


class Hotel:
    """
    Represents a hotel that manages rooms and clients.

    Attributes:
        _name (str): Name of the hotel.
        _address (str): Physical address of the hotel.
        _phone (str): Contact phone number.
        _rooms (List[Room]): List of rooms available in the hotel.
        _clients (List[User]): List of registered clients.
    """

    def __init__(self, name: str, address: str, phone: str):
        """
        Initializes a new Hotel instance.

        Args:
            name (str): Name of the hotel.
            address (str): Physical address of the hotel.
            phone (str): Contact phone number.
        """
        self._name = name
        self._address = address
        self._phone = phone
        self._rooms: List[Room] = []
        self._clients: List[User] = []

    def get_name(self) -> str:
        """
        Returns the name of the hotel.

        Returns:
            str: The hotel name.
        """
        return self._name

    def set_name(self, name: str) -> None:
        """Sets the hotel name."""
        self._name = name

    def get_address(self) -> str:
        """
        Returns the address of the hotel.

        Returns:
            str: The hotel address.
        """
        return self._address

    def set_address(self, address: str) -> None:
        """Sets the hotel address."""
        self._address = address

    def get_phone(self) -> str:
        """
        Returns the phone number of the hotel.

        Returns:
            str: The hotel phone.
        """
        return self._phone

    def set_phone(self, phone: str) -> None:
        """Sets the hotel phone number."""
        self._phone = phone

    def add_room(self, room: Room) -> None:
        """
        Adds a new room to the hotel.

        Args:
            room (Room): The room to add.

        Raises:
            ValueError: If a room with the same number already exists.
        """
        if self.get_room_by_number(room.get_number_id()) is not None:
            raise ValueError("Room already exists")
        self._rooms.append(room)

    def add_client(self, client: User) -> None:
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

    def get_client_by_id(self, client_id: int) -> User | None:
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

    def get_room_by_number(self, room_number: str) -> Room | None:
        """
        Searches for a room by its number.

        Args:
            room_number (str): Number of the room.

        Returns:
            Room | None: The room if found, otherwise None.
        """
        for room in self._rooms:
            if room.get_number_id() == room_number:
                return room
        return None

    def get_room_by_type(self, room_type: str) -> Room | None:
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

    def get_all_rooms(self) -> List[Room]:
        """Returns all rooms in the hotel."""
        return self._rooms

    def get_all_clients(self) -> List[User]:
        """Returns all registered clients."""
        return self._clients