from HotelApp.app.main import create_api_client
from HotelApp.app.api_client import ApiClient


def test_create_api_client_returns_client() -> None:
    client = create_api_client()

    assert isinstance(client, ApiClient)
    assert client.base_url == "http://localhost:8000"
