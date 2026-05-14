"""
Configuración central de la aplicación HOT TEL.

Usa pydantic-settings para leer variables de entorno desde el archivo .env.
Se instancia una sola vez como singleton (``settings``) y se importa
desde cualquier módulo que lo necesite.

Ejemplo de uso::

    from src.core.config import settings

    client = create_client(settings.supabase_url, settings.supabase_key)
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables de entorno validadas y tipadas al arrancar la app."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Supabase ──────────────────────────────────────────────────────────────
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    use_supabase: bool = False

    # ── FastAPI ───────────────────────────────────────────────────────────────
    api_base_url: str = "http://localhost:8000"
    api_title: str = "HOT TEL API"
    api_version: str = "1.0.0"

    # ── Entorno ───────────────────────────────────────────────────────────────
    debug: bool = False


# Singleton: se carga al importar el módulo por primera vez.
settings = Settings()