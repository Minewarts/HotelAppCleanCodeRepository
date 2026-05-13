from typing import List

from ..models import User, UserHistory
from ..storage import Storage
from ..core.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
)


class UserServices:
    """
    Service responsible for managing user-related operations.

    The UserService class is responsible for creating, getting, updating, and deleting users.
    This class validates the user data and ensures consistency with the storage system.
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def create_user(self, user: User) -> None:
        """
        Creates a new user in the system.

        Args:
            user (User): The user object to create.

        Raises:
            InvalidUserDataError: If user data is invalid.
            UserAlreadyExistsError: If a user with the same ID already exists.
        """
        if user.get_id() <= 0:
            raise InvalidUserDataError("User id must be a positive integer")

        if not user.get_first_name().strip():
            raise InvalidUserDataError("User first name cannot be empty")

        if not user.get_last_name().strip():
            raise InvalidUserDataError("User last name cannot be empty")

        if "@" not in user.get_email():
            raise InvalidUserDataError("Invalid email address")

        users: List[User] = self.storage.load()

        # Check for duplicate id
        if any(u.get_id() == user.get_id() for u in users):
            raise UserAlreadyExistsError(user.get_id())

        users.append(user)
        self.storage.save(users)

    def get_user(self, user_id: int) -> User:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object if found.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        users: List[User] = self.storage.load()
        for user in users:
            if user.get_id() == user_id:
                return user
        raise UserNotFoundError(f"User {user_id} not found")

    def update_user(self, user_id: int, first_name: str | None = None, last_name: str | None = None, email: str | None = None) -> User:
        """
        Updates user information.

        Args:
            user_id (int): The ID of the user to update.
            first_name (str | None): New first name.
            last_name (str | None): New last name.
            email (str | None): New email.

        Returns:
            User: The updated user object.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        users: List[User] = self.storage.load()
        user = None
        for u in users:
            if u.get_id() == user_id:
                user = u
                break

        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")

        if first_name is not None:
            user._first_name = first_name
        if last_name is not None:
            user._last_name = last_name
        if email is not None:
            user._email = email

        self.storage.save(users)
        return user

    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user from the system.

        Args:
            user_id (int): The ID of the user to delete.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        users: List[User] = self.storage.load()
        filtered = [u for u in users if u.get_id() != user_id]

        if len(filtered) == len(users):
            raise UserNotFoundError(f"User {user_id} not found")

        self.storage.save(filtered)

    def add_history(self, user_id: int, history: UserHistory) -> None:
        """
        Adds a history record to a user.

        Args:
            user_id (int): The ID of the user.
            history (UserHistory): The history record to add.

        Raises:
            UserNotFoundError: If the user is not found.
        """
        user = self.get_user(user_id)
        user.history.append(history)
        users: List[User] = self.storage.load()
        self.storage.save(users)
