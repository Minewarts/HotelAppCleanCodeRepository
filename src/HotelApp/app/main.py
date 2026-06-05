"""
HOT TEL - Capa de aplicación

Este módulo ofrece el adaptador de cliente HTTP para la interfaz del
programa y ya no contiene una interfaz de línea de comandos.
"""

from .api_client import ApiClient


def create_api_client() -> ApiClient:
    """Devuelve un cliente HTTP configurado para comunicarse con la API."""
    return ApiClient()


__all__ = ["ApiClient", "create_api_client"]
