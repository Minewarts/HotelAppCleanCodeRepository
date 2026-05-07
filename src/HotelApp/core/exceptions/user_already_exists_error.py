from .user_error import UserError


class UserAlreadyExistsError(UserError):
    """
    Exception raised when attempting to create a user that already exists.
    """

    def __init__(self, user_id: int) -> None:
        """
        Initializes the exception.

        Args:
            user_id (int): ID of the user that already exists.
        """
        self.user_id = user_id
        super().__init__(f"User with id {user_id} already exists")
