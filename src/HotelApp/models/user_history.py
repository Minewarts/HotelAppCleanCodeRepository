from __future__ import annotations
from datetime import datetime
from typing import Optional
from .user import User
from .room import Room
from ..exceptions import InvalidUserDataError


class UserHistory:
    """
    Represents a stay record linking a user to a room.

    Attributes:
        _user (User): The user associated with this stay.
        _room (Room): The room occupied during this stay.
        _check_in (datetime): Timestamp when the user checked in.
        _check_out (Optional[datetime]): Timestamp when the user checked out, or None if ongoing.
    """

    def __init__(self, user: User, room: Room, check_in: Optional[datetime] = None):
        """
        Initializes a new UserHistory instance.

        Args:
            user (User): The user checking in.
            room (Room): The room being occupied.
            check_in (Optional[datetime]): Check-in time. Defaults to current time.

        Raises:
            InvalidUserDataError: If the room is not available or arguments are invalid.
        """
        self._validate_user(user)
        self._validate_room(room)

        self._user = user
        self._room = room
        self._check_in = check_in or datetime.now()
        self._check_out: Optional[datetime] = None

        self._room.set_status("occupied")
        self._user.history.append(self)

    

    def get_user(self) -> User:
        """Returns the user associated with this stay."""
        return self._user

    def get_room(self) -> Room:
        """Returns the room associated with this stay."""
        return self._room

    def get_check_in(self) -> datetime:
        """Returns the check-in timestamp."""
        return self._check_in

    def get_check_out(self) -> Optional[datetime]:
        """Returns the check-out timestamp, or None if the stay is ongoing."""
        return self._check_out

    def is_active(self) -> bool:
        """
        Indicates whether the stay is currently ongoing.

        Returns:
            bool: True if the user has not checked out yet.
        """
        return self._check_out is None

    

    def check_out(self, check_out_time: Optional[datetime] = None) -> None:
        """
        Registers the user's check-out and marks the room as available.

        Args:
            check_out_time (Optional[datetime]): Check-out time. Defaults to current time.

        Raises:
            InvalidUserDataError: If the stay is already closed.
        """
        if not self.is_active():
            raise InvalidUserDataError("This stay is already closed.")

        self._check_out = check_out_time or datetime.now()
        self._room.set_status("available")



    def _validate_user(self, user: User) -> None:
        """
        Validates that the user argument is a User instance.

        Raises:
            InvalidUserDataError: If user is not a User instance.
        """
        if not isinstance(user, User):
            raise InvalidUserDataError("A valid User instance is required.")

    def _validate_room(self, room: Room) -> None:
        """
        Validates that the room is a Room instance and is currently available.

        Raises:
            InvalidUserDataError: If room is not a Room instance or is already occupied.
        """
        if not isinstance(room, Room):
            raise InvalidUserDataError("A valid Room instance is required.")
        if room.get_status() != "available":
            raise InvalidUserDataError(
                f"Room {room.get_room_number()} is not available."
            )

   

    def __repr__(self) -> str:
        status = "active" if self.is_active() else "closed"
        return (
            f"UserHistory(user={self._user.get_name()!r}, "
            f"room={self._room.get_room_number()}, "
            f"status={status!r})"
        )