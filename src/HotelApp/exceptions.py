class AppError(Exception):
    """Base class for all application-specific exceptions."""

    pass


class UserError(AppError):
    """Base class for user-related exceptions."""

    pass


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


class InvalidUserDataError(UserError):
    """
    Exception raised when provided user data is invalid.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the exception.

        Args:
            message (str): Description of the validation error.
        """
        super().__init__(message)