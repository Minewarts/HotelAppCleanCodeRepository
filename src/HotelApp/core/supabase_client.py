"""
Cliente de Supabase para HOT TEL.

Crea una única instancia del cliente que se reutiliza en toda la aplicación.
Las credenciales se leen desde las variables de entorno a través de `settings`.

Ejemplo de uso::

    from src.HotelApp.core.supabase_client import get_supabase_client

    client = get_supabase_client()
    data = client.table("users").select("*").execute()
"""

from supabase import Client, create_client

from .config import settings

_client: Client | None = None


def get_supabase_client() -> Client:
    """
    Returns the Supabase client singleton.

    The client is created once and reused across all calls.

    Returns:
        Client: The Supabase client instance.

    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_KEY are not configured.
    """
    global _client

    if _client is None:
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in the .env file."
            )
        _client = create_client(settings.supabase_url, settings.supabase_key)

    return _client