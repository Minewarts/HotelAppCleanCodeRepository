"""
Unit tests for the services module.

These tests validate the business logic of UserServices and HotelService,
including user and hotel management operations.
"""

from decimal import Decimal
import pytest
from unittest.mock import MagicMock
from HotelApp.services import UserServices, HotelService
from HotelApp.models import User, Room, UserHistory
from HotelApp.core.exceptions import UserNotFoundError, InvalidUserDataError, UserAlreadyExistsError


class TestUserService:
    """Tests for the UserServices class."""

    def test_create_user_success(self):
        """Test successfully creating a user."""
        fake_storage = MagicMock()
        fake_storage.load.return_value = []
        
        service = UserServices(fake_storage)
        user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        service.create_user(user)
        
        fake_storage.save.assert_called_once()

    def test_create_user_invalid_id(self):
        """Test creating user with invalid ID raises InvalidUserDataError."""
        fake_storage = MagicMock()
        
        service = UserServices(fake_storage)
        user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        
        with pytest.raises(InvalidUserDataError):
            user_invalid = User(user_id=0, first_name="Juan", last_name="Perez", email="juan@gmail.com")

    def test_create_user_duplicate(self):
        """Test that creating duplicate user raises UserAlreadyExistsError."""
        fake_storage = MagicMock()
        existing_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        fake_storage.load.return_value = [existing_user]
        
        service = UserServices(fake_storage)
        duplicate_user = User(user_id=1, first_name="Pedro", last_name="Lopez", email="pedro@gmail.com")
        
        with pytest.raises(UserAlreadyExistsError):
            service.create_user(duplicate_user)

    def test_get_user_by_id(self):
        """Test retrieving user by ID."""
        fake_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        fake_storage = MagicMock()
        fake_storage.load.return_value = [fake_user]
        
        service = UserServices(fake_storage)
        result = service.get_user(1)
        
        assert result.get_id() == 1
        assert result.get_first_name() == "Juan"

    def test_get_nonexistent_user(self):
        """Test that getting nonexistent user raises UserNotFoundError."""
        fake_storage = MagicMock()
        fake_storage.load.return_value = []
        
        service = UserServices(fake_storage)
        
        with pytest.raises(UserNotFoundError):
            service.get_user(999)

    def test_update_user(self):
        """Test updating user information."""
        existing_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        fake_storage = MagicMock()
        fake_storage.load.return_value = [existing_user]
        
        service = UserServices(fake_storage)
        updated_user = service.update_user(1, first_name="Pedro", last_name="Lopez")
        
        assert updated_user.get_first_name() == "Pedro"
        assert updated_user.get_last_name() == "Lopez"

    def test_delete_user(self):
        """Test deleting a user."""
        existing_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        fake_storage = MagicMock()
        fake_storage.load.return_value = [existing_user]
        
        service = UserServices(fake_storage)
        service.delete_user(1)
        
        fake_storage.save.assert_called_once()


class TestHotelService:
    """Tests for the HotelService class."""

    def test_log_user_action(self):
        """Test logging a user action."""
        existing_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        fake_storage = MagicMock()
        fake_storage.load.return_value = [existing_user]
        
        service = HotelService(fake_storage)
        history = service.log_user_action(1, "Check-in", "Room 101")
        
        assert history.get_action() == "Check-in"
        assert history.get_description() == "Room 101"

    def test_log_action_nonexistent_user(self):
        """Test logging action for nonexistent user raises UserNotFoundError."""
        fake_storage = MagicMock()
        fake_storage.load.return_value = []
        
        service = HotelService(fake_storage)
        
        with pytest.raises(UserNotFoundError):
            service.log_user_action(999, "Check-in")

    def test_get_user_history(self):
        """Test retrieving user history."""
        existing_user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        history = UserHistory(user_id=1, action="Check-in", description="Room 101")
        existing_user.history.append(history)
        
        fake_storage = MagicMock()
        fake_storage.load.return_value = [existing_user]
        
        service = HotelService(fake_storage)
        result = service.get_user_history(1)
        
        assert len(result) == 1
        assert result[0].get_action() == "Check-in"

    def test_get_history_nonexistent_user(self):
        """Test getting history for nonexistent user raises UserNotFoundError."""
        fake_storage = MagicMock()
        fake_storage.load.return_value = []
        
        service = HotelService(fake_storage)
        
        with pytest.raises(UserNotFoundError):
            service.get_user_history(999)

    def test_check_availability(self):
        """Test checking room availability."""
        fake_storage = MagicMock()
        
        service = HotelService(fake_storage)
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        
        assert service.check_availability(room) is True
        
        room.set_status("Ocupada")
        assert service.check_availability(room) is False
