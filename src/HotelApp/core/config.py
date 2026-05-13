"""
Configuración central de la aplicación.

Usa pydantic-settings para leer variables de entorno desde el archivo .env.
Se instancia una sola vez como singleton (``settings``) y se importa
desde cualquier módulo que lo necesite.

Ejemplo de uso::

    from src.core.config import settings

    client = create_client(settings.supabase_url, settings.supabase_key)
"""