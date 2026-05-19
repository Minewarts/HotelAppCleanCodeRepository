"""
Unit tests for the models module.

These tests validate the core business logic of User, Room, Hotel, and UserHistory models,
including validation rules and getter/setter methods.
"""

from decimal import Decimal
import pytest
from HotelApp.models import User, Room, Hotel, UserHistory
from HotelApp.core.exceptions import InvalidUserDataError


class TestUser:
    """Tests for the User model."""

    def test_create_valid_user(self):
        """Test creating a user with valid data."""
        user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        assert user.get_id() == 1
        assert user.get_first_name() == "Juan"
        assert user.get_last_name() == "Perez"
        assert user.get_email() == "juan@gmail.com"

    def test_user_invalid_id_zero(self):
        """Test that zero ID raises InvalidUserDataError."""
        with pytest.raises(InvalidUserDataError):
            User(user_id=0, first_name="Juan", last_name="Perez", email="juan@gmail.com")

    def test_user_invalid_id_negative(self):
        """Test that negative ID raises InvalidUserDataError."""
        with pytest.raises(InvalidUserDataError):
            User(user_id=-1, first_name="Juan", last_name="Perez", email="juan@gmail.com")

    def test_user_invalid_email_no_at(self):
        """Test that email without @ raises InvalidUserDataError."""
        with pytest.raises(InvalidUserDataError):
            User(user_id=1, first_name="Juan", last_name="Perez", email="juangmail.com")

    def test_user_invalid_email_empty(self):
        """Test that empty email raises InvalidUserDataError."""
        with pytest.raises(InvalidUserDataError):
            User(user_id=1, first_name="Juan", last_name="Perez", email="")


class TestRoom:
    """Tests for the Room model."""

    def test_create_room(self):
        """Test creating a room with valid data."""
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        assert room.get_number_id() == "101"
        assert room.get_room_type() == "Single"
        assert room.get_price_per_night() == Decimal("50.00")
        assert room.get_status() == "Disponible"

    def test_room_status_change(self):
        """Test changing room status."""
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        room.set_status("Ocupada")
        assert room.get_status() == "Ocupada"

    def test_invalid_status_assignment(self):
        """Test that invalid status raises ValueError."""
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        with pytest.raises(ValueError):
            room.set_status("Invalid")

    def test_invalid_price_zero(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError):
            Room(number_id="101", room_type="Single", price_per_night=Decimal("0"))

    def test_invalid_price_negative(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError):
            Room(number_id="101", room_type="Single", price_per_night=Decimal("-50"))


class TestHotel:
    """Tests for the Hotel model."""

    def test_create_hotel(self):
        """Test creating a hotel."""
        hotel = Hotel(name="Hilton", address="123 Main St", phone="555-1234")
        assert hotel.get_name() == "Hilton"
        assert hotel.get_address() == "123 Main St"
        assert hotel.get_phone() == "555-1234"

    def test_add_and_get_room(self):
        """Test adding and retrieving a room."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        hotel.add_room(room)
        
        found_room = hotel.get_room_by_number("101")
        assert found_room is not None
        assert found_room.get_room_type() == "Single"

    def test_add_duplicate_room(self):
        """Test that duplicate room raises ValueError."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        room = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        hotel.add_room(room)
        
        with pytest.raises(ValueError):
            hotel.add_room(room)

    def test_add_and_get_client(self):
        """Test adding and retrieving a client."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        user = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        hotel.add_client(user)
        
        found_client = hotel.get_client_by_id(1)
        assert found_client is not None
        assert found_client.get_first_name() == "Juan"

    def test_get_nonexistent_room(self):
        """Test getting nonexistent room returns None."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        assert hotel.get_room_by_number("999") is None

    def test_get_nonexistent_client(self):
        """Test getting nonexistent client returns None."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        assert hotel.get_client_by_id(999) is None

    def test_get_all_rooms(self):
        """Test getting all rooms."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        room1 = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        room2 = Room(number_id="102", room_type="Double", price_per_night=Decimal("75.00"))
        hotel.add_room(room1)
        hotel.add_room(room2)
        
        all_rooms = hotel.get_all_rooms()
        assert len(all_rooms) == 2

    def test_get_all_clients(self):
        """Test getting all clients."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        user1 = User(user_id=1, first_name="Juan", last_name="Perez", email="juan@gmail.com")
        user2 = User(user_id=2, first_name="Maria", last_name="Lopez", email="maria@gmail.com")
        hotel.add_client(user1)
        hotel.add_client(user2)
        
        all_clients = hotel.get_all_clients()
        assert len(all_clients) == 2

    def test_get_room_by_type(self):
        """Test getting room by type."""
        hotel = Hotel(name="TestHotel", address="123 Main St", phone="555-1234")
        single = Room(number_id="101", room_type="Single", price_per_night=Decimal("50.00"))
        double = Room(number_id="102", room_type="Double", price_per_night=Decimal("75.00"))
        hotel.add_room(single)
        hotel.add_room(double)
        
        found = hotel.get_room_by_type("Double")
        assert found is not None
        assert found.get_number_id() == "102"


class TestUserHistory:
    """Tests for the UserHistory model."""

    def test_create_user_history(self):
        """Test creating user history."""
        history = UserHistory(user_id=1, action="Check-in", description="Room 101")
        assert history.get_user_id() == 1
        assert history.get_action() == "Check-in"
        assert history.get_description() == "Room 101"

    def test_history_without_description(self):
        """Test creating history without description."""
        history = UserHistory(user_id=1, action="Check-out")
        assert history.get_action() == "Check-out"
        assert history.get_description() is None

    def test_invalid_action_empty(self):
        """Test that empty action raises ValueError."""
        with pytest.raises(ValueError):
            UserHistory(user_id=1, action="")

    def test_invalid_user_id_zero(self):
        """Test that zero user_id raises ValueError."""
        with pytest.raises(ValueError):
            UserHistory(user_id=0, action="Check-in")

    def test_history_has_timestamp(self):
        """Test that history has a timestamp."""
        history = UserHistory(user_id=1, action="Check-in")
        assert history.get_timestamp() is not None
