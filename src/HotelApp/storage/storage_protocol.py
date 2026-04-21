from typing import List, Protocol

from ..models import User


class Storage(Protocol):
    """
    Protocol that defines the interface for a storage system.

    Any class implementing this protocol must provide methods to
    load and save a list of users.
    """

    def load(self) -> List[User]:
        """
        Loads users from the storage system.

        Returns:
            List[User]: A list of User objects retrieved from storage.
        """
        ...

    def save(self, users: List[User]) -> None:
        """
        Saves a list of users to the storage system.

        Args:
            users (List[User]): The list of users to be saved.
        """
        ...
