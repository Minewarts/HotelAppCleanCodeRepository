import pytest
from unittest.mock import MagicMock
from src.HotelApp.services import UserService, HotelService
from src.HotelApp.models import User
from src.HotelApp.models import Room


class TestUserService:

    def test_create_user_calls_storage(self):
        fake_storage = MagicMock()
        service = UserService(fake_storage)

        service.create_user("1", "Juan", "juan@gmail.com")

        fake_storage.save_user.assert_called_once()

    def test_get_user_by_id(self):
        fake_storage = MagicMock()
        fake_user = User("1", "Juan", "juan@gmail.com")
        fake_storage.get_user_by_id.return_value = fake_user

        service = UserService(fake_storage)

        result = service.get_user_by_id("1")

        assert result == fake_user
        fake_storage.get_user_by_id.assert_called_once_with("1")

    def test_create_user_invalid_email(self):
        fake_storage = MagicMock()
        service = UserService(fake_storage)

        with pytest.raises(ValueError):
            service.create_user("1", "Juan", "correo_invalido")


class TestHotelService:

    def test_add_room_calls_storage(self):
        fake_storage = MagicMock()
        service = HotelService(fake_storage)

        service.add_room("101", "Single")

        fake_storage.save_room.assert_called_once()

    def test_get_room(self):
        fake_storage = MagicMock()
        fake_room = Room("101", "Single")
        fake_storage.get_room_by_number.return_value = fake_room

        service = HotelService(fake_storage)

        result = service.get_room("101")

        assert result == fake_room
        fake_storage.get_room_by_number.assert_called_once_with("101")

    def test_book_room(self):
        fake_storage = MagicMock()
        fake_room = Room("101", "Single")
        fake_storage.get_room_by_number.return_value = fake_room

        service = HotelService(fake_storage)

        service.book_room("101")

        assert fake_room.is_reserved is True
        fake_storage.save_room.assert_called()