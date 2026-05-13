from __future__ import annotations
from datetime import datetime
from typing import Optional
from ..core.exceptions import InvalidUserDataError


class UserHistory:
    """
    Represents an action or event record for a user.

    Attributes:
        _id (int): Unique identifier for this history record.
        _user_id (int): ID of the user associated with this action.
        _action (str): Description of the action performed.
        _description (Optional[str]): Additional details about the action.
        _timestamp (datetime): When the action occurred.
    """

    def __init__(
        self,
        user_id: int,
        action: str,
        description: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ):
        """
        Initializes a new UserHistory instance.

        Args:
            user_id (int): ID of the user.
            action (str): Description of the action.
            description (Optional[str]): Additional details.
            timestamp (Optional[datetime]): When it happened. Defaults to now.

        Raises:
            InvalidUserDataError: If the user_id is not positive or action is empty.
        """
        self._validate_user_id(user_id)
        self._validate_action(action)

        self._user_id = user_id
        self._action = action
        self._description = description
        self._timestamp = timestamp or datetime.now()

    def get_user_id(self) -> int:
        """Returns the associated user ID."""
        return self._user_id

    def get_action(self) -> str:
        """Returns the action description."""
        return self._action

    def get_description(self) -> Optional[str]:
        """Returns additional details about the action."""
        return self._description

    def get_timestamp(self) -> datetime:
        """Returns when the action occurred."""
        return self._timestamp

    def _validate_user_id(self, user_id: int) -> None:
        """
        Validates that the user_id is positive.

        Raises:
            InvalidUserDataError: If user_id is not positive.
        """
        if user_id <= 0:
            raise InvalidUserDataError("User ID must be positive.")

    def _validate_action(self, action: str) -> None:
        """
        Validates that the action is not empty.

        Raises:
            InvalidUserDataError: If action is empty.
        """
        if not action or not action.strip():
            raise InvalidUserDataError("Action cannot be empty.")

    def __repr__(self) -> str:
        return (
            f"UserHistory(user_id={self._user_id}, "
            f"action={self._action!r}, "
            f"timestamp={self._timestamp!r})"
        )