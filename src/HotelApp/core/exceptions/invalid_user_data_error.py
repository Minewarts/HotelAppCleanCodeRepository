from .user_error import UserError


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
