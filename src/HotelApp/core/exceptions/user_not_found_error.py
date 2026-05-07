from .user_error import UserError


class UserNotFoundError(UserError):
    """
    Exception raised when a user with the specified ID cannot be found.
    """

    def __init__(self, user_id: int) -> None:
        """
        Initializes the exception.

        Args:
            user_id (int): ID of the user that was not found.
        """
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")
