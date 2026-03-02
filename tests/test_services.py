import pytest
from pathlib import Path
from src.HotelApp.models import User, Room
from src.HotelApp.services import UserService, HotelService
from src.HotelApp.storage import JSONStorage
from src.HotelApp.exceptions import UserNotFoundError, UserAlreadyExistsError


class TestUserService:
    
    @pytest.fixture
    def storage(self, tmp_path):
        return JSONStorage(tmp_path / "users.json")
    
    @pytest.fixture
    def service(self, storage):
        return UserService(storage)
    
    def test_create_user(self, service):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        service.create_user(user)
        assert service.get_user(1).get_name == "Juan"
    
    def test_create_duplicate_user(self, service):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        service.create_user(user)
        with pytest.raises(UserAlreadyExistsError):
            service.create_user(user)
    
    def test_get_nonexistent_user(self, service):
        with pytest.raises(UserNotFoundError):
            service.get_user(999)
    
    def test_delete_user(self, service):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        service.create_user(user)
        service.delete_user(1)
        with pytest.raises(UserNotFoundError):
            service.get_user(1)


class TestHotelService:
    
    @pytest.fixture
    def storage(self, tmp_path):
        return JSONStorage(tmp_path / "rooms.json")
    
    @pytest.fixture
    def service(self, storage):
        return HotelService(storage)
    
    def test_reserve_room(self, service):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        room = Room(room_number=101, room_type="Single")
        service.reservate_room(user, room)
        assert room.get_status() == "occupied"
    
    def test_check_availability(self, service):
        room = Room(room_number=101, room_type="Single")
        assert service.check_availability(room) is True