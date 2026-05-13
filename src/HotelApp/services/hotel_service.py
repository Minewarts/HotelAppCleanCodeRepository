from ..models import User, Room, UserHistory, Hotel
from ..storage import Storage
from ..core.exceptions import UserNotFoundError, InvalidUserDataError


class HotelService:
    """
    Service responsible for hotel operations:
    - Record user actions (check-in, reservations, cancellations).
    - Log events in user history.
    - Manage room availability.
    """

    def __init__(self, storage: Storage):
        """
        Initializes the hotel service with a storage system.

        Args:
            storage (Storage): Object responsible for persisting user information.
        """
        self.storage = storage

    def log_user_action(
        self, user_id: int, action: str, description: str | None = None
    ) -> UserHistory:
        """
        Records an action in a user's history.

        Args:
            user_id (int): The ID of the user.
            action (str): Description of the action (e.g., "Check-in", "Reservation").
            description (str | None): Additional details about the action.

        Returns:
            UserHistory: The created history record.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        users = self.storage.load()
        user = None
        for u in users:
            if u.get_id() == user_id:
                user = u
                break

        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")

        history = UserHistory(user_id=user_id, action=action, description=description)
        user.history.append(history)
        self.storage.save(users)

        return history

    def get_user_history(self, user_id: int) -> list[UserHistory]:
        """
        Retrieves all history records for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[UserHistory]: List of history records.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        users = self.storage.load()
        for user in users:
            if user.get_id() == user_id:
                return user.history

        raise UserNotFoundError(f"User {user_id} not found")

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
