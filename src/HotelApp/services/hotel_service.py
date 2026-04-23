from ..models import User, Room, UserHistory
from ..storage import Storage
from ..exceptions import UserNotFoundError


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
        the room status is changed to "occupied" and a new UserHistory
        is created and added to the user's history. The changes are then
        persisted in the storage system.

        Args:
            user (User): The user who wants to reserve the room.
            room (Room): The room to be reserved.

        Raises:
            Exception: If the room is not available.
            UserNotFoundError: If the user does not exist in storage.
        """
        # Verificamos disponibilidad
        if room.get_status() != "available":
            raise Exception("Room is not available")

        # ocupamos la habitación y añadimos al historial del usuario
        room.set_status("occupied")
        user_history = UserHistory(user, room)
        user.history.append(user_history)

        # persistir cambios en storage
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

        The method finds the active UserHistory for the room and checks out.
        The room status is changed to "available". The changes are
        then saved in the storage system.

        Args:
            user (User): The user who cancels the reservation.
            room (Room): The room whose reservation will be canceled.

        Raises:
            Exception: If the room is not reserved by the user.
            UserNotFoundError: If the user does not exist in storage.
        """
        # encontrar el UserHistory activo para esta habitación
        active_history = None
        for history in user.history:
            if history.get_room() == room and history.is_active():
                active_history = history
                break

        if not active_history:
            raise Exception("Room is not reserved by the user")

        # check out y liberar habitación
        active_history.check_out()
        room.set_status("available")

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

        If the room exists in the user's active reservation history, the method
        returns a dictionary containing details about the room and the
        user who holds the reservation.

        Args:
            user (User): The user who holds the reservation.
            room (Room): The room to retrieve information from.

        Returns:
            dict | None: A dictionary with the room information if the
            user has reserved it, or None otherwise.
        """
        for history in user.history:
            if history.get_room() == room and history.is_active():
                return {
                    "room_holder": user.get_name(),
                    "room_number": room.get_room_number(),
                    "room_type": room.get_room_type(),
                    "status": room.get_status(),
                }
        return None
