from __future__ import annotations
from typing import List, TYPE_CHECKING
from ..core.exceptions import InvalidUserDataError

if TYPE_CHECKING:
    from .user_history import UserHistory

class User:
    """
    Represents a user in the system.

    Attributes:
        _id (int): Unique identifier of the user.
        _first_name (str): First name of the user.
        _last_name (str): Last name of the user.
        _email (str): Email address of the user.
        history (List[UserHistory]): List of stay records for the user.
    """

    def __init__(self, user_id: int, first_name: str, last_name: str, email: str):
        """
        Initializes a new User instance.

        Args:
            user_id (int): Unique positive identifier for the user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            email (str): Email address of the user.

        Raises:
            InvalidUserDataError: If the user ID is not positive or the email is invalid.
        """
        self._validate_id(user_id)
        self._validate_email(email)

        self._id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self.history: List[UserHistory] = []

    def get_id(self) -> int:
        """
        Returns the user's ID.

        Returns:
            int: The unique identifier of the user.
        """
        return self._id

    def get_first_name(self) -> str:
        """
        Returns the user's first name.

        Returns:
            str: The first name of the user.
        """
        return self._first_name

    def get_last_name(self) -> str:
        """
        Returns the user's last name.

        Returns:
            str: The last name of the user.
        """
        return self._last_name

    def get_email(self) -> str:
        """
        Returns the user's email address.

        Returns:
            str: The email address of the user.
        """
        return self._email

    def _validate_id(self, user_id: int):
        """
        Validates that the user ID is a positive integer.

        Args:
            user_id (int): The ID to validate.

        Raises:
            InvalidUserDataError: If the ID is less than or equal to zero.
        """
        if user_id <= 0:
            raise InvalidUserDataError("User id must be positive")

    def _validate_email(self, user_email: str):
        """
        Validates the basic format of an email address.

        Args:
            user_email (str): The email address to validate.

        Raises:
            InvalidUserDataError: If the email is empty or does not contain '@'.
        """
        if "@" not in user_email or not user_email.strip():
            raise InvalidUserDataError("Invalid Email")