from typing import List

from .models import User, Room, Hotel
from .storage import Storage

from .exceptions import (
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


class HotelService:
    """
    The class HotelService is the responsable to : 
    - Reserve a room 
    - Cancel a pending reservation 
    - Check the disponibility of a room 
    - Show the room user history ( you can look the status and the tenant . ) 
    """
    
    def __init__(self, storage: Storage):
        """
        Initializes the reservation manager with a storage system.

        Args:
            storage (Storage): Object responsible for loading and saving
            user information and their reservations.
        """
        self.storage = storage


    def reserve_room(self, user: User, room: Room) -> None:
        """
        Reserves a room for a given user.

        The method checks if the room is available. If it is available,
        the room status is changed to "occupied" and it is added to the
        user's history if it is not already present. The changes are then
        persisted in the storage system.

        Args:
            user (User): The user who wants to reserve the room.
            room (Room): The room to be reserved.

        Raises:
            Exception: If the room is not available.
            UserNotFoundError: If the user does not exist in storage.
        """
        # Verificamos disponibilidad vida hjpta 😊
        if room.get_status() != "available":
            raise Exception("Room is not available")

        # ocupamos la habitación y añadimos al historial del usuario
        room.set_status("occupied")
        # evitar duplicados
        if room not in user.history:
            user.history.append(room)

        # si quieres persistir cambios en storage, debes cargar usuarios, actualizar y guardar.
        users = self.storage.load()
        for u in users:
            if u.get_id() == user.get_id():
                u.history = user.history
                break
        else:
            # si el usuario no existe en el storage, opcional: levantar excepción
            raise UserNotFoundError(f"User {user.get_id()} not found")
        self.storage.save(users)


    def cancel_reservation(self, user: User, room: Room) -> None:
        """
        Cancels a room reservation for a given user.

        The method verifies that the room exists in the user's history.
        If it does, the room status is changed to "available" and the room
        is removed from the user's reservation history. The changes are
        then saved in the storage system.

        Args:
            user (User): The user who cancels the reservation.
            room (Room): The room whose reservation will be canceled.

        Raises:
            Exception: If the room is not reserved by the user.
            UserNotFoundError: If the user does not exist in storage.
        """
        # comprobar que la habitación está en el historial del usuario
        if room not in user.history:
            raise Exception("Room is not reserved by the user")

        # liberar habitación y quitar del historial
        room.set_status("available")
        user.history.remove(room)

        # persistir cambios
        users = self.storage.load()
        for u in users:
            if u.get_id() == user.get_id():
                u.history = user.history
                break
        else:
            raise UserNotFoundError(f"User {user.get_id()} not found")
        self.storage.save(users)


    def check_availability(self, room: Room) -> bool:
        """
        Checks whether a room is available.

        Args:
            room (Room): The room to check.

        Returns:
            bool: True if the room is available, False otherwise.
        """
        return room.get_status() == "available"


    def room_data(self, user: User, room: Room) -> dict | None:
        """
        Retrieves information about a room reserved by a user.

        If the room exists in the user's reservation history, the method
        returns a dictionary containing details about the room and the
        user who holds the reservation.

        Args:
            user (User): The user who holds the reservation.
            room (Room): The room to retrieve information from.

        Returns:
            dict | None: A dictionary with the room information if the
            user has reserved it, or None otherwise.
        """
        if room in user.history:
            return {
                "room_holder": user.get_name(),
                "room_number": room.get_room_number(),
                "room_type": room.get_room_type(),
                "status": room.get_status(),
            }
        return None