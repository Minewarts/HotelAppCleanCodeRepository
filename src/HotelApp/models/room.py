from __future__ import annotations
from typing import List
from ..core.exceptions import InvalidUserDataError


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

