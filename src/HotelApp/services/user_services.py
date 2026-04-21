from typing import List

from ..models import User, Room
from ..storage import Storage
from ..exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
)


class UserServices:

    """
    Service responsible for managing user-related operations


    The UserService class is responsible for creating, getting , and deleting users. 
    This class validates the user and, if they don't have an account, creates a new one and returns the value `user`.
    Otherwise, it  return  the user's name and ID and returns that value.
    
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def create_user(self, user: User) -> None:
        """
        This method create a User 

        args : user, this arg identify the user and save the variable generating a id >= 0 and a email.

        raises : 
        - InvalidUserDataError : The User id must be a number greater than zero. 
        - InvalidUserDataError : The user cannot leave the User empty.
        - InvalidUserDataError : The user must have the special character "@" in the email address. 
        """
        # validaciones ya hechas parcialmente en User, pero volvemos a validar
        if user.get_id() <= 0:
            raise InvalidUserDataError("User id must be a positive integer")

        if not user.get_name().strip():
            raise InvalidUserDataError("User name cannot be empty")

        if "@" not in user.get_email():
            raise InvalidUserDataError("Invalid email address")

        users: List[User] = self.storage.load()

        # check for duplicate id
        if any(u.get_id() == user.get_id() for u in users):
            raise UserAlreadyExistsError(user.get_id())

        users.append(user)
        self.storage.save(users)

    def get_user(self, user_id: int) -> User:

        '''
        This method get the user

        Args: user_id for identify the user who are you loking for

        Raises:
        - UserNotFoundError: It going to raise if the id of the User isnt found

        Returns: Object called User 
        '''

        users: List[User] = self.storage.load()
        for user in users:
            if user.get_id() == user_id:
                return user
        raise UserNotFoundError(f"User {user_id} not found")

    def delete_user(self, user_id: int) -> None:
        '''
        This method delete theh user from the storage

        Args ☆*: .｡. o(≧▽≦)o .｡.:*☆: used_id for identify the user tha you are looking for

        Raises 🚨: 
        - UserNotFoundError: it raises if the user isnt found in the storage

        Return ✈️: Nothing
        '''
        users: List[User] = self.storage.load()
        filtered = [u for u in users if u.get_id() != user_id]

        if len(filtered) == len(users):
            raise UserNotFoundError(f"User {user_id} not found")

        self.storage.save(filtered)
