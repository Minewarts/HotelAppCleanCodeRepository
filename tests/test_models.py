import pytest
from src.HotelApp.models import User, Room, Hotel
from src.HotelApp.exceptions import InvalidUserDataError


class TestUser:

    def test_create_valid_user(self):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")

        assert user.get_id() == 1
        assert user.get_name() == "Juan"
        assert user.get_email() == "juan@gmail.com"
        assert user.history == []

    def test_user_invalid_id(self):
        with pytest.raises(InvalidUserDataError):
            User(user_id=0, name="Juan", email="juan@gmail.com")

    def test_user_invalid_email(self):
        with pytest.raises(InvalidUserDataError):
            User(user_id=1, name="Juan", email="juangmail.com")

    def test_set_valid_email(self):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        user.set_email("nuevo@gmail.com")

        assert user.get_email() == "nuevo@gmail.com"

    def test_set_invalid_email(self):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")

        with pytest.raises(InvalidUserDataError):
            user.set_email("correo_invalido")


class TestRoom:

    def test_create_room(self):
        room = Room(room_number=101, room_type="Single")

        assert room.get_room_number() == 101
        assert room.get_room_type() == "Single"
        assert room.get_status() == "available"

    def test_invalid_room_number(self):
        with pytest.raises(ValueError):
            Room(room_number=0, room_type="Single")

    def test_toggle_status(self):
        room = Room(room_number=101, room_type="Single")

        room.set_status("occupied")
        assert room.get_status() == "occupied"

        room.set_status("available")
        assert room.get_status() == "available"

    def test_invalid_status_assignment(self):
        room = Room(room_number=101, room_type="Single")

        with pytest.raises(ValueError):
            room.set_status("broken")


class TestHotel:

    def test_create_hotel(self):
        hotel = Hotel(name="Hilton", stars=5)

        assert hotel.get_name() == "Hilton"
        assert hotel.get_stars() == 5

    def test_add_and_get_room(self):
        hotel = Hotel(name="TestHotel")
        room = Room(room_number=101, room_type="Single")

        hotel.add_room(room)

        found_room = hotel.get_room_by_number(101)
        assert found_room is not None
        assert found_room.get_room_type() == "Single"

    def test_add_duplicate_room(self):
        hotel = Hotel(name="TestHotel")
        room = Room(room_number=101, room_type="Single")

        hotel.add_room(room)

        with pytest.raises(ValueError):
            hotel.add_room(room)

    def test_add_and_get_client(self):
        hotel = Hotel(name="TestHotel")
        user = User(user_id=1, name="Juan", email="juan@gmail.com")

        hotel.add_client(user)

        found_client = hotel.get_client_by_id(1)
        assert found_client is not None
        assert found_client.get_name() == "Juan"

    def test_get_nonexistent_room(self):
        hotel = Hotel(name="TestHotel")
        assert hotel.get_room_by_number(999) is None

    def test_get_nonexistent_client(self):
        hotel = Hotel(name="TestHotel")
        assert hotel.get_client_by_id(999) is None