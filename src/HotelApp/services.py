from typing import List

from .models import User, Room, Hotel
from .storage import Storage

from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
)


class UserService:
    '''Service responsible for managing user-related operations'''
    def __init__(self, storage: Storage):
        self.storage = storage

    def create_user(self, user: User) -> None:
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
    def __init__(self, storage: Storage):
        self.storage = storage

    def reserve_room(self, user: User, room: Room) -> None:
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
        return room.get_status() == "available"

    def room_data(self, user: User, room: Room) -> dict | None:
        if room in user.history:
            return {
                "room_holder": user.get_name(),
                "room_number": room.get_room_number(),
                "room_type": room.get_room_type(),
                "status": room.get_status(),
            }
        return None
