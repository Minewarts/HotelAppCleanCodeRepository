import pytest
import json
from pathlib import Path

from src.HotelApp.models import User, Room
from src.HotelApp.storage import JSONStorage


class TestJSONStorage:

    @pytest.fixture
    def storage(self, tmp_path):
        return JSONStorage(tmp_path / "users.json")

    def test_load_when_file_not_exists(self, storage):
        # Si el archivo no existe debe devolver lista vacía
        users = storage.load()
        assert users == []

    def test_save_and_load_user(self, storage):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        storage.save([user])

        loaded_users = storage.load()

        assert len(loaded_users) == 1
        assert loaded_users[0].get_id() == 1
        assert loaded_users[0].get_name() == "Juan"
        assert loaded_users[0].get_email() == "juan@gmail.com"

    def test_save_and_load_user_with_room_history(self, storage):
        user = User(user_id=1, name="Juan", email="juan@gmail.com")
        room = Room(room_number=101, room_type="Single")
        room.set_status("occupied")
        user.history.append(room)

        storage.save([user])
        loaded_users = storage.load()

        assert len(loaded_users) == 1
        loaded_user = loaded_users[0]

        assert len(loaded_user.history) == 1
        loaded_room = loaded_user.history[0]

        assert loaded_room.get_room_number() == 101
        assert loaded_room.get_room_type() == "Single"
        assert loaded_room.get_status() == "occupied"

    def test_overwrite_existing_file(self, storage):
        user1 = User(user_id=1, name="Juan", email="juan@gmail.com")
        storage.save([user1])

        user2 = User(user_id=2, name="Maria", email="maria@gmail.com")
        storage.save([user2])

        loaded_users = storage.load()

        assert len(loaded_users) == 1
        assert loaded_users[0].get_id() == 2

    def test_load_corrupted_json(self, storage):
        # Creamos manualmente un JSON inválido
        storage.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(storage.filepath, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")

        with pytest.raises(Exception):
            storage.load()