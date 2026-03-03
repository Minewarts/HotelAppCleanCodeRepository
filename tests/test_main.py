import pytest
from typer.testing import CliRunner

from main import app
from src.HotelApp.storage import JSONStorage
from src.HotelApp.services import UserService, HotelService

runner = CliRunner()


class TestCLI:

    @pytest.fixture
    def isolated_app(self, tmp_path, monkeypatch):
        """
        Reemplaza el storage real de main.py por uno temporal.
        """

        temp_storage = JSONStorage(tmp_path / "test_db.json")
        user_service = UserService(temp_storage)
        hotel_service = HotelService(temp_storage)

        monkeypatch.setattr("main.storage", temp_storage)
        monkeypatch.setattr("main.user_service", user_service)
        monkeypatch.setattr("main.hotel_service", hotel_service)

        return temp_storage

    def test_create_user_command(self, isolated_app):
        result = runner.invoke(app, ["create-user", "1", "Juan", "juan@gmail.com"])

        assert result.exit_code == 0
        assert "creado con éxito" in result.stdout

    def test_list_users_command(self, isolated_app):
        runner.invoke(app, ["create-user", "1", "Juan", "juan@gmail.com"])
        result = runner.invoke(app, ["list-users"])

        assert result.exit_code == 0
        assert "Juan" in result.stdout

    def test_book_room_command(self, isolated_app):
        runner.invoke(app, ["create-user", "1", "Juan", "juan@gmail.com"])
        result = runner.invoke(app, ["book", "1", "101", "Single"])

        assert result.exit_code == 0
        assert "reservada" in result.stdout

    def test_cancel_booking_command(self, isolated_app):
        runner.invoke(app, ["create-user", "1", "Juan", "juan@gmail.com"])
        runner.invoke(app, ["book", "1", "101", "Single"])

        result = runner.invoke(app, ["cancel", "1", "101"])

        assert result.exit_code == 0
        assert "cancelada" in result.stdout

    def test_create_user_invalid_email(self, isolated_app):
        result = runner.invoke(app, ["create-user", "1", "Juan", "correo_invalido"])

        assert result.exit_code == 1
        assert "Error" in result.stdout