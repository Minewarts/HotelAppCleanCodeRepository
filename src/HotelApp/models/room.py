from __future__ import annotations
from decimal import Decimal
from typing import Literal
from ..core.exceptions import InvalidUserDataError


class Room:
    """
    Represents a room in the system.

    Attributes:
        _number_id (str): Unique identifier for the room (e.g., "101", "Suite A").
        _room_type (str): Type or category of the room.
        _price_per_night (Decimal): Price per night in currency units.
        _status (str): Current status of the room (Disponible, Ocupada, Mantenimiento).
    """

    def __init__(self, number_id: str, room_type: str, price_per_night: Decimal):
        """
        Initializes a new Room instance.

        Args:
            number_id (str): Unique identifier for the room.
            room_type (str): Type or category of the room.
            price_per_night (Decimal): Price per night (must be positive).

        Raises:
            ValueError: If the price_per_night is not positive.
        """
        self._validate_price(price_per_night)
        self._number_id = number_id
        self._room_type = room_type
        self._price_per_night = price_per_night
        self._status: Literal["Disponible", "Ocupada", "Mantenimiento"] = "Disponible"

    def get_number_id(self) -> str:
        """
        Returns the room identifier.

        Returns:
            str: The room number or identifier.
        """
        return self._number_id

    def get_room_type(self) -> str:
        """
        Returns the type of the room.

        Returns:
            str: The room type.
        """
        return self._room_type

    def get_price_per_night(self) -> Decimal:
        """
        Returns the price per night.

        Returns:
            Decimal: The price per night.
        """
        return self._price_per_night

    def get_status(self) -> str:
        """
        Returns the current status of the room.

        Returns:
            str: The room status (Disponible, Ocupada, Mantenimiento).
        """
        return self._status

    def set_status(self, status: Literal["Disponible", "Ocupada", "Mantenimiento"]):
        """
        Updates the status of the room.

        Args:
            status (str): New status for the room.

        Raises:
            ValueError: If the status is not valid.
        """
        if status not in ("Disponible", "Ocupada", "Mantenimiento"):
            raise ValueError("status must be 'Disponible', 'Ocupada' or 'Mantenimiento'")
        self._status = status

    def _validate_price(self, price_per_night: Decimal):
        """
        Validates that the price is positive.

        Args:
            price_per_night (Decimal): The price to validate.

        Raises:
            ValueError: If the price is not positive.
        """
        if price_per_night <= 0:
            raise ValueError("Price per night must be positive")

