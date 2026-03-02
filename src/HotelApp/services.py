from .models import User
from .storage import Storage
from .storage import Room
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
)


class UserService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def create_user(self, user: User) -> None:
        # check for required fields
        if user.id <= 0:
            raise InvalidUserDataError("User id must be a positive integer")

        if not user.name.strip():
            raise InvalidUserDataError("User name cannot be empty")

        if "@" not in user.email:
            raise InvalidUserDataError("Invalid email address")

        users = self.storage.load()

        # check for duplicate id
        if any(u.id == user.id for u in users):
            raise UserAlreadyExistsError(user.id)

        # finally add the user if all checks pass
        users.append(user)
        self.storage.save(users)

        # check if the user is in the system
    def get_user(self, user_id: int) -> User:
        users = self.storage.load()
        for user in users:
            if user.id == user_id:
                return user
        raise UserNotFoundError(f"User {user_id} not found")

    def delete_user(self, user_id: int) -> None:
        users = self.storage.load()
        filtered = [u for u in users if u.id != user_id]

        if len(filtered) == len(users):
            raise UserNotFoundError(f"User {user_id} not found")

        self.storage.save(filtered)


class HotelService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def reservate_room(self, user:User, room:Room):
        if room.get_status() == 'available':
            room.set_status()
            user.history.append(room)
        else:
            raise Exception("Room is not available")

    def cancel_reservation(self, user:User, room:Room):
        if room in self.storage.load():
            room.set_status('available')
            user.history.remove(room)
        else:
            raise Exception("Room is not reserved stupid 🤣")

    def check_availability(self, room:Room):
        return room.get.status() == 'available'
    
    def room_data(self, user:User, room:Room):
        if room in user.history:
            return {
                "room_holder": user.name,
                "room_number": room.number,
                "room_type": room.type,
                "status": room.get_status(),
            }
